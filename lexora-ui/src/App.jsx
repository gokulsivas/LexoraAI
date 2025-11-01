import { useState } from 'react'
import { Scale, Menu, X, Plus, MessageSquare, Trash2, Edit2 } from 'lucide-react'
import { Loader } from 'lucide-react'
import QuerySection from './components/QuerySection'
import AnswerDisplay from './components/AnswerDisplay'
import './App.css'

export default function App() {
  const [chats, setChats] = useState([
    { id: Date.now(), title: 'New Chat', messages: [] }
  ])
  const [activeChat, setActiveChat] = useState(chats[0].id)
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [editingChat, setEditingChat] = useState(null)
  const [editTitle, setEditTitle] = useState('')

  const getCurrentChat = () => chats.find(c => c.id === activeChat)

  const handleResults = (data) => {
    if (data) {
      setChats(prev => prev.map(chat => 
        chat.id === activeChat 
          ? {
              ...chat,
              messages: [...chat.messages, {
                id: Date.now(),
                type: 'answer',
                data: data
              }],
              title: chat.messages.length === 0 && data.answer 
                ? data.answer.slice(0, 30) + '...' 
                : chat.title
            }
          : chat
      ))
    }
    setLoading(false)
  }

  const handleQueryStart = (question) => {
    setLoading(true)
  }

  const createNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: 'New Chat',
      messages: []
    }
    setChats(prev => [...prev, newChat])
    setActiveChat(newChat.id)
    setSidebarOpen(false)
  }

  const deleteChat = (chatId) => {
    if (chats.length === 1) return
    setChats(prev => prev.filter(c => c.id !== chatId))
    if (activeChat === chatId) {
      setActiveChat(chats[0].id === chatId ? chats[1].id : chats[0].id)
    }
  }

  const startRename = (chat) => {
    setEditingChat(chat.id)
    setEditTitle(chat.title)
  }

  const saveRename = () => {
    if (editTitle.trim()) {
      setChats(prev => prev.map(c => 
        c.id === editingChat ? { ...c, title: editTitle.trim() } : c
      ))
    }
    setEditingChat(null)
    setEditTitle('')
  }

  const cancelRename = () => {
    setEditingChat(null)
    setEditTitle('')
  }

  const currentChat = getCurrentChat()

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

        <button
          onClick={createNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition flex items-center justify-center gap-2 mb-4"
        >
          <Plus size={20} />
          New Chat
        </button>

        <div className="space-y-2">
          {chats.map(chat => (
            <div
              key={chat.id}
              className={`group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition ${
                activeChat === chat.id
                  ? 'bg-slate-700'
                  : 'hover:bg-slate-700/50'
              }`}
            >
              <MessageSquare size={18} className="flex-shrink-0" />
              {editingChat === chat.id ? (
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') saveRename()
                    if (e.key === 'Escape') cancelRename()
                  }}
                  onBlur={saveRename}
                  autoFocus
                  className="flex-1 bg-slate-600 text-white text-sm px-2 py-1 rounded outline-none"
                />
              ) : (
                <span
                  onClick={() => {
                    setActiveChat(chat.id)
                    setSidebarOpen(false)
                  }}
                  className="flex-1 text-sm truncate"
                >
                  {chat.title}
                </span>
              )}
              <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition">
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    startRename(chat)
                  }}
                  className="p-1 hover:bg-blue-600 rounded"
                >
                  <Edit2 size={16} />
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    deleteChat(chat.id)
                  }}
                  className="p-1 hover:bg-red-600 rounded"
                  disabled={chats.length === 1}
                  style={{ opacity: chats.length === 1 ? 0.5 : 1, cursor: chats.length === 1 ? 'not-allowed' : 'pointer' }}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </aside>

      <main className="flex-1 flex flex-col overflow-hidden pt-16 lg:pt-0 bg-gray-950">
        <div className={`flex-1 overflow-y-auto p-6 flex ${currentChat?.messages.length === 0 && !loading ? 'flex-col justify-center items-center' : 'flex-col'}`}>
          <div className="flex justify-center w-full">
            <div style={{ width: '95%', maxWidth: '1200px' }}>
              {currentChat?.messages.length === 0 && !loading ? (
                <div className="text-center">
                  <Scale size={48} className="mx-auto mb-3 text-gray-500" />
                  <p className="text-gray-400 text-lg">Start a conversation. Upload a document and ask questions.</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {currentChat?.messages.map((msg) => (
                    <div key={msg.id}>
                      {msg.type === 'answer' && (
                        <div className="flex justify-start">
                          <AnswerDisplay data={msg.data} loading={false} />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
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
