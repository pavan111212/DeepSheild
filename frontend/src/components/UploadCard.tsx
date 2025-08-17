
import React, { useCallback, useRef, useState } from "react"
import ProgressBar from "./ProgressBar"

type Props = {
  onSelected: (file: File) => void
}

export default function UploadCard({ onSelected }: Props) {
  const [dragOver, setDragOver] = useState(false)
  const [progress, setProgress] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files || !files[0]) return
    const file = files[0]
    onSelected(file)
    // simulate progress bar animation
    setProgress(10)
    const id = setInterval(() => {
      setProgress((p) => {
        const np = Math.min(100, p + 10)
        if (np >= 100) clearInterval(id)
        return np
      })
    }, 120)
  }, [onSelected])

  return (
    <div
      className={`glass rounded-2xl p-8 text-center transition-all ${dragOver ? "ring-2 ring-emerald-400" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        e.preventDefault()
        setDragOver(false)
        handleFiles(e.dataTransfer.files)
      }}
    >
      <div className="mx-auto mb-4 w-16 h-16 rounded-2xl flex items-center justify-center bg-gray-900">
        <span className="text-3xl">🎬</span>
      </div>
      <h2 className="text-xl font-semibold mb-2">Upload a video</h2>
      <p className="text-gray-400 mb-6">Drag & drop an MP4/MOV/AVI, or click to select.</p>
      <button
        onClick={() => inputRef.current?.click()}
        className="px-5 py-2 rounded-2xl bg-emerald-400/20 hover:bg-emerald-400/30 transition text-emerald-300 font-medium"
      >
        Choose File
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <div className="mt-6">
        <ProgressBar value={progress} />
      </div>
    </div>
  )
}
