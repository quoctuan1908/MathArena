import React from "react"

type InputProps = React.InputHTMLAttributes<HTMLInputElement>

export const Input = (props: InputProps) => {
  return (
    <input
      {...props}
      className={`border rounded px-2 py-1 ${props.className || ""}`}
    />
  )
}