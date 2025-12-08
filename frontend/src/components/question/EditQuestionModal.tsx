import { useState } from "react"
import { X } from "lucide-react"
import type { Question } from "../../types/questions"
import apiSlice from "../../store/apiSlice"

interface EditQuestionModalProps {
  question: Question
  onClose: () => void
}

const EditQuestionModal: React.FC<EditQuestionModalProps> = ({ question, onClose }) => {
  const [text, setText] = useState(question.question_text)
  const [answer, setAnswer] = useState(question.answer || "")
  const [score, setScore] = useState(question.score)
  const [updateQuestion] = apiSlice.endpoints.updateQuestion.useMutation()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const updated = {
      ...question,
      question_text: text,
      answer,
      score,
    }
    await updateQuestion({
        payload: updated,
        id: question.id
    })

    onClose()
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-50">
      <div className="bg-white rounded-lg shadow-lg w-96 p-6 relative">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Chỉnh sửa câu hỏi</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Câu hỏi</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={3}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Đáp án</label>
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Điểm</label>
            <input
              type="number"
              min={0}
              value={score}
              onChange={(e) => setScore(Number(e.target.value))}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
            />
          </div>

          <div className="flex justify-end gap-2 mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm border rounded hover:bg-gray-100">
              Trở về
            </button>
            <button type="submit" className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700">
              Lưu
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditQuestionModal
