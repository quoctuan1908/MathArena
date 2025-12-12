import { useEffect, useState } from "react";
import ChatBox from "../components/communication/chatbox";
import MessageBox from "../components/communication/messageBox";
import apiSlice from "../store/apiSlice";
import type { Message, MessageCreate } from "../types/message";
import type { RoomChat } from "../types/roomchat";
import { useParams, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import type { RootState, AppDispatch } from "../store/store";
import { connectToSocket, sendSocketMessage } from "../socket";
import { Button } from "../components/Button";

const CommunicationPage = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const user = useSelector((state: RootState) => state.auth.user);
  const room_id = useSelector((state: RootState) => state.socket.room_id);
  const lastEvent = useSelector((state: RootState) => state.socket.lastEvent);
  const lastPayload = useSelector((state: RootState) => state.socket.lastPayload);

  const [roomData, setRoomData] = useState<RoomChat | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [hasJoined, setHasJoined] = useState(false);

  const [getRoomChatById] = apiSlice.endpoints.getRoomChatById.useLazyQuery();
  const [getMessageByRoomChatId] = apiSlice.endpoints.getMessageByRoomChatId.useLazyQuery();
  const [getUserRoomByUserId] = apiSlice.endpoints.getUserRoomByUserId.useLazyQuery();

  // Lấy dữ liệu phòng và kiểm tra user đã tham gia chưa
  useEffect(() => {
    if (!id || !user) return;

    const fetchRoomAndCheckJoin = async () => {
      try {
        // 1. Lấy thông tin phòng
        const roomRes = await getRoomChatById(id);
        if (!roomRes || !roomRes.data) return; // ✅ kiểm tra undefined
        const room = roomRes.data;
        setRoomData(room);

        // 2. Kiểm tra user đã join chưa
        const userRoomsRes = await getUserRoomByUserId(user.id);
        console.log(userRoomsRes)
        const joined = userRoomsRes?.data?.some(
          (r) => r.room_chat_id === room.room_chat_id
        );
        setHasJoined(joined ?? false);

        // 3. Nếu đã join → load messages
        if (joined) {
          const msgRes = await getMessageByRoomChatId(room.room_chat_id);
          if (msgRes?.data) setMessages(msgRes.data);
        }
      } catch (err) {
        console.error("Error fetching room or user-room data:", err);
      }
    };

    fetchRoomAndCheckJoin();
  }, [id, user]);

  // Kết nối socket nếu đã join
  useEffect(() => {
    if (hasJoined && roomData?.room_chat_id && room_id !== roomData.room_chat_id) {
      dispatch(connectToSocket(roomData.room_chat_id));
    }
  }, [hasJoined, roomData, dispatch, room_id]);

  // Khi có message mới từ socket
  useEffect(() => {
    if (lastEvent === "receive_message" || lastEvent === "broadcast") {
      setMessages((prev) => [...prev, lastPayload]);
    }
  }, [lastEvent, lastPayload]);

  // Gửi tin nhắn
  const handleSend = (msg: MessageCreate) => {
    dispatch(sendSocketMessage("send_message", msg));
  };

  //Tham gia phòng
  const handleJoinRoom = async () => {
    if (!user || !roomData) return;
    try {
      const joinRoomRequest = {
        room_chat_id: roomData.room_chat_id,
        user_id: user.id,
        user_room_role_id: "2",
      };
      await dispatch(apiSlice.endpoints.joinRoom.initiate(joinRoomRequest)).unwrap();
      setHasJoined(true);
      // Load messages sau khi join
      const msgRes = await getMessageByRoomChatId(roomData.room_chat_id);
      if (msgRes.data) setMessages(msgRes.data);
    } catch (err: any) {
      console.error("Join room failed:", err);
      alert("Tham gia phòng thất bại!: " + err.data.detail);
    }
  };

  //  Render
  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
        <p>Vui lòng đăng nhập để tham gia phòng.</p>
        <Button onClick={() => navigate("/login")}>Đăng nhập</Button>
      </div>
    );
  }

  if (!roomData) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
        <p>Đang tải thông tin phòng...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {hasJoined ? (
        <>
          <div className="flex-1 overflow-y-auto p-4">
            <ChatBox messages={messages} />
          </div>
          <div className="border-t bg-white p-0 shadow-md sticky bottom-0">
            <MessageBox onSend={handleSend} room_data={roomData} />
          </div>
        </>
      ) : (
        <div className="flex flex-col items-center justify-center flex-1">
          <p className="text-lg mb-4">Bạn chưa tham gia phòng này</p>
          <Button onClick={handleJoinRoom} className="px-4 py-2 bg-blue-600 text-white rounded">
            Tham gia phòng
          </Button>
        </div>
      )}
    </div>
  );
};

export default CommunicationPage;
