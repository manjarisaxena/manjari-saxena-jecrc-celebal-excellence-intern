import { useState } from 'react'
import AuthScreen from './components/AuthScreen.jsx'
import EvaluatePanel from './components/EvaluatePanel.jsx'
import HistoryPanel from './components/HistoryPanel.jsx'
import ChatPanel from './components/ChatPanel.jsx'

export default function App() {
  const [name, setName] = useState(() => localStorage.getItem('hiresense_name'))
  const [tab, setTab] = useState('evaluate')
  const [historyRefresh, setHistoryRefresh] = useState(0)

  const logout = () => {
    localStorage.removeItem('hiresense_token')
    localStorage.removeItem('hiresense_name')
    setName(null)
  }

  if (!name) {
    return (
      <div className="app-shell">
        <AuthScreen onAuthenticated={setName} />
      </div>
    )
  }

  return (
    <div className="app-shell">
      <div className="topbar">
        <div className="brand">
          <div className="brand-mark" />
          HireSense AI
        </div>
        <div className="user-chip">
          {name}
          <button className="logout-btn" onClick={logout}>Log out</button>
        </div>
      </div>

      <div className="main">
        <div className="container">
          <div className="tabs">
            <button className={`tab ${tab === 'evaluate' ? 'active' : ''}`} onClick={() => setTab('evaluate')}>Evaluate</button>
            <button className={`tab ${tab === 'history' ? 'active' : ''}`} onClick={() => setTab('history')}>History</button>
            <button className={`tab ${tab === 'chat' ? 'active' : ''}`} onClick={() => setTab('chat')}>Chat</button>
          </div>

          {tab === 'evaluate' && <EvaluatePanel onEvaluated={() => setHistoryRefresh((k) => k + 1)} />}
          {tab === 'history' && <HistoryPanel refreshKey={historyRefresh} />}
          {tab === 'chat' && <ChatPanel />}
        </div>
      </div>
    </div>
  )
}
