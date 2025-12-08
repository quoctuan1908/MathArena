import { useEffect, useState } from "react";
import { Button } from "../Button";
import { Input } from "../Input";
import type { RoomChat } from "../../types/roomchat";
import { useSelector } from "react-redux";
import type { RootState } from "../../store/store";
import { useNavigate } from "react-router-dom";
import type { FastAnswerQuestion, Question } from "../../types/questions";

type AnswerQuestionBoxType = {
  onSend: (msg: FastAnswerQuestion) => void;
  room_data: RoomChat | null | undefined;
  currentQuestion: Question;
};

const AnswerQuestionBox: React.FC<AnswerQuestionBoxType> = ({
  onSend,
  room_data,
  currentQuestion,
}) => {
  const user = useSelector((state: RootState) => state.auth.user);
  const navigate = useNavigate();
  const [answer, setAnswer] = useState<string>("");

  useEffect(() => {
    setAnswer("");
  }, [room_data, user]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!user) return navigate("/login");
    if (!room_data?.room_chat_id) return;

    const msg: FastAnswerQuestion = {
      room_id: room_data.room_chat_id,
      user_id: user.id,
      answer: answer.trim(),
    };

    onSend(msg);

    // Gợi ý kiểm tra đáp án (chỉ hiển thị console, có thể hiển thị UI sau)
    if (currentQuestion.answer) {
      const isCorrect =
        currentQuestion.answer.toLowerCase() === answer.trim().toLowerCase();
      console.log(isCorrect ? "🎉 Correct answer!" : "❌ Wrong answer!");
    }

    setAnswer("");
  };

  return (
    <div className="w-full flex justify-center py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-t border-indigo-100">
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-3 bg-white shadow-md rounded-2xl p-4 border border-gray-200 max-w-2xl w-full transition-all hover:shadow-lg"
      >
        <Input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="💡 Nhập câu trả lời của bạn..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-3 text-base focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none transition-all"
        />

        <Button
          type="submit"
          className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold text-base hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-400 transition-all"
        >
          Gửi
        </Button>
      </form>
    </div>
  );
};

export default AnswerQuestionBox;
