import { useEffect, useState } from "react";
import apiSlice from "../store/apiSlice";
import type { RoomChat } from "../types/roomchat";
import QuizRoomCard from "../components/communication/quizRoomCard";
import type { UserRoom, UserRoomCreate } from "../types/userRoom";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import type { RootState, AppDispatch } from "../store/store";
import { connectToSocket} from "../socket";
import { clearRoomData } from "../store/socketSlice";

const QuizListPage = () => {
  const [getRoomQuiz] = apiSlice.endpoints.getRoomQuiz.useLazyQuery();
  const [getUserRoomByUserId] = apiSlice.endpoints.getUserRoomByUserId.useLazyQuery();
  const [quizRoomList, setQuizRoomList] = useState<RoomChat[]>([]);
  const [userRoom, setUserRoom] = useState<UserRoom[]>([]);
  const user = useSelector((state: RootState) => state.auth.user);
  const roomUserCounts = useSelector((state: RootState) => state.socket.roomUserCounts); 
  const allRooms = useSelector((state: RootState) => state.socket.allRooms);
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  // 🔹 1. Lấy danh sách phòng và user-room ban đầu
  useEffect(() => {
    const fetchQuizRoomAndUserRooms = async () => {
      const result = await getRoomQuiz();
      if (result.data) setQuizRoomList(result.data);

      if (user) {
        const userRooms = await getUserRoomByUserId(user.id);
        if (userRooms?.data) setUserRoom(userRooms.data);
      }
    };
    fetchQuizRoomAndUserRooms();
  }, [user]);

  // 🔹 2. Kết nối socket
  useEffect(() => {
    dispatch(connectToSocket("quiz-room"));
  }, []);

  // 🔹 4. Join room
  const QUIZ_ROOM_TYPE_ID = "3";

  const joinQuizRoom = async (room_chat_id: string, user_id: string, user_room_role_id: string) => {
    // Lọc tất cả userRoom thuộc loại Quiz
    const quizUserRooms = userRoom.filter(
      (room) => room.room_chats.room_type.room_type_id == QUIZ_ROOM_TYPE_ID
    );

    dispatch(clearRoomData());

    // Kiểm tra xem user đã có trong phòng đó chưa
    const alreadyJoined = quizUserRooms.some(
      (room) => room.room_chat_id === room_chat_id && room.user_id === user_id
    );
    console.log(quizUserRooms)
    if (alreadyJoined) {
      alert("⚠️ Bạn đã tham gia phòng này rồi!");
      return; // dừng, không join lại
    }

    // Kiểm tra room_capacity
    const room = quizRoomList.find((r) => r.room_chat_id === room_chat_id);
    if (room && room.room_capacity !== null) {
      const currentCount =
        roomUserCounts[room_chat_id] ??
        allRooms.find((r) => r.room_id === room_chat_id)?.count ??
        0;

      if (currentCount >= room.room_capacity) {
        alert("⚠️ Phòng đã đầy!");
        return;
      }
    }

    // 🔹 Gửi join room request
    const joinRoomRequest: UserRoomCreate = { room_chat_id, user_id, user_room_role_id };
    try {
      const joinRoomResult = await dispatch(apiSlice.endpoints.joinRoom.initiate(joinRoomRequest)).unwrap();
      if (joinRoomResult) navigate("/quiz_room/" + joinRoomResult.room_chat_id);
    } catch (err) {
      console.error("Join room failed:", err);
    }
  };

  // 🔹 5. Render giao diện
  return (
    <div className="p-4 bg-gray-50 rounded-xl overflow-y-auto flex-1">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Phòng giải đố</h2>

      <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {quizRoomList.map((quizRoom) => {
          return (
            <QuizRoomCard
              key={quizRoom.room_chat_id}
              quizRoom={quizRoom}
              onJoin={joinQuizRoom}
              currentCount={
                roomUserCounts[quizRoom.room_chat_id] ??
                allRooms.find(r => r.room_id === quizRoom.room_chat_id)?.count ??
                0
              }
            />
          );
        })}
      </div>
    </div>
  );
};

export default QuizListPage;
