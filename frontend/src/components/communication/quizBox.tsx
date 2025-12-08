import React from "react";
import type { Question } from "../../types/questions";

interface QuizBoxProps {
  question: Question;
  currentIndex?: number;
  totalQuestions?: number;
}

const QuizBox: React.FC<QuizBoxProps> = ({ question, currentIndex, totalQuestions }) => {
  return (
    <div className="flex flex-col items-center justify-center flex-1 p-8 bg-gradient-to-br from-blue-50 to-indigo-100 h-full">
      <div className="max-w-3xl w-full bg-white shadow-2xl rounded-2xl p-10 border border-indigo-100 transform transition-all duration-300 hover:scale-[1.02]">
        <h2 className="text-3xl font-extrabold text-indigo-700 mb-6 text-center tracking-tight">
          🧩 Câu hỏi hiện tại {currentIndex}/{totalQuestions}
        </h2>
        <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-8 rounded-xl text-center">
          <p className="text-2xl font-semibold text-gray-800 leading-relaxed">
            {question.question_text}
          </p>
        </div>
      </div>
    </div>
  );
};

export default QuizBox;
