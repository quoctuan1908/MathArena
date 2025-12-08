import { Navigate } from "react-router-dom"
import { useSelector } from "react-redux"
import type { RootState } from "../store/store"
import type { JSX } from "react"

type Props = {
  children: JSX.Element
}

export const PublicRoute = ({ children }: Props) => {
  const token = useSelector((state: RootState) => state.auth.token)
  if (token) {
    return <Navigate to="/" replace />
  }
  return children
}
