import React from "react"

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>

export const Button = ({ className, children, ...props }: ButtonProps) => {
  return (
    <button
      {...props}
      className={`border rounded px-2 py-1 ${className || ""}`}
    >
      {children}
    </button>
  )
}