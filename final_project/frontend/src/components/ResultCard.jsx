export default function ResultCard({ result }) {
  if (!result) return null

  return (
    <div className="card">
      <div className="score-row">
        <div className="score-tile">
          <div className="num">{result.ats_score}%</div>
          <div className="lbl">ATS Match Score</div>
        </div>
        <div className="score-tile">
          <div className="num">{result.ml_rank_confidence}%</div>
          <div className="lbl">Rank Confidence</div>
        </div>
      </div>

      <div className="stamp-row">
        <div className="stamp-group">
          <h4>Cleared skills</h4>
          {result.skills_match.length === 0 && <span className="mono" style={{ fontSize: 12, color: 'var(--ink-soft)' }}>none matched</span>}
          {result.skills_match.map((s) => (
            <span key={s} className="stamp cleared">{s}</span>
          ))}
        </div>
        <div className="stamp-group">
          <h4>Missing skills</h4>
          {result.skills_missing.length === 0 && <span className="mono" style={{ fontSize: 12, color: 'var(--ink-soft)' }}>none missing</span>}
          {result.skills_missing.map((s) => (
            <span key={s} className="stamp void">{s}</span>
          ))}
        </div>
      </div>

      <h4 style={{ fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--ink-soft)', margin: '0 0 10px' }}>
        AI Feedback
      </h4>
      <div className="feedback-box">{result.explainable_feedback}</div>
    </div>
  )
}
