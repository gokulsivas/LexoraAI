import { useState, useRef } from 'react'
import axios from 'axios'
import { Send, Sliders, Loader, Upload } from 'lucide-react'

export default function QuerySection({ onResults, onQueryStart }) {
  const [question, setQuestion] = useState('')
  const [nChunks, setNChunks] = useState(5)
  const [loading, setLoading] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const fileInputRef = useRef(null)

  const handleQuery = async () => {
    if (!question.trim()) return

    setLoading(true)
    if (onQueryStart) onQueryStart()

    try {
      const response = await axios.post(
        'http://localhost:8000/api/query',
        {
          question: question.trim(),
          doc_type: null,
          n_chunks: nChunks
        },
        { timeout: 120000 }
      )

      console.log('Backend response:', response.data)
      onResults(response.data)
      setQuestion('')
    } catch (error) {
      console.error('Query error:', error)
      alert(`Error: ${error.response?.data?.message || error.message}`)
    }

    setLoading(false)
  }

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('doc_type', 'ipc')

      axios.post('http://localhost:8000/api/upload-pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 120000
      }).then(() => {
        alert('Document uploaded successfully')
      }).catch((err) => {
        alert(`Upload failed: ${err.message}`)
      })
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

      <div className="flex items-center gap-3 bg-gray-800 rounded-xl p-2">
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 flex items-center justify-center transition text-white"
          title="Settings"
        >
          <Sliders size={28} strokeWidth={1.5} />
        </button>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
          placeholder="Ask your question..."
          className="flex-1 bg-white border-none rounded-lg p-3 resize-none outline-none text-gray-900 placeholder-gray-500 font-medium max-h-24"
          rows="1"
          style={{ minHeight: '48px' }}
        />

        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-gray-700 hover:bg-gray-600 flex items-center justify-center transition text-gray-400 hover:text-white"
          title="Upload document"
        >
          <Upload size={28} strokeWidth={1.5} />
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
          className="hidden"
        />

        <button
          onClick={handleQuery}
          disabled={loading || !question.trim()}
          className="flex-shrink-0 w-14 h-14 rounded-full bg-gray-700 hover:bg-gray-600 disabled:bg-gray-700 disabled:cursor-not-allowed flex items-center justify-center transition text-gray-400 hover:text-white"
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
