import { useEffect, useState } from 'react'
import api from '../api'

export default function HistoryPanel({ refreshKey }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    api
      .get('/resumes/history')
      .then(({ data }) => { if (!cancelled) setItems(data) })
      .catch(() => { if (!cancelled) setError('Could not load history.') })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [refreshKey])

  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>Evaluation history</h3>
      {error && <div className="error-banner">{error}</div>}
      {loading && <p className="empty-state">Loading…</p>}
      {!loading && items.length === 0 && <p className="empty-state">No evaluations yet — run one from the Evaluate tab.</p>}
      {!loading &&
        items.map((item) => (
          <div className="history-item" key={item._id}>
            <div>
              <div className="job">{item.job_title}</div>
              <div className="date">{new Date(item.processed_at).toLocaleString()}</div>
            </div>
            <div className="score">{item.ats_score}%</div>
          </div>
        ))}
    </div>
  )
}
