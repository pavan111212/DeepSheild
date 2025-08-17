
import React, { useEffect, useRef } from "react"

export default function VideoPreview({ file }: { file: File | null }) {
  const ref = useRef<HTMLVideoElement>(null)
  useEffect(() => {
    if (!file || !ref.current) return
    const url = URL.createObjectURL(file)
    ref.current.src = url
    return () => URL.revokeObjectURL(url)
  }, [file])
  if (!file) return null
  return (
    <div className="rounded-2xl overflow-hidden border border-white/10">
      <video ref={ref} controls className="w-full h-auto" />
    </div>
  )
}
