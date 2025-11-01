import { useState } from 'react'
import axios from 'axios'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'

export default function DocumentUpload({ onUpload }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0] || null
    setFile(selectedFile)
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('doc_type', 'ipc')

    try {
      const response = await axios.post(
        'http://localhost:8000/api/upload-pdf',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 30000
        }
      )
      setSuccess(`✓ Stored ${response.data.chunks_stored} chunks`)
      if (onUpload) onUpload(file.name)
      setFile(null)
      setTimeout(() => setSuccess(null), 4000)
    } catch (err) {
      setError(
        `Upload failed: ${err.response?.data?.message || err.message}`
      )
    }

    setLoading(false)
  }

  return (
    <div className="bg-slate-700 rounded-lg p-5 space-y-4 w-full">
      {/* File Input */}
      <div>
        <label className="block text-xs font-semibold text-slate-200 mb-2 uppercase">
          Select PDF File
        </label>
        <div className="relative border-2 border-dashed border-slate-400 rounded-lg p-6 text-center hover:border-blue-400 transition cursor-pointer bg-slate-600">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={loading}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-label="Upload PDF file"
          />
          <div className="flex flex-col items-center gap-2">
            <Upload size={24} className="text-slate-300" />
            <p className="text-sm text-slate-200 font-medium">
              {file ? file.name : 'Click or drag PDF here'}
            </p>
            <p className="text-xs text-slate-400">Max 50MB</p>
          </div>
        </div>
      </div>

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-500 disabled:cursor-not-allowed text-white font-semibold py-2.5 px-4 rounded-lg transition flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <span className="animate-spin">⏳</span> Uploading...
          </>
        ) : (
          <>
            <Upload size={18} /> Upload Document
          </>
        )}
      </button>

      {/* Success Message */}
      {success && (
        <div className="bg-green-900 border border-green-700 text-green-100 px-4 py-3 rounded-lg flex items-center gap-2 text-sm">
          <CheckCircle size={18} className="flex-shrink-0" />
          {success}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-900 border border-red-700 text-red-100 px-4 py-3 rounded-lg flex items-center gap-2 text-sm">
          <AlertCircle size={18} className="flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  )
}
