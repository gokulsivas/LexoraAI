import axios from 'axios'

// Send to your backend to summarize using LLM
export const summarizeAnswer = async (rawText, question) => {
  try {
    const response = await axios.post('http://localhost:8000/api/summarize', {
      text: rawText,
      question: question
    })
    return response.data.summary
  } catch (error) {
    console.error('Summarization error:', error)
    return rawText // Fallback to raw text
  }
}
