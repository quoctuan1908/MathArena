import { useState } from "react"
import apiSlice from "../store/apiSlice"
import type { Question } from "../types/questions"
import EditQuestionModal from "../components/question/EditQuestionModal"
import CreateQuestionModal from "../components/question/CreateQuestionModal"



const AddQuestionsPage = () => {
  const user = JSON.parse(localStorage.getItem("user") || "{}")
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)

  const [page, setPage] = useState(0)
  const limit = 10

  const { data, isLoading, refetch } = apiSlice.endpoints.getQuestionsByCreatorId.useQuery(
    { creatorId: user?.id ?? "", page, limit },
    { skip: !user?.id }
  )

  const questions = data?.items ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / limit)

  const handleEdit = (question: Question) => {
    setSelectedQuestion(question)
    setIsEditModalOpen(true)
  }

  const handleAdd = () => {
    setIsAddModalOpen(true)
  }
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Quản lý câu hỏi</h1>
        <button
          onClick={handleAdd}
          className="px-4 py-2 bg-green-600 text-white text-sm rounded hover:bg-green-700"
        >
          + Thêm câu hỏi
        </button>
      </div>

      {isLoading ? (
        <p>Loading questions...</p>
      ) : questions.length === 0 ? (
        <div className="text-center text-gray-500 mt-10">
          No questions found. Try adding a new one.
        </div>
      ) : (
        <>
          <table className="w-full border border-gray-200 rounded-lg overflow-hidden shadow-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-3 py-2 text-left">Câu hỏi</th>
                <th className="border px-3 py-2 text-left">Điểm</th>
                <th className="border px-3 py-2 text-left">Môn</th>
                <th className="border px-3 py-2 text-left">Loại</th>
                <th className="border px-3 py-2 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {questions.map((q) => (
                <tr key={q.id} className="hover:bg-gray-50">
                  <td className="border px-3 py-2">{q.question_text}</td>
                  <td className="border px-3 py-2">{q.score}</td>
                  <td className="border px-3 py-2">{q.subject?.name}</td>
                  <td className="border px-3 py-2">{q.question_type?.name}</td>
                  <td className="border px-3 py-2 text-center">
                    <button
                      onClick={() => handleEdit(q)}
                      className="text-blue-600 hover:underline"
                    >
                      Chỉnh sửa
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-4">
            <p className="text-sm text-gray-600">
              Trang {page + 1} / {totalPages || 1} | Tổng {total} câu hỏi
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setPage((p) => Math.max(p - 1, 0))}
                disabled={page === 0}
                className={`px-3 py-1 border rounded ${
                  page === 0
                    ? "text-gray-400 border-gray-200 cursor-not-allowed"
                    : "hover:bg-gray-100"
                }`}
              >
                Trước
              </button>
              <button
                onClick={() => setPage((p) => Math.min(p + 1, totalPages - 1))}
                disabled={page >= totalPages - 1 || totalPages === 0}
                className={`px-3 py-1 border rounded ${
                  page >= totalPages - 1 || totalPages === 0
                    ? "text-gray-400 border-gray-200 cursor-not-allowed"
                    : "hover:bg-gray-100"
                }`}
              >
                Tiếp
              </button>
            </div>
          </div>
        </>
      )}

      {/* Edit Modal */}
      {isEditModalOpen && selectedQuestion && (
        <EditQuestionModal
          question={selectedQuestion}
          onClose={() => {
            setIsEditModalOpen(false)
            refetch()
          }}
        />
      )}

      {/* Add Modal */}
      {isAddModalOpen && (
        <CreateQuestionModal
          onClose={() => {
            setIsAddModalOpen(false)
            refetch()
          }}
          creatorId={user.id}
        />
      )}
    </div>
  )
}

export default AddQuestionsPage
