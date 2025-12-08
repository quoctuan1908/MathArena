import React, { useState } from "react"
import type { UserCreate } from "../../types/user"
import { Input } from "../Input"
import { Button } from "../Button"
import apiSlice from "../../store/apiSlice"

const initialSignUp: UserCreate = {
  username: "",
  password_hashed: "",
  user_info: {
    name: "",
    birthday: "",
    address: "",
    phone: "",
    email: "",
  },
}

const SignUpForm = () => {
  const [createUser] = apiSlice.useCreateUserMutation()
  const [signUpData, setSignUpData] = useState<UserCreate>(initialSignUp)

  const setUserValue = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target
    setSignUpData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const setUserInfoValue = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target
    setSignUpData((prev) => ({
      ...prev,
      user_info: {
        ...prev.user_info,
        [name]: value,
      },
    }))
  }

  const handleSubmitSignUp = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const result = await createUser(signUpData).unwrap()
      if (result) {
        console.log(result)
        alert("Đăng ký thành công!")
      }
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100">
      <form
        onSubmit={handleSubmitSignUp}
        className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-lg space-y-6"
      >
        <h2 className="text-2xl font-bold text-center text-indigo-700 mb-2">
          Tạo tài khoản mới
        </h2>
        <p className="text-center text-gray-500 text-sm mb-4">
          Điền đầy đủ thông tin để đăng ký
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Tên đăng nhập
            </label>
            <Input
              name="username"
              value={signUpData.username}
              onChange={setUserValue}
              placeholder="Nhập tên đăng nhập"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Mật khẩu
            </label>
            <Input
              name="password_hashed"
              type="password"
              value={signUpData.password_hashed}
              onChange={setUserValue}
              placeholder="Nhập mật khẩu"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Họ và tên
            </label>
            <Input
              name="name"
              value={signUpData.user_info.name}
              onChange={setUserInfoValue}
              placeholder="Nhập họ và tên"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Ngày sinh
            </label>
            <Input
              name="birthday"
              type="date"
              value={signUpData.user_info.birthday}
              onChange={setUserInfoValue}
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Địa chỉ
            </label>
            <Input
              name="address"
              value={signUpData.user_info.address}
              onChange={setUserInfoValue}
              placeholder="Nhập địa chỉ"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Số điện thoại
            </label>
            <Input
              name="phone"
              type="tel"
              value={signUpData.user_info.phone}
              onChange={setUserInfoValue}
              placeholder="VD: 0901234567"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Email
            </label>
            <Input
              name="email"
              type="email"
              value={signUpData.user_info.email}
              onChange={setUserInfoValue}
              placeholder="VD: email@example.com"
              className="w-full border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 rounded-lg"
            />
          </div>
        </div>

        <div className="pt-4">
          <Button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition"
          >
            Đăng ký
          </Button>
        </div>
      </form>
    </div>
  )
}

export default SignUpForm
