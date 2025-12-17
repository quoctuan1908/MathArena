import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "../store/store";
import { Button } from "../components/Button";
import { apiSlice } from "../store/apiSlice";
import { Star, TrendingUp, Layers } from "lucide-react";

const HomePage = () => {
  const user = useSelector((state: RootState) => state.auth.user);
  console.log(import.meta.env.VITE_SOCKET_URL)
  const { data: systemStats } = apiSlice.endpoints.getSystemStats.useQuery(undefined, {
    skip: !user || user.user_role.user_role_name !== "admin",
  });

  const { data: userStats } = apiSlice.endpoints.getUserStats.useQuery(user?.id!, {
    skip: !user || user.user_role.user_role_name === "admin",
  });

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
        <h1 className="text-2xl font-bold mb-4">Chào mừng bạn đến hệ thống trò chơi giải toán</h1>
        <Button type="button">
          <Link to="/login">Đăng nhập</Link>
        </Button>
      </div>
    );
  }

  // ✅ ADMIN VIEW (giữ nguyên)
  if (user.user_role.user_role_name === "admin") {
    return (
      <div className="min-h-screen bg-gray-100 p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-6 text-yellow-600 flex items-center gap-2">
            👑 Dashboard Admin
          </h1>
          <p className="text-gray-600 mb-8 text-center md:text-left">
            Quản lý người dùng, câu hỏi và theo dõi thống kê hệ thống.
          </p>

          {systemStats ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              <StatCard
                icon={<Star className="text-yellow-500 w-6 h-6" />}
                label="Tổng người dùng"
                value={systemStats.total_users}
                bgColor="bg-yellow-50"
              />
              <StatCard
                icon={<Layers className="text-blue-500 w-6 h-6" />}
                label="Tổng phòng quiz"
                value={systemStats.total_rooms}
                bgColor="bg-blue-50"
              />
              <StatCard
                icon={<TrendingUp className="text-green-500 w-6 h-6" />}
                label="Tổng tin nhắn"
                value={systemStats.total_messages}
                bgColor="bg-green-50"
              />
              <StatCard
                icon={<Star className="text-purple-500 w-6 h-6" />}
                label="Tổng câu hỏi"
                value={systemStats.total_questions}
                bgColor="bg-purple-50"
              />
              <StatCard
                icon={<Layers className="text-pink-500 w-6 h-6" />}
                label="Trung bình người dùng/phòng"
                value={systemStats.average_users_per_room}
                bgColor="bg-pink-50"
              />
              <StatCard
                icon={<TrendingUp className="text-indigo-500 w-6 h-6" />}
                label="Điểm trung bình mỗi người"
                value={systemStats.average_user_score}
                bgColor="bg-indigo-50"
              />
            </div>
          ) : (
            <p className="text-gray-500 text-center">Đang tải thống kê...</p>
          )}
        </div>
      </div>
    );
  }

  // ✅ USER VIEW — Trang bảng cá nhân đẹp hơn
  const level = userStats?.level ?? "Chưa có";
  const score = userStats?.total_score ?? 0;
  const nextLevelScore = Math.floor(score / 200 + 1) * 200;
  const progress = Math.min((score % 200) / 2, 100); // % tiến trình đến level kế

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-3xl relative">
        <div className="absolute top-4 right-4 text-sm text-gray-500">
          Thành viên từ {new Date(user.created_at).toLocaleDateString()}
        </div>

        <div className="flex flex-col items-center text-center mb-8">
          <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-4xl font-bold text-blue-600 mb-3 shadow-inner">
            {user.user_info.name.charAt(0).toUpperCase()}
          </div>
          <h1 className="text-2xl font-bold text-gray-800">{user.user_info.name}</h1>
          <p className="text-gray-500">{user.user_info.email}</p>
          <span className="mt-2 inline-block bg-blue-100 text-blue-700 text-sm px-3 py-1 rounded-full">
            {user.user_role.user_role_name}
          </span>
        </div>

        {userStats ? (
          <>
            {/* Thanh tiến trình Level */}
            <div className="mb-8">
              <div className="flex justify-between mb-1">
                <span className="font-semibold text-gray-700">
                  🌟 Cấp độ: {level}
                </span>
                <span className="text-sm text-gray-500">
                  {score}/{nextLevelScore} điểm
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-blue-500 to-indigo-500 h-3 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {/* Thống kê */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              <StatCard
                icon={<Star className="text-yellow-500" />}
                label="Điểm hiện tại"
                value={score}
              />
              <StatCard
                icon={<TrendingUp className="text-green-500" />}
                label="Bài toán đã giải"
                value={userStats.problem_solved}
              />
              <StatCard
                icon={<Layers className="text-purple-500" />}
                label="Cấp độ"
                value={level}
              />
            </div>
          </>
        ) : (
          <p className="text-gray-500 mb-6 text-center">Đang tải thống kê...</p>
        )}

      </div>
    </div>
  );
};

const StatCard = ({
  icon,
  label,
  value,
  bgColor = "bg-white",
}: {
  icon: React.ReactNode;
  label: string;
  value: number | string;
  bgColor?: string;
}) => (
  <div className={`${bgColor} rounded-2xl shadow-md p-6 flex flex-col items-center justify-center hover:shadow-lg transition`}>
    <div className="mb-3">{icon}</div>
    <p className="text-sm text-gray-500">{label}</p>
    <p className="text-2xl font-bold text-gray-800">{value}</p>
  </div>
);

export default HomePage;
