import React, { useState } from "react"
import type { UserLogin } from "../../types/auth"
import { Input } from "../Input"
import { Button } from "../Button"
import apiSlice from "../../store/apiSlice"
import { Link } from "react-router-dom"
import { useDispatch } from "react-redux"
import { setCredentials } from "../../store/authSlice"

const LoginForm = () => {
  const [loginUser] = apiSlice.useLoginUserMutation()
  const [loginData, setLoginData] = useState<UserLogin>({} as UserLogin)
  const dispatch = useDispatch()

  const setUserValue = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target
    setLoginData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmitLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      await loginUser(loginData)
        .unwrap()
        .then((result) => {
          dispatch(setCredentials(result))
        })
        .catch((err) => {
            if (err.status == 401) {
                alert("Tài khoản hoặc mật khẩu không chính xác")
            }
          
        })
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <form
        onSubmit={handleSubmitLogin}
        className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md space-y-6"
      >
        <h2 className="text-2xl font-bold text-center text-indigo-700 mb-4">
          Đăng nhập tài khoản
        </h2>

        <div>
          <label
            htmlFor="username"
            className="block text-sm font-medium text-gray-600 mb-1"
          >
            Tài khoản
          </label>
          <Input
            id="username"
            name="username"
            className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            value={loginData.username || ""}
            onChange={setUserValue}
            placeholder="Nhập tài khoản..."
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-600 mb-1"
          >
            Mật khẩu
          </label>
          <Input
            id="password"
            name="password"
            type="password"
            className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            value={loginData.password || ""}
            onChange={setUserValue}
            placeholder="Nhập mật khẩu..."
          />
        </div>

        <div className="flex flex-col gap-3">
          <Button
            type="submit"
            className="bg-indigo-600 text-white hover:bg-indigo-700 transition rounded-lg py-2"
          >
            Đăng nhập
          </Button>
          <Link
            to="/signup"
            className="text-center text-indigo-600 hover:underline text-sm"
          >
            Chưa có tài khoản? Đăng ký ngay
          </Link>
        </div>
      </form>
    </div>
  )
}

export default LoginForm
