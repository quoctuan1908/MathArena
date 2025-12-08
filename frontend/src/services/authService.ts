import type { LoginResponse } from "../types/auth";


export const login = (loginData : LoginResponse) => {
    console.log(loginData)
    localStorage.setItem('user', JSON.stringify(loginData.user))
    localStorage.setItem('token', JSON.stringify(loginData.token))
}

export const logout = () => {
    console.log("Logout")
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    location.href = "/login"
}
