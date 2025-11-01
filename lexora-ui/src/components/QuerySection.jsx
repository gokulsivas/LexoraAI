import { useState, useRef } from 'react'
import axios from 'axios'
import { Send, Sliders, Loader, Upload } from 'lucide-react'

export default function QuerySection({ onResults, onQueryStart }) {
  const [question, setQuestion] = useState('')
  const [nChunks, setNChunks] = useState(5)
  const [loading, setLoading] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleQuery = async () => {
    if (!question.trim()) return

    const currentQuestion = question.trim()
    setQuestion('')
    setLoading(true)
    onQueryStart(currentQuestion)

    try {
      const response = await axios.post(
        'http://localhost:8000/api/query',
        {
          question: currentQuestion,
          doc_type: null,
          n_chunks: nChunks
        },
        { timeout: 120000 }
      )

      console.log('Backend response received:', response.data)
      setLoading(false)
      onResults(response.data)
    } catch (error) {
      console.error('Query error:', error)
      alert(`Error: ${error.response?.data?.message || error.message}`)
      setLoading(false)
    }
  }

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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading && question.trim()) {
      e.preventDefault()
      handleQuery()
    }
  }

  return (
    <div className="w-full">
      {showAdvanced && (
        <div className="mb-4 bg-gray-700 border border-gray-600 rounded-lg p-4">
          <label className="block text-sm font-medium text-gray-200 mb-2">
            Document Chunks: {nChunks}
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={nChunks}
            onChange={(e) => setNChunks(parseInt(e.target.value))}
            disabled={loading}
            className="w-full cursor-pointer"
          />
        </div>
      )}

      <div className="flex items-center gap-2 bg-gray-800 rounded-full p-1">
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 flex items-center justify-center transition text-white"
          title="Settings"
          disabled={loading}
        >
          <Sliders size={28} strokeWidth={1.5} />
        </button>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
          placeholder="Ask your question..."
          className="flex-1 bg-white border-none rounded-full px-4 py-2 resize-none outline-none text-gray-900 placeholder-gray-500 font-medium max-h-24"
          rows="1"
          style={{ minHeight: '50px' }}
        />

        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading || loading}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-gray-700 hover:bg-gray-600 disabled:bg-gray-600 flex items-center justify-center transition text-gray-400 hover:text-white disabled:opacity-50"
          title="Upload PDF document"
        >
          <Upload size={28} strokeWidth={1.5} />
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
          />
        </button>

        <button
          onClick={handleQuery}
          disabled={loading || !question.trim()}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition text-white"
          title="Send message"
        >
          {loading ? (
            <Loader size={28} strokeWidth={1.5} className="animate-spin" />
          ) : (
            <Send size={28} strokeWidth={1.5} />
          )}
        </button>
      </div>
    </div>
  )
}
