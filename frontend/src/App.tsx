
import React, { useState } from "react"
import UploadCard from "./components/UploadCard"
import ResultCard from "./components/ResultCard"
import VideoPreview from "./components/VideoPreview"
import { predictVideo } from "./api"

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  async function handlePredict(f: File) {
    setFile(f)
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await predictVideo(f)
      setResult(res)
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || "Prediction failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen px-4">
      <div className="max-w-5xl mx-auto py-10">
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
            <span className="text-emerald-300">deep</span>Shield
          </h1>
          <p className="text-gray-400 mt-2">Detect DeepFake videos with a clean, fast interface.</p>
        </header>

        <div className="grid md:grid-cols-2 gap-6">
          <UploadCard onSelected={handlePredict} />
          <div className="space-y-6">
            <VideoPreview file={file} />
            {loading && (
              <div className="glass rounded-2xl p-6 text-center">Analyzing video…</div>
            )}
            {error && (
              <div className="rounded-2xl p-4 bg-red-500/20 border border-red-500/30 text-red-200">{error}</div>
            )}
            <ResultCard result={result} />
          </div>
        </div>

        <footer className="mt-10 text-xs text-gray-500">
          For best results, add real pretrained weights in <code>backend/weights/model.pt</code> (see README).
        </footer>
      </div>
    </div>
  )
}
