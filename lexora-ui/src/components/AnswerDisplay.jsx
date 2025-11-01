import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { AlertCircle, Loader, Copy, Check, Scale } from 'lucide-react'


export default function AnswerDisplay({ data, loading }) {
  const [copied, setCopied] = useState(false)


  const toggleSource = (idx) => {}


  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(typeof text === 'string' ? text : JSON.stringify(text))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }


  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="text-center">
          <Loader size={48} className="animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-400 text-lg">Searching for answer...</p>
        </div>
      </div>
    )
  }


  if (!data) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="text-center">
          <Scale size={48} className="mx-auto mb-3 text-gray-500" />
          <p className="text-gray-400 text-lg">Upload a document and ask a question</p>
        </div>
      </div>
    )
  }


  const answer = data?.answer || data?.simplified_answer || data?.message || JSON.stringify(data)


  if (!answer) {
    return (
      <div className="bg-red-500 bg-opacity-10 border border-red-500 border-opacity-30 rounded-xl p-5 max-w-3xl backdrop-blur-sm">
        <div className="flex items-start gap-3">
          <AlertCircle size={22} className="text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-300 mb-1">Unable to Answer</h3>
            <p className="text-red-200 text-sm">No answer found in the response.</p>
          </div>
        </div>
      </div>
    )
  }


  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-2xl p-8 shadow-2xl backdrop-blur-sm hover:border-slate-600 transition w-full min-h-64">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600 bg-opacity-20 flex items-center justify-center">
            <Scale size={20} className="text-blue-400" />
          </div>
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Simplified Answer</h2>
        </div>
        <button
          onClick={() => copyToClipboard(answer)}
          className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition flex items-center gap-2"
        >
          {copied ? (
            <>
              <Check size={16} /> Copied
            </>
          ) : (
            <>
              <Copy size={16} /> Copy
            </>
          )}
        </button>
      </div>


      <div className="prose prose-invert max-w-none text-white leading-relaxed">
        <ReactMarkdown
          components={{
            p: ({ children }) => <p className="mb-4 text-white text-base leading-7">{children}</p>,
            strong: ({ children }) => <strong className="text-white font-bold">{children}</strong>,
            h1: ({ children }) => <h1 className="text-2xl font-bold text-white mt-6 mb-3">{children}</h1>,
            h2: ({ children }) => <h2 className="text-xl font-bold text-white mt-5 mb-2">{children}</h2>,
            h3: ({ children }) => <h3 className="text-lg font-semibold text-white mt-4 mb-2">{children}</h3>,
            ul: ({ children }) => <ul className="list-disc pl-6 space-y-2 mb-4 text-white">{children}</ul>,
            ol: ({ children }) => <ol className="list-decimal pl-6 space-y-3 mb-4 text-white">{children}</ol>,
            li: ({ children }) => <li className="text-white text-base leading-7">{children}</li>,
          }}
        >
          {typeof answer === 'string' ? answer : JSON.stringify(answer, null, 2)}
        </ReactMarkdown>
      </div>
    </div>
  )
}
