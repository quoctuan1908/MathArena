import { clearQueuedMessages, queueMessage, setConnected, setLastMessage, setRoomId, setPlayers, setGameCountdown, setGameStarted, setCurrentQuestion, updateScore, setGameFinished, setRoomUserCount, setAllRooms, clearRoomData} from "./store/socketSlice";
import type { AppDispatch, RootState } from "./store/store";


let ws: WebSocket | null = null;

export const connectToSocket = (room_chat_id: string) => (dispatch: AppDispatch, getState: () => RootState) => {
  const state = getState();
  const currentUser = state.auth.user; // lấy thông tin user từ redux
  if (!currentUser) return;

  if (ws) ws.close();

  ws = new WebSocket(import.meta.env.VITE_SOCKET_URL);

  ws.onopen = () => {
    console.log("✅ Socket connected");

    // Gửi join_room kèm thông tin user
    ws?.send(JSON.stringify({
      event: "join_room",
      payload: {
        room_id: room_chat_id,
        user: currentUser
      }
    }));

    dispatch(setConnected(true));
    dispatch(setRoomId(room_chat_id));

    // gửi các message đang queue
    const queued = getState().socket.queuedMessages;
    queued.forEach(msg => ws?.send(JSON.stringify(msg)));
    dispatch(clearQueuedMessages());
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (!data.event || !("payload" in data)) {
        console.warn("Nhận được message không rõ định dạng", data);
        return;
      }
      
      console.log("✅ Socket received:", data.event);
      console.log(data.payload)
      

      // --- PHÂN TUYẾN SỰ KIỆN (EVENT ROUTER) ---
      switch (data.event) {
        // --- Sự kiện Game (từ backend của bạn) ---
        case "game_countdown":
          dispatch(setGameCountdown(data.payload.time));
          break;
        
        case "game_started":
          dispatch(setGameStarted());
          break;

          case "quiz_update_question": {
            const { question, current_index, total_questions } = data.payload;
            dispatch(
              setCurrentQuestion({
                question,
                index: current_index ?? 0,
                total: total_questions ?? 0,
              })
            );
            dispatch(setGameStarted());
            break;
          }

        // --- Sự kiện Quản lý phòng ---
        case "joined":
        case "user_joined":
        case "user_left": {
          const {room_id, users, count} = data.payload
          dispatch(setPlayers(users));
          dispatch(setRoomUserCount({ room_id , count }));
          if (data.payload.rooms) {
            dispatch(setAllRooms(data.payload.rooms))
          }
          break;
        }
        case "user_left_self": {
          const {room_id, count} = data.payload
          dispatch(setRoomUserCount({ room_id , count }));
          break;
        }
        // --- Sự kiện Chat (ví dụ) ---
        case "receive_message":
        case "receive_answer":
        case "broadcast":
          dispatch(setLastMessage(data)); 
          break;
        case "answer_result":
          // Cập nhật điểm cho người chơi
          dispatch(updateScore({
            userId: data.payload.user_id,
            score: data.payload.total_score
          }));
          // Có thể hiển thị feedback đúng/sai
          dispatch(setLastMessage(data)); 
          break;
        case "player_answered":
          // frontend có thể hiện thông báo cạnh player đó
          dispatch(setLastMessage(data));
          break
        case "game_finished":
          console.log("🎉 Game finished:", data.payload.scores);
          dispatch(setGameFinished(data.payload)); // lưu bảng điểm cuối
          break;
        case "update_user_count": {
          const {room_id, count} = data.payload
          dispatch(setRoomUserCount({ room_id , count }));
          break;
        }

        default:
          console.log(`Unhandled event: ${data.event}`);
          dispatch(setLastMessage(data));
      }
      // ----------------------------------------

    } catch (err) {
      console.error("❌ Parse socket message error:", err);
    }
  };

  ws.onclose = () => {
    console.log("🔌 Socket closed");
    const state = getState(); 
    if (state.socket.room_id) {
      dispatch(setRoomUserCount({ room_id: state.socket.room_id, count: 0 })); 
      dispatch(clearRoomData()); 
    }

    // 2️⃣ Cập nhật kết nối
    dispatch(setConnected(false));
  };
};

// Gửi message qua socket, nếu chưa sẵn sàng thì queue
export const sendSocketMessage = (event: string, payload: any) => (dispatch: AppDispatch, getState: () => RootState) => {
  const { isConnected } = getState().socket;
  console.log("Hello")
  if (isConnected && ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ event, payload }));
  } else {
    console.log(`⚠️ WebSocket not ready, queuing message: ${event}`);
    dispatch(queueMessage({ event, payload }));
  }
};

export const disconnectSocket = () => (dispatch: AppDispatch) => {
  if (ws) {
    console.log("🔌 Disconnecting socket...");
    ws.close();
    ws = null;
  }

  // reset redux state
  dispatch(setConnected(false));
  dispatch(setRoomId(""));
};
