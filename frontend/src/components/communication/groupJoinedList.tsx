import { ChevronDown, ChevronRight, PlusCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { useState } from "react";
import CreateRoomModal from "./createRoomModal";
import type { UserRoom } from "../../types/userRoom";

// Component con để hiển thị từng danh sách phòng theo loại
interface RoomCategoryListProps {
  title: string;
  rooms: UserRoom[];
}

const RoomCategoryList = ({ title, rooms }: RoomCategoryListProps) => {
  const [open, setOpen] = useState(true); // Mặc định mở
  
  const isType1 = title.includes("Loại 1"); 
  const linkPaddingClass = isType1 ? "pl-4" : "pl-8"; // Tùy chỉnh padding

  return (
    <div>
      {/* Header droplist */}
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="w-full flex justify-between items-center py-2 px-4 hover:bg-blue-500 rounded"
      >
        <span className="font-semibold">{title}</span>
        {open ? (
          <ChevronDown className="w-4 h-4" />
        ) : (
          <ChevronRight className="w-4 h-4" />
        )}
      </button>

      {/* Danh sách phòng */}
      <ul
        className={`transition-all duration-300 overflow-scroll custom-scrollbar ${
          open ? "max-h-64 opacity-100 mt-1" : "max-h-0 opacity-0"
        }`}
      >
        {rooms.length > 0 ? (
          rooms.map((room) => (
            <li key={room.room_chat_id}>
              <Link
                to={room.room_chats.room_type_id != 3 ? `/communication/${room.room_chat_id}` : `/quiz_room/${room.room_chat_id}`}
                className={`block py-1.5 ${linkPaddingClass} pr-4 text-sm hover:bg-blue-500 rounded truncate`}
                title={room.room_chats.room_name}
              >
                {room.room_chats.room_name}
              </Link>
            </li>
          ))
        ) : (
          <li className="pl-4 pr-4 py-1.5 text-sm text-blue-100">
            Không có phòng nào
          </li>
        )}
      </ul>
    </div>
  );
};


// Component chính GroupJoinedList (Đã sửa đổi)
interface GroupJoinedListProps {
  rooms: UserRoom[];
  onCreateRoomSuccess: () => void
}

const GroupJoinedList = ({ rooms, onCreateRoomSuccess }: GroupJoinedListProps) => {
  const [showCreateRoomModal, setShowCreateRoomModal] = useState(false);

  const roomsType1 = rooms.filter(r => r.room_chats.room_type_id === 1);
  const roomsType2 = rooms.filter(r => r.room_chats.room_type_id === 2);
  const roomsType3 = rooms.filter(r => r.room_chats.room_type_id === 3);
  return (
    <div className="space-y-2">
      
      {/* 2. DROPLIST DÀNH CHO LOẠI 1 (Phòng Cá nhân/Trực tiếp) */}
      <RoomCategoryList 
        title="Phòng chung" 
        rooms={roomsType1} 
      />

      {/* 3. DROPLIST DÀNH CHO LOẠI 2 & 3 (Phòng Nhóm/Chơi game) */}
      <RoomCategoryList 
        title="Phòng riêng" 
        rooms={roomsType2} 
      />
      <RoomCategoryList 
        title="Phòng chơi"
        rooms={roomsType3}
      />

      {/* NÚT TẠO PHÒNG (Được đưa ra ngoài) */}
      <li className="list-none pt-2">
        <button
          onClick={() => setShowCreateRoomModal(true)}
          className="flex items-center gap-2 text-sm pl-4 pr-4 py-1.5 text-white bg-blue-500 hover:bg-blue-600 rounded w-full font-medium"
        >
          <PlusCircle className="w-4 h-4" />
          Tạo phòng Mới
        </button>
      </li>

      {/* Create Room Modal */}
      {showCreateRoomModal && (
        <CreateRoomModal 
          onClose={() => setShowCreateRoomModal(false)}   
          onSuccess={() => {
            onCreateRoomSuccess() 
          }}/>
      )}
    </div>
  );
};

export default GroupJoinedList;