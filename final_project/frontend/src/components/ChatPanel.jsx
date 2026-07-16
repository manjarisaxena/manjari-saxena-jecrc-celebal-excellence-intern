import { useState } from 'react'
import { Send } from 'lucide-react'
import api from '../api'

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hi! Ask me anything about your resume results or how to improve your score." },
  ])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')

  const send = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text) return
    setMessages((m) => [...m, { role: 'user', text }])
    setInput('')
    setSending(true)
    setError('')
    try {
      const { data } = await api.post('/chatbot/chat', { message: text })
      setMessages((m) => [...m, { role: 'bot', text: data.response }])
    } catch (err) {
      setError(err.response?.data?.detail || 'Chat failed. Please try again.')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>Ask HireSense AI</h3>
      {error && <div className="error-banner">{error}</div>}
      <div className="chat-log">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.role}`}>{m.text}</div>
        ))}
        {sending && <div className="chat-bubble bot">Thinking…</div>}
      </div>
      <form className="chat-input-row" onSubmit={send}>
        <input
          type="text"
          placeholder="Type your question…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit" className="btn-primary" disabled={sending}>
          <Send size={16} />
        </button>
      </form>
    </div>
  )
}
