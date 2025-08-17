
import React from "react"

type FrameScore = { idx: number; score: number }
type Result = {
  label: "fake" | "real"
  score: number
  threshold: number
  frames_analyzed: number
  per_frame: FrameScore[]
}

export default function ResultCard({ result }: { result: Result | null }) {
  if (!result) return null
  const pct = Math.round(result.score * 100)
  return (
    <div className="glass rounded-2xl p-6">
      <div className="flex items-center gap-4 mb-4">
        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${result.label === "fake" ? "bg-red-400/20" : "bg-emerald-400/20"}`}>
          <span className="text-2xl">{result.label === "fake" ? "⚠️" : "✅"}</span>
        </div>
        <div>
          <div className="text-sm text-gray-400">Prediction</div>
          <div className="text-xl font-semibold capitalize">{result.label}</div>
        </div>
        <div className="ml-auto text-right">
          <div className="text-sm text-gray-400">Confidence</div>
          <div className="text-xl font-semibold">{pct}%</div>
        </div>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {result.per_frame.slice(0, 8).map((f) => (
          <div key={f.idx} className="rounded-xl bg-gray-900 p-3">
            <div className="text-xs text-gray-400">Frame {f.idx}</div>
            <div className="text-lg font-medium">{(f.score * 100).toFixed(1)}%</div>
          </div>
        ))}
      </div>
      <div className="text-xs text-gray-500 mt-4">
        Threshold: {result.threshold} • Frames analyzed: {result.frames_analyzed}
      </div>
    </div>
  )
}
