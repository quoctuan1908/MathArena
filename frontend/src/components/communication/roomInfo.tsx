import { useEffect, useState } from "react"

type RoomInfoProps = {
  room_data?: {
    room_chat_id: string
    room_name?: string
    member_count?: number
    description?: string
  }
}

const RoomInfo = ({ room_data }: RoomInfoProps) => {
  const [memberCount, setMemberCount] = useState<number>(room_data?.member_count || 0)

  // Nếu bạn có WebSocket gửi event khi người ra/vào phòng
  useEffect(() => {
    // Giả sử socket gửi event "update_member_count"
    const handleMemberUpdate = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        if (data.event === "update_member_count") {
          setMemberCount(data.payload.count)
        }
      } catch (err) {
        console.error("Invalid event:", err)
      }
    }

    window.addEventListener("message", handleMemberUpdate)
    return () => window.removeEventListener("message", handleMemberUpdate)
  }, [])

  if (!room_data) return null

  return (
    <div className="bg-gray-100 border-b border-gray-300 p-4 flex justify-between items-center">
      <div>
        <h2 className="text-lg font-semibold">{room_data.room_name || "Phòng Chat"}</h2>
        {room_data.description && (
          <p className="text-sm text-gray-600">{room_data.description}</p>
        )}
      </div>
      <div className="text-sm text-gray-700">
        👥 {memberCount} người trong phòng
      </div>
    </div>
  )
}

export default RoomInfo
