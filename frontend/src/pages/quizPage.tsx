import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useNavigate } from "react-router-dom";
import type { RootState, AppDispatch } from "../store/store";
import {
  connectToSocket,
  disconnectSocket,
  sendSocketMessage,
} from "../socket";

import QuizBox from "../components/communication/quizBox";
import PlayerBox from "../components/communication/playerBox";
import AnswerQuestionBox from "../components/communication/answerQuestionBox";

import type { RoomChat } from "../types/roomchat";
import type { FastAnswerQuestion } from "../types/questions";
import apiSlice from "../store/apiSlice";
import { Button } from "../components/Button";
import {
  clearRoomData,
  resetGameState,
} from "../store/socketSlice";

const QuizRoomPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  const user = useSelector((state: RootState) => state.auth.user);
  
  // Lấy danh sách questions từ Redux (đã được cập nhật khi game finished)
  const { room_id, gameStatus, countdownTime, currentQuestion, players, questionIndex, totalQuestions, questions } =
    useSelector((state: RootState) => state.socket);

  const [roomData, setRoomData] = useState<RoomChat>();
  
  // [MỚI] State để hiển thị bảng đáp án
  const [showResultBoard, setShowResultBoard] = useState(false);

  const [getRoomChatById] = apiSlice.endpoints.getRoomChatById.useLazyQuery();
  const [leaveRoom] = apiSlice.endpoints.leaveRoom.useMutation();

  // --- Load thông tin phòng ---
  useEffect(() => {
    if (!id) return;
    const fetchData = async () => {
      try {
        const roomRes = await getRoomChatById(id);
        if (roomRes.data) setRoomData(roomRes.data);
      } catch (err) {
        console.error("Error fetching room:", err);
      }
    };
    fetchData();
  }, [id]);

  // --- Kết nối socket ---
  useEffect(() => {
    if (!roomData?.room_chat_id) return;
    if (room_id !== roomData.room_chat_id) {
      dispatch(connectToSocket(roomData.room_chat_id));
    }

    return () => {
      dispatch(disconnectSocket());
      dispatch(resetGameState());
    };
  }, [roomData?.room_chat_id, dispatch]);

  // --- Gửi câu trả lời ---
  const handleSend = (msg: FastAnswerQuestion) => {
    dispatch(sendSocketMessage("submit_answer", msg));
  };

  // --- Bắt đầu game ---
  const handleStartGame = () => {
    if (room_id) {
      dispatch(sendSocketMessage("start_game", { room_id }));
    }
  };

  // --- Rời phòng ---
  const handleLeaveRoom = async () => {
    try {
      dispatch(disconnectSocket());
      if (user && roomData) {
        await leaveRoom({
          room_chat_id: roomData.room_chat_id,
          user_id: user.id,
        });
      }
      dispatch(clearRoomData());
      navigate("/quiz_room");
    } catch (err) {
      console.error("❌ Error leaving room:", err);
    }
  };

  // --- Render game content dựa vào Redux state ---
  const renderGameContent = () => {
    console.log(gameStatus)
    switch (gameStatus) {
      case "countdown":
        return (
          <div className="flex items-center justify-center h-full text-center">
            <h1 className="text-6xl font-bold">
              Bắt đầu sau: {countdownTime}
            </h1>
          </div>
        );

      case "started":
        if (!currentQuestion)
          return (
            <div className="flex items-center justify-center h-full text-center">
              <h2 className="text-2xl font-semibold">Đang tải câu hỏi...</h2>
            </div>
          );
        return (
          <div className="flex flex-col h-full bg-gray-50">
            {/* Phần câu hỏi */}
            <div className="flex-1 overflow-auto p-4">
              <QuizBox
                question={currentQuestion}
                currentIndex={questionIndex}
                totalQuestions={totalQuestions}
              />
            </div>

            {/* Phần trả lời cố định ở dưới */}
            <div className="border-t bg-white p-3 shadow-md">
              <AnswerQuestionBox
                onSend={handleSend}
                room_data={roomData}
                currentQuestion={currentQuestion}
              />
            </div>
          </div>
        );

      case "finished":
        return (
          <div className="flex flex-col items-center justify-center h-full text-center relative overflow-hidden">
            <h1 className="text-4xl font-bold mb-4 text-green-600">
              🎉 Trò chơi đã kết thúc!
            </h1>
            <h2 className="text-2xl mb-6">Bảng xếp hạng:</h2>
            <div className="w-96 bg-white rounded-xl shadow-lg p-6 max-h-[40vh] overflow-y-auto">
              {players
                // Sắp xếp người chơi theo điểm giảm dần
                .slice()
                .sort((a, b) => ((b.user_statistic?.score ?? 0) + (b.room_score ?? 0)) - ((a.user_statistic?.score ?? 0) + (a.room_score ?? 0)))
                .map((p, index) => (
                <div
                  key={p.id}
                  className="flex justify-between items-center py-2 border-b last:border-none"
                >
                  <div className="flex items-center gap-2">
                    {index === 0 && <span className="text-yellow-500 text-xl">🥇</span>}
                    {index === 1 && <span className="text-gray-400 text-xl">🥈</span>}
                    {index === 2 && <span className="text-orange-400 text-xl">🥉</span>}
                    <span className="font-medium text-lg">
                       {p.user_role.user_role_name !== "admin" ? p.user_info.name : p.user_role.user_role_name}
                    </span>
                  </div>
                  <span className="font-bold text-blue-600 text-lg">
                    {(p.user_role.user_role_name !== "admin" ? p.user_statistic.score ?? 0 : 0) + (p.room_score ?? 0)} pts
                  </span>
                </div>
              ))}
            </div>

            <div className="mt-8 flex gap-4">
              {/* [MỚI] Nút xem đáp án */}
              <Button
                onClick={() => setShowResultBoard(true)}
                className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-lg text-lg shadow-md transition-transform transform hover:scale-105"
              >
                📜 Xem đáp án
              </Button>

              <Button
                onClick={handleLeaveRoom}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg text-lg shadow-md transition-transform transform hover:scale-105"
              >
                🚪 Rời phòng
              </Button>
            </div>

            {/* [MỚI] Popup/Modal hiển thị danh sách câu hỏi và đáp án */}
            {showResultBoard && (
              <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                <div className="bg-white w-full max-w-3xl h-[80vh] rounded-2xl shadow-2xl flex flex-col animate-fadeIn">
                  <div className="flex justify-between items-center p-4 border-b">
                    <h3 className="text-2xl font-bold text-gray-800">REVIEW CÂU HỎI VÀ ĐÁP ÁN</h3>
                    <button 
                      onClick={() => setShowResultBoard(false)}
                      className="text-gray-500 hover:text-red-500 text-3xl font-bold leading-none"
                    >
                      &times;
                    </button>
                  </div>
                  
                  <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
                    {questions && questions.length > 0 ? (
                      questions.map((q, idx) => (
                        <div key={q.id || idx} className="bg-white p-4 mb-4 rounded-lg shadow border border-gray-200 text-left">
                          <div className="flex justify-between items-start mb-2">
                            <span className="font-bold text-gray-500">Câu {idx + 1}</span>
                            <span className="text-xs font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded">
                              {q.score} điểm
                            </span>
                          </div>
                          <p className="text-lg font-medium text-gray-800 mb-3">{q.question_text}</p>
                          <div className="p-3 bg-green-50 border-l-4 border-green-500 rounded-r">
                            <span className="font-semibold text-green-700">Đáp án đúng: </span>
                            <span className="text-gray-800">{q.answer}</span>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-center text-gray-500 mt-10">Không có dữ liệu câu hỏi.</p>
                    )}
                  </div>

                  <div className="p-4 border-t bg-gray-100 rounded-b-2xl text-right">
                    <Button 
                      onClick={() => setShowResultBoard(false)}
                      className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2"
                    >
                      Đóng
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      case "idle":

      default:
        const isLeader = players.length > 0 && players[0].id === user?.id;
        return (
          <div className="flex flex-col items-center justify-center h-full text-center p-5">
            <h1 className="text-3xl font-bold mb-4">Đang chờ người chơi...</h1>
            <p className="text-gray-600 mb-8">
              Game sẽ bắt đầu khi chủ phòng nhấn "Bắt đầu".
            </p>
            {isLeader ? (
              <Button
                onClick={handleStartGame}
                className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg text-lg"
              >
                Bắt đầu
              </Button>
            ) : (
              <p className="text-lg font-semibold">
                Chỉ người đầu tiên trong phòng có thể bắt đầu.
              </p>
            )}
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <div className="flex-1 flex flex-col border-r border-gray-200 relative">
        <div className="flex justify-between items-center p-4 border-b bg-white">
          <h2 className="text-lg font-semibold">
            {roomData?.room_name ?? "Quiz Room"}
          </h2>
          <Button
            onClick={handleLeaveRoom}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md"
          >
            Thoát phòng
          </Button>
        </div>

        {renderGameContent()}
      </div>
        <PlayerBox
          players={players}
          playersScore={players.map((p) => ({
            user_id: p.id,
            score: p.room_score ?? 0,
          }))}
        />
    </div>
  );
};

export default QuizRoomPage;