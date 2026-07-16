import { useState } from 'react'
import api from '../api'
import ResultCard from './ResultCard.jsx'

export default function EvaluatePanel({ onEvaluated }) {
  const [file, setFile] = useState(null)
  const [jdTitle, setJdTitle] = useState('')
  const [jdText, setJdText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please attach a resume file (.pdf, .docx, or .txt).')
      return
    }
    setError('')
    setLoading(true)
    setResult(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('jd_title', jdTitle)
      formData.append('jd_text', jdText)
      const { data } = await api.post('/resumes/evaluate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(data)
      onEvaluated?.(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Evaluation failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="card">
        <h3 style={{ marginTop: 0 }}>Scan a resume</h3>
        {error && <div className="error-banner">{error}</div>}
        <form onSubmit={submit}>
          <label htmlFor="jdTitle">Job title</label>
          <input
            id="jdTitle"
            type="text"
            placeholder="e.g. Backend Engineer"
            value={jdTitle}
            onChange={(e) => setJdTitle(e.target.value)}
            required
          />

          <label htmlFor="jdText">Job description</label>
          <textarea
            id="jdText"
            placeholder="Paste the job description here…"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            required
          />

          <label htmlFor="resumeFile">Resume file (.pdf, .docx, .txt)</label>
          <input
            id="resumeFile"
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            required
          />

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Scanning…' : 'Run evaluation'}
          </button>
        </form>

        {loading && (
          <div className="scan-frame" style={{ marginTop: 20 }}>
            <div className="laser" />
            <div className="scan-label">ANALYZING RESUME · MATCHING SKILLS · SCORING…</div>
          </div>
        )}
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <ResultCard result={result} />
        </div>
      )}
    </div>
  )
}
