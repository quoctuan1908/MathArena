import { useState } from "react"
import apiSlice from "../../store/apiSlice"

interface AddQuestionManuallyFormProps {
  onBack: () => void
  onClose: () => void
  creatorId: string
}

const AddQuestionManuallyForm: React.FC<AddQuestionManuallyFormProps> = ({ onBack, onClose, creatorId }) => {
  const [questionText, setQuestionText] = useState("")
  const [answer, setAnswer] = useState("")
  const [score, setScore] = useState(0)
  const [subjectId, setSubjectId] = useState<number | "">("")
  const [questionTypeId, setQuestionTypeId] = useState<number | "">("")

  const { data: subjects = [] } = apiSlice.endpoints.getSubjects.useQuery()
  const { data: questionTypes = [] } = apiSlice.endpoints.getQuestionTypes.useQuery()
  const [createQuestion, { isLoading }] = apiSlice.endpoints.createQuestion.useMutation()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await createQuestion({
      question_text: questionText,
      answer,
      score,
      subject_id: Number(subjectId),
      question_type_id: Number(questionTypeId),
      creator_id: creatorId,
    })
    onClose()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Câu hỏi</label>
        <textarea
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          className="w-full border rounded-md px-3 py-2 text-sm"
          rows={3}
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Đáp án</label>
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="w-full border rounded-md px-3 py-2 text-sm"
        />
      </div>

      <div className="flex gap-3">
        <div className="flex-1">
          <label className="block text-sm font-medium mb-1">Điểm</label>
          <input
            type="number"
            value={score}
            onChange={(e) => setScore(Number(e.target.value))}
            className="w-full border rounded-md px-3 py-2 text-sm"
          />
        </div>
        <div className="flex-1">
          <label className="block text-sm font-medium mb-1">Môn</label>
          <select
            value={subjectId}
            onChange={(e) => setSubjectId(Number(e.target.value))}
            className="w-full border rounded-md px-3 py-2 text-sm"
          >
            <option value="">Chọn môn</option>
            {subjects.map((s: any) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex-1">
          <label className="block text-sm font-medium mb-1">Loại câu</label>
          <select
            value={questionTypeId}
            onChange={(e) => setQuestionTypeId(Number(e.target.value))}
            className="w-full border rounded-md px-3 py-2 text-sm"
          >
            <option value="">Chọn loại</option>
            {questionTypes.map((t: any) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex justify-end gap-2">
        <button
          type="button"
          onClick={onBack}
          className="px-3 py-2 border rounded text-sm"
        >
          Trờ về
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="px-3 py-2 bg-green-600 text-white rounded text-sm"
        >
          {isLoading ? "Đạng tạo..." : "Tạo câu hỏi"}
        </button>
      </div>
    </form>
  )
}

export default AddQuestionManuallyForm
