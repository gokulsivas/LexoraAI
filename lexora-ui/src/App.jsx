import { useState } from 'react'
import { Scale, Menu, X } from 'lucide-react'
import QuerySection from './components/QuerySection'
import AnswerDisplay from './components/AnswerDisplay'
import './App.css'

export default function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleResults = (data) => {
    setResults(data)
    setLoading(false)
  }

  const handleQueryStart = () => {
    setLoading(true)
  }

  return (
    <div className="flex flex-col lg:flex-row h-screen bg-white">
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 text-gray-700 hover:bg-gray-100 rounded-lg"
      >
        {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      <aside
        className={`${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 transition-transform duration-300 fixed lg:relative w-64 lg:w-96 h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white p-6 border-r border-slate-700 overflow-y-auto z-40`}
      >
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-blue-500 p-2 rounded-lg">
            <Scale size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-bold">LexoraAI</h1>
            <p className="text-xs text-slate-400">Legal Chatbot</p>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden pt-16 lg:pt-0 bg-gray-950">
        <div className="flex-1 overflow-y-auto p-6 flex flex-col">
          <div className="flex-1 max-w-4xl mx-auto w-full">
            <AnswerDisplay data={results} loading={loading} />
          </div>
        </div>

        <div className="bg-gray-950 p-6 pb-8 flex justify-center">
          <div style={{ width: '90%', maxWidth: '900px' }} className="bg-gray-800 rounded-2xl p-4 shadow-2xl border border-gray-700">
            <QuerySection
              onResults={handleResults}
              onQueryStart={handleQueryStart}
            />
          </div>
        </div>
      </main>

      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}
