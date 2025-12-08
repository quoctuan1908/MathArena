import { useState } from "react"
import { X, Info, AlertCircle } from "lucide-react" // Đã thêm icon Info và AlertCircle
import AddQuestionManuallyForm from "./AddQuestionManuallyForm"
import AddQuestionWithAI from "./AddQuestionWithAI"

interface CreateQuestionModalProps {
  onClose: () => void
  creatorId: string
}

const CreateQuestionModal: React.FC<CreateQuestionModalProps> = ({ onClose, creatorId }) => {
  const [mode, setMode] = useState<"choose" | "manual" | "ai" | "import">("choose")

  const renderContent = () => {
    switch (mode) {
      case "manual":
        return <AddQuestionManuallyForm onBack={() => setMode("choose")} onClose={onClose} creatorId={creatorId} />
      case "ai":
        return <AddQuestionWithAI onBack={() => setMode("choose")} onClose={onClose} creatorId={creatorId} />
      default:
        return (
          <div className="space-y-6">
            {/* Phần chọn chế độ */}
            <div>
              <p className="mb-4 text-sm text-gray-600">Chọn kiểu thêm câu hỏi:</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setMode("manual")}
                  className="p-4 border rounded-lg hover:shadow-md hover:border-blue-400 transition-all text-left bg-white"
                >
                  <div className="font-semibold text-blue-600">Thủ công</div>
                  <div className="text-xs text-gray-500 mt-1">Điền vào form mẫu có sẵn</div>
                </button>
                <button
                  onClick={() => setMode("ai")}
                  className="p-4 border rounded-lg hover:shadow-md hover:border-purple-400 transition-all text-left bg-white"
                >
                  <div className="font-semibold text-purple-600">Tạo câu hỏi bằng AI</div>
                  <div className="text-xs text-gray-500 mt-1">Tự động sinh câu hỏi thông minh</div>
                </button>
              </div>
            </div>

            {/* Phần hướng dẫn sử dụng cú pháp toán học */}
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-sm">
              <div className="flex items-center gap-2 mb-3 text-gray-800 font-semibold border-b pb-2">
                <Info className="w-4 h-4" />
                <h3>Hướng dẫn cú pháp toán học</h3>
              </div>

              {/* Danh sách các phép toán */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-2 mb-4 text-gray-700">
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">add</code> <span>Cộng</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">subtract</code> <span>Trừ</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">multiply</code> <span>Nhân</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">divide</code> <span>Chia</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">min</code> <span>Nhỏ nhất</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">max</code> <span>Lớn nhất</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">lcm</code> <span>BCNN</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">sqrt</code> <span>Căn bậc 2</span>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-1">
                  <code className="text-blue-600 font-bold">negate</code> <span>Số đối</span>
                </div>
              </div>

              {/* Các lưu ý quan trọng */}
              <div className="bg-yellow-50 border border-yellow-200 rounded p-3 text-xs text-yellow-800 space-y-2">
                <div className="flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                  <div>
                    <strong>Lưu ý về hằng số:</strong>
                    <p className="mt-1">
                      Các số nằm trong hàm phải có tiền tố <code className="bg-yellow-100 px-1 rounded font-bold">const_</code>.
                      <br />
                      <span className="opacity-80">Ví dụ: <code>add(const_5, const_10)</code></span>
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start gap-2">
                   <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                   <div>
                    <strong>Lưu ý về phép tính:</strong>
                    <p className="mt-1">
                      Đối với phép <strong>Trừ (subtract)</strong> và <strong>Chia (divide)</strong>: 
                      Số bị trừ/chia nên lớn hơn số trừ/chia để đảm bảo kết quả hợp lệ trong ngữ cảnh bài toán.
                    </p>
                   </div>
                </div>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-50 p-4 animate-in fade-in duration-200">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto relative flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b sticky top-0 bg-white z-10">
          <h2 className="text-xl font-bold text-gray-800">Thêm câu hỏi mới</h2>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6">
          {renderContent()}
        </div>
      </div>
    </div>
  )
}

export default CreateQuestionModal