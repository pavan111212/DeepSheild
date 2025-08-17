
import React from "react"

export default function ProgressBar({ value }: { value: number }) {
  return (
    <div className="w-full bg-gray-800 rounded-2xl h-3 overflow-hidden">
      <div className="h-3 rounded-2xl" style={{ width: `${value}%`, background: "linear-gradient(90deg, #34d399, #60a5fa)" }}></div>
    </div>
  )
}
