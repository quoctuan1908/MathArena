import { useDispatch, useSelector } from "react-redux"
import { Link, useNavigate } from "react-router-dom"
import type { RootState } from "../store/store"
import { logout } from "../store/authSlice"
import GroupJoinedList from "./communication/groupJoinedList"
import { useEffect, useState } from "react"
import apiSlice from "../store/apiSlice"
import type { UserRoom } from "../types/userRoom"
import { LogOut, LogIn, Home, MessageCircle, Settings, Menu, Search } from "lucide-react"


export const Header = () => {
  const dispatch = useDispatch()
  const token = useSelector((state: RootState) => state.auth.token)
  const user = useSelector((state: RootState) => state.auth.user)
  const [getUserRoomByUserId] = apiSlice.endpoints.getUserRoomByUserId.useLazyQuery()
  const [joinedRooms, setJoinedRooms] = useState<UserRoom[]>([])
  const roomChanged = useSelector((state: RootState) => state.socket.inRoom)
  const [sidebarOpen, setSidebarOpen] = useState(false) // state toggle sidebar trên mobile
  const [searchRoomId, setSearchRoomId] = useState("");
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout())
  }

  const fetchJoinedRooms = async () => {
    if (user) {
      const result = await getUserRoomByUserId(user.id)
      if (result?.data) {
        setJoinedRooms(result.data)
      }
    }
  }

  
  const handleGoToRoom = () => {
    if (searchRoomId.trim()) {
      navigate(`/communication/${searchRoomId.trim()}`);
      setSidebarOpen(false); // đóng sidebar nếu trên mobile
    }
  };

  useEffect(() => {
    fetchJoinedRooms()
  }, [user, roomChanged])

  return (
    <>
      <button
        className="md:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-blue-600 text-white shadow"
        onClick={() => setSidebarOpen(true)}
      >
        <Menu className="w-5 h-5" />
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-screen w-full bg-gradient-to-b from-blue-600 to-blue-700 text-white flex flex-col shadow-xl
          transform transition-transform duration-300 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} 
          md:translate-x-0 md:static md:flex
          z-40
        `}
      >
        {/* Logo / Header */}
        <div className="px-5 py-4 border-b border-blue-500 flex justify-between items-center">
          <div>
            <h1 className="text-lg font-semibold tracking-wide">🧩 Quiz Platform</h1>
            {user && (
              <p className="text-sm text-blue-100 mt-1 truncate">Hi, {user.username}</p>
            )}
          </div>
          {/* Close button cho mobile */}
          <button
            className="md:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            ✕
          </button>
        </div>

        {/* Navigation */}
        <ul className="flex-1 overflow-y-auto space-y-1 text-sm">
          <li>
            <Link
              to="/"
              className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-blue-500 transition"
            >
              <Home className="w-4 h-4" />
              Trang chủ
            </Link>
          </li>

          <li>
            <Link
              to="/quiz_room"
              className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-blue-500 transition"
            >
              <MessageCircle className="w-4 h-4" />
              Phòng chơi
            </Link>
          </li>

          {user?.user_role.user_role_name === "admin" && (
            <li>
              <Link
                to="/questions"
                className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-blue-500 transition"
              >
                <Settings className="w-4 h-4" />
                Quản lý Câu hỏi
              </Link>
            </li>
          )}

          {/* Danh sách phòng đã tham gia */}
          <div className="mt-4">
            <p className="text-xs uppercase text-blue-200 font-semibold mb-2">
              Phòng đã tham gia
            </p>
            <GroupJoinedList
              rooms={joinedRooms}
              onCreateRoomSuccess={fetchJoinedRooms}
            />
          </div>
          <div className="mt-4">
            <label className="text-xs text-blue-200 font-semibold mb-1 block">
              TÌM PHÒNG BẰNG ID
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Nhập Room ID..."
                value={searchRoomId}
                onChange={(e) => setSearchRoomId(e.target.value)}
                className="flex-1 px-2 py-1 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-blue-400 placeholder:text-white"
              />
              <button
                onClick={handleGoToRoom}
                className="px-2 py-1 bg-blue-500 hover:bg-blue-600 rounded-md text-white text-sm"
              >
              <Search className="w-5 h-5 text-white" />
              </button>
            </div>
          </div>
        </ul>

        {/* Auth section */}
        <div className="border-t border-blue-500 px-3 py-3">
          {token ? (
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center gap-2 py-2 bg-blue-500 hover:bg-blue-600 rounded-md text-sm font-medium transition"
            >
              <LogOut className="w-4 h-4" />
              Đăng xuất
            </button>
          ) : (
            <Link
              to="/login"
              className="w-full flex items-center justify-center gap-2 py-2 bg-blue-500 hover:bg-blue-600 rounded-md text-sm font-medium transition"
            >
              <LogIn className="w-4 h-4" />
              Đăng nhập
            </Link>
          )}
        </div>
      </aside>

      {/* Overlay để click ngoài đóng sidebar trên mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
    </>
  )
}
