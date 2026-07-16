import { useState } from 'react'
import api from '../api'

export default function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const path = mode === 'login' ? '/auth/login' : '/auth/register'
      const body = mode === 'login' ? { email, password } : { name, email, password }
      const { data } = await api.post(path, body)
      localStorage.setItem('hiresense_token', data.access_token)
      localStorage.setItem('hiresense_name', data.name)
      onAuthenticated(data.name)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <h1 className="auth-title display">
          {mode === 'login' ? 'Welcome back' : 'Create your account'}
        </h1>
        <p className="auth-sub">
          {mode === 'login'
            ? 'Log in to scan resumes against your job descriptions.'
            : 'Set up an account to start screening candidates.'}
        </p>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={submit}>
          {mode === 'register' && (
            <>
              <label htmlFor="name">Full name</label>
              <input id="name" type="text" value={name} onChange={(e) => setName(e.target.value)} required />
            </>
          )}
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            required
          />

          <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}
          </button>
        </form>

        <p style={{ marginTop: 18, fontSize: 13, color: 'var(--ink-soft)' }}>
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button className="link-btn" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}>
            {mode === 'login' ? 'Sign up' : 'Log in'}
          </button>
        </p>
      </div>
    </div>
  )
}
