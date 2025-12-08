import { useState } from "react"
import apiSlice from "../../store/apiSlice"
import { computeAst } from "../../services/questionService"

interface AddQuestionWithAIProps {
  onBack: () => void
  onClose: () => void
  creatorId: string
}

const AddQuestionWithAI: React.FC<AddQuestionWithAIProps> = ({ onBack, onClose, creatorId }) => {
  const [inputText, setInputText] = useState("") // input AST hoặc numbers
  const [questionText, setQuestionText] = useState("") // câu hỏi sinh ra
  const [answer, setAnswer] = useState("")
  const [score, setScore] = useState(0)
  const [subjectId, setSubjectId] = useState<number | "">("")
  const [questionTypeId, setQuestionTypeId] = useState<number | "">("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [isCreating, setIsCreating] = useState(false)

  const { data: subjects = [] } = apiSlice.endpoints.getSubjects.useQuery()
  const { data: questionTypes = [] } = apiSlice.endpoints.getQuestionTypes.useQuery()
  const [generateQuestion] = apiSlice.endpoints.generateQuestion.useMutation()
  const [createQuestion] = apiSlice.endpoints.createQuestion.useMutation()

  // --- Gọi API để generate question ---
  const handleGenerateQuestion = async () => {
    if (!inputText) return;
    setIsGenerating(true);
    try {
      // 1️⃣ Gọi API sinh câu hỏi (có thể từ AST hoặc text input)
      const res = await generateQuestion({ text: inputText });
      if (res.data) {
        setQuestionText(res.data);
      }

      // 2️⃣ Tự động tính AST từ input và đưa vào field answer
      try {
        const ans = computeAst(inputText);
        if (ans !== null) setAnswer(ans.toString());
        else setAnswer(""); // nếu AST không hợp lệ
      } catch (err) {
        console.error("Lỗi tính AST:", err);
        setAnswer("");
      }
    } catch (err) {
      console.error("Lỗi generate question:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  // --- Tạo câu hỏi ---
  const handleCreate = async () => {
    if (!questionText) return
    setIsCreating(true)
    try {
      await createQuestion({
        question_text: questionText,
        answer,
        score,
        subject_id: Number(subjectId),
        question_type_id: Number(questionTypeId),
        creator_id: creatorId,
      })
      onClose()
    } catch (err) {
      console.error(err)
    } finally {
      setIsCreating(false)
    }
  }

  const generateRandomAst = () => {
    const ops = ["add", "subtract", "multiply", "divide", "min", "max", "lcm"];
    const randOp = ops[Math.floor(Math.random() * ops.length)];
    const a = Math.floor(Math.random() * 10) + 1;
    const b = Math.floor(Math.random() * 10) + 1;
    const ast = `${randOp}(const_${a},const_${b})`;
    setInputText(ast);

    // Tính luôn answer từ AST
    try {
      const ans = computeAst(ast);
      if (ans !== null) setAnswer(ans.toString());
      else setAnswer("");
    } catch {
      setAnswer("");
    }
  };


  return (
    <form className="space-y-4 p-4 max-w-xl mx-auto" onSubmit={(e) => e.preventDefault()}>
      {/* Input AST / Numbers */}
      <div>
        <label className="block text-sm font-medium mb-1">Input AST</label>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="E.g., add(const_2,const_3)"
          className="w-full border rounded-md px-3 py-2 text-sm"
        />
      </div>

      <button
        type="button"
        disabled={isGenerating}
        onClick={handleGenerateQuestion}
        className={`px-3 py-2 rounded text-white ${isGenerating ? "bg-gray-400" : "bg-blue-600"}`}
      >
        {isGenerating ? "Generating..." : "Sinh câu hỏi"}
      </button>
      <button
        type="button"
        onClick={generateRandomAst}
        className="px-3 py-2 bg-purple-600 text-white rounded-md text-sm"
      >
        Sinh ngẫu nhiên cây AST
      </button>
      {/* Generated Question */}
      <div>
        <label className="block text-sm font-medium mb-1">Câu hỏi</label>
        <textarea
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          rows={3}
          className="w-full border rounded-md px-3 py-2 text-sm"
        />
      </div>

      {/* Answer */}
      <div>
        <label className="block text-sm font-medium mb-1">Đáp án</label>
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="w-full border rounded-md px-3 py-2 text-sm"
        />
      </div>

      {/* Score / Subject / Type */}
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
            <option value="">Select subject</option>
            {subjects.map((s: any) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        <div className="flex-1">
          <label className="block text-sm font-medium mb-1">Loại</label>
          <select
            value={questionTypeId}
            onChange={(e) => setQuestionTypeId(Number(e.target.value))}
            className="w-full border rounded-md px-3 py-2 text-sm"
          >
            <option value="">Chọn loại</option>
            {questionTypes.map((t: any) => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex justify-end gap-2">
        <button
          type="button"
          onClick={onBack}
          className="px-3 py-2 border rounded text-sm"
        >
          Trở về
        </button>
        <button
          type="button"
          disabled={isCreating || !questionText}
          onClick={handleCreate}
          className={`px-3 py-2 rounded text-white ${isCreating ? "bg-gray-400" : "bg-green-600"}`}
        >
          {isCreating ? "Creating..." : "Tạo câu hỏi"}
        </button>
      </div>
    </form>
  )
}

export default AddQuestionWithAI
