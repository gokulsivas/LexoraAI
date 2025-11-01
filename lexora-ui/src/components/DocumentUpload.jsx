import { useState, useRef } from 'react'
import axios from 'axios'
import { Upload } from 'lucide-react'

export default function DocumentUpload() {
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.pdf')) {
      alert('Only PDF files allowed')
      return
    }

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(
        'http://localhost:8000/api/upload-pdf',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 60000
        }
      )
      alert('Document uploaded successfully')
      fileInputRef.current.value = ''
    } catch (error) {
      console.error('Upload error:', error)
      alert(`Upload failed: ${error.response?.data?.message || error.message}`)
    } finally {
      setUploading(false)
    }
  }

  return (
    <button
      onClick={() => fileInputRef.current?.click()}
      disabled={uploading}
      className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-700 hover:bg-gray-600 disabled:bg-gray-600 flex items-center justify-center transition text-gray-400 hover:text-white disabled:opacity-50"
      title="Upload PDF document"
    >
      <Upload size={20} strokeWidth={1.5} />
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileUpload}
        className="hidden"
      />
    </button>
  )
}
