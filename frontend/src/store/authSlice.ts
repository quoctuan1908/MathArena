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
  token: localStorage.getItem('token') || null,
}

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Khi login thành công
    setCredentials: (
      state,
      action: PayloadAction<{ user: UserResponse; token: string }>
    ) => {
      state.user = action.payload.user
      state.token = action.payload.token

      localStorage.setItem('user', JSON.stringify(action.payload.user))
      localStorage.setItem('token', action.payload.token)
    },

    // Khi refresh token thành công
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload
      localStorage.setItem('token', action.payload)
    },

    logout: (state) => {
      state.user = null
      state.token = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
  },
})

export const { setCredentials, setToken, logout } = authSlice.actions
export default authSlice.reducer