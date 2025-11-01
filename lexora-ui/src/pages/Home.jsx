import { useState } from 'react'
import DocumentUpload from '../components/DocumentUpload'
import QuerySection from '../components/QuerySection'
import AnswerDisplay from '../components/AnswerDisplay'

export default function Home() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleQuery = (data) => {
    setLoading(false)
    setResults(data)
  }

  const handleQueryStart = () => {
    setLoading(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">LexoraAI</h1>
          <p className="text-gray-600 mt-2">AI-Powered Legal Document Q&A System</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-6">
            <DocumentUpload />
            <QuerySection onResults={handleQuery} onLoadingStart={handleQueryStart} />
          </div>

          <div>
            <AnswerDisplay data={results} loading={loading} />
          </div>
        </div>
      </div>
    </div>
  )
}
