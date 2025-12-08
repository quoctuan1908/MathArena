import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { UserResponse } from '../types/user'

interface AuthState {
  user: UserResponse | null
  token: string | null
}

const initialState: AuthState = {
  user: localStorage.getItem('user')
    ? JSON.parse(localStorage.getItem('user')!)
    : null,
  token: localStorage.getItem('token')
    ? JSON.parse(localStorage.getItem('token')!)
    : null,
}


export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Cập nhật kiểu PayloadAction để cho phép null
    setCredentials: (
      state,
      action: PayloadAction<{ user: UserResponse | null; token: string | null }>
    ) => {
      const { user, token } = action.payload

      // Thêm điều kiện kiểm tra null
      if (user !== null && token !== null) {
        state.user = user
        state.token = token

        // Lưu vào localStorage
        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('token', JSON.stringify(token))
      } else {
        // Nếu bạn muốn XÓA credentials khi nhận null/null
        // thì nên dùng reducer `logout` hoặc thêm logic xóa ở đây.
        // Hiện tại, nếu là null/null, state và storage sẽ KHÔNG thay đổi.
        console.log("Dữ liệu user hoặc token là null, không lưu vào Redux/LocalStorage.")
      }
    },
    logout: (state) => {
      state.user = null
      state.token = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      
      
    },
  },
})

export const { setCredentials, logout } = authSlice.actions
export default authSlice.reducer