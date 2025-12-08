import { type FC } from "react";
import type { RoomChat } from "../../types/roomchat";
import { Lock, Users, Puzzle } from "lucide-react";
import { useSelector } from "react-redux";
import type { RootState } from "../../store/store";
import { useNavigate } from "react-router-dom";

interface QuizRoomCardProps {
  quizRoom: RoomChat;
  currentCount?: number; // số người hiện tại (load từ API)
  onJoin?: (room_chat_id: string, user_id: string, user_room_role_id: string) => void;
}

const QuizRoomCard: FC<QuizRoomCardProps> = ({ quizRoom, currentCount, onJoin }) => {
  const user = useSelector((state: RootState) => state.auth.user);
  const navigate = useNavigate();

  return (
    <div
      onClick={() => {
        if (!user) {
          navigate("/login");
          return;
        }
        onJoin?.(quizRoom.room_chat_id, user.id, "2");
      }}
      className="group relative bg-white rounded-xl border border-gray-200 p-4 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 cursor-pointer"
    >
      <div className="flex justify-between items-center mb-2">
        <h2 className="font-semibold text-gray-800 text-sm truncate flex items-center gap-2">
          <Puzzle className="text-purple-500" size={18} />
          {quizRoom.room_name}
        </h2>
        {quizRoom.room_password && <Lock className="text-gray-400" size={16} />}
      </div>

      <div className="text-xs text-gray-600 space-y-1">
        <div className="flex items-center gap-1.5">
          <Users size={14} className="text-gray-500" />
          <span>
            <strong>{currentCount ?? 0}</strong> / {quizRoom.room_capacity ?? "∞"} người
          </span>
        </div>
        {quizRoom.room_type && (
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded-md text-[11px] font-medium">
              {quizRoom.room_type.room_type_name}
            </span>
          </div>
        )}
      </div>

      <div className="absolute inset-0 rounded-xl bg-purple-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
        <button className="bg-purple-600 text-white font-medium px-3 py-1.5 rounded-lg shadow hover:bg-purple-700 transition text-sm">
          Tham gia
        </button>
      </div>
    </div>
  );
};

export default QuizRoomCard;
