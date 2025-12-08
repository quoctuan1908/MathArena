import { useState } from "react"
import { X } from "lucide-react"
import apiSlice from "../../store/apiSlice"
import type { RoomChatCreate } from "../../types/roomchat"
import { useSelector } from "react-redux"
import type { RootState } from "../../store/store"
import ReactDOM from "react-dom";

type CreateRoomModalProps = {
  onClose: () => void,
  onSuccess: () => void
}

const CreateRoomModal: React.FC<CreateRoomModalProps> = ({ onClose, onSuccess }) => {
  const [roomName, setRoomName] = useState("")
  const [roomCapacity, setRoomCapacity] = useState(1)
  const [roomPassword, setRoomPassword] = useState("")
  const [roomTypeId, setRoomTypeId] = useState<number | "">("")

  const { data: roomTypes = [], isLoading } = apiSlice.endpoints.getRoomChatTypes.useQuery()
  const [createRoomChat] = apiSlice.endpoints.createRoomChat.useMutation()
  const user = useSelector((state: RootState) => state.auth.user);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!roomTypeId) {
      alert("Vui lòng chọn loại phòng")
      return
    }

    if(!user) {
      alert("Vui lòng đăng nhập trước khi tạo phòng.")
      return
    }

    const payload: RoomChatCreate = {
      room_name: roomName,
      room_capacity: Number(roomCapacity),
      room_password: roomPassword || null,
      room_type_id: Number(roomTypeId),
      host_id: user?.id
    }

    try {
      const res = await createRoomChat(payload).unwrap()
      console.log("Room created:", res)
      alert("Tạo phòng thành công 🎉")
      onSuccess()
      onClose()
    } catch (error: any) {
      console.error("Error creating room:", error)
      alert(error?.data?.detail || "Không thể tạo phòng, vui lòng thử lại")
    }
    onClose()
  }

  const modal = (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40 z-[9999]">
      <div className="bg-white rounded-lg shadow-lg w-96 p-6 relative">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Tạo phòng</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          {/* Room Name */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Tên phòng</label>
            <input
              type="text"
              value={roomName}
              onChange={(e) => setRoomName(e.target.value)}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
              required
            />
          </div>

          {/* Capacity */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Sức chứa</label>
            <input
              type="number"
              min={1}
              max={50}
              value={roomCapacity}
              onChange={(e) => setRoomCapacity(Number(e.target.value))}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
              required
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Mật khẩu (optional)</label>
            <input
              type="password"
              value={roomPassword}
              onChange={(e) => setRoomPassword(e.target.value)}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
            />
          </div>

          {/* Room Type */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Loại phòng</label>
            <select
              value={roomTypeId}
              onChange={(e) => setRoomTypeId(e.target.value ? Number(e.target.value) : "")}
              className="w-full border rounded-md px-3 py-2 text-sm focus:ring focus:ring-blue-200 outline-none"
              required
              disabled={isLoading}
            >
              <option value="">-- Chọn loại phòng --</option>
              {roomTypes.map((type: any) => (
                <option key={type.room_type_id} value={type.room_type_id}>
                  {type.room_type_name}
                </option>
              ))}
            </select>
          </div>

          {/* Buttons */}
          <div className="flex justify-end gap-2 mt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm border rounded hover:bg-gray-100"
            >
              Hủy
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Tạo phòng
            </button>
          </div>
        </form>
      </div>
    </div>
  )

  return ReactDOM.createPortal(modal, document.body);
}

export default CreateRoomModal
