
import axios from "axios"

const API_BASE = import.meta.env.VITE_API_BASE_URL || (window.localStorage.getItem("API_BASE_URL") || "http://localhost:8000")

export async function predictVideo(file: File) {
  const form = new FormData()
  form.append("file", file)
  const res = await axios.post(`${API_BASE}/api/v1/predict`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  })
  return res.data
}
