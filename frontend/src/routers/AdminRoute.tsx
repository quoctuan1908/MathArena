import { useSelector } from "react-redux"
import { Navigate } from "react-router-dom"
import type { RootState } from "../store/store"
import type { JSX } from "react"

interface AdminRouteProps {
  element: JSX.Element
}

const AdminRoute = ({ element }: AdminRouteProps) => {
  const user = useSelector((state: RootState) => state.auth.user)

  // 🛡️ Nếu chưa đăng nhập hoặc không phải admin → chặn
  if (!user) return <Navigate to="/login" replace />
  if (user.user_role.user_role_name !== "admin") return <Navigate to="/" replace />

  // ✅ Cho phép truy cập nếu là admin
  return element
}

export default AdminRoute