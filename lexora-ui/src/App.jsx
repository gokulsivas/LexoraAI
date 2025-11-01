import { useState } from 'react'
import { Scale, Menu, X } from 'lucide-react'
import { Loader } from 'lucide-react'
import QuerySection from './components/QuerySection'
import AnswerDisplay from './components/AnswerDisplay'
import './App.css'

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleResults = (data) => {
    if (data) {
      setMessages((prev) => [...prev, {
        id: Date.now(),
        type: 'answer',
        data: data
      }])
    }
    setLoading(false)
  }

  const handleQueryStart = (question) => {
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
          <div className="flex justify-center w-full">
            <div style={{ width: '95%', maxWidth: '1200px' }} className="space-y-6">
              {messages.length === 0 ? (
                <div className="flex justify-center items-center h-full">
                  <div className="text-center">
                    <Scale size={48} className="mx-auto mb-3 text-gray-500" />
                    <p className="text-gray-400 text-lg">Start a conversation. Upload a document and ask questions.</p>
                  </div>
                </div>
              ) : (
                messages.map((msg) => (
                  <div key={msg.id}>
                    {msg.type === 'answer' && (
                      <div className="flex justify-start">
                        <AnswerDisplay data={msg.data} loading={false} />
                      </div>
                    )}
                  </div>
                ))
              )}
              {loading && (
                <div className="flex justify-center items-center py-8">
                  <div className="text-center">
                    <Loader size={32} className="animate-spin mx-auto mb-3 text-blue-600" />
                    <p className="text-gray-400 text-sm">Searching for answer...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="bg-gray-950 p-6 pb-8 flex justify-center">
          <div style={{ width: '90%', maxWidth: '900px' }}>
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
