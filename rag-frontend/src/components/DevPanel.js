import React from "react";

function DevPanel({ data }) {
  if (!data) return null;

  return (
    <div className="dev-panel">
      <div className="dev-panel-header">
        <div className="dev-panel-dot" />
        Dev Console
      </div>

      <div className="dev-label">Rewritten Query</div>
      <div className="dev-rewritten">{data.rewritten_query || "—"}</div>

      {data.scores?.length > 0 && (
        <>
          <div className="dev-label">Relevance Scores</div>
          {data.scores.map((s, i) => {
            const pct = Math.max((1 + s) * 100, 4);
            const isGood = s > -0.5;
            return (
              <div key={i} className="score-bar-wrapper">
                <div className="score-bar-label">
                  <span>Chunk {i + 1}</span>
                  <span>{s.toFixed(3)}</span>
                </div>
                <div className="score-bar-track">
                  <div
                    className="score-bar-fill"
                    style={{
                      width: `${pct}%`,
                      background: isGood
                        ? "linear-gradient(90deg, #00d4ff, #0099cc)"
                        : "linear-gradient(90deg, #7c5cfc, #5a3fd4)",
                    }}
                  />
                </div>
              </div>
            );
          })}
        </>
      )}

      {data.chunks?.length > 0 && (
        <>
          <div className="dev-label">Retrieved Chunks</div>
          {data.chunks.map((c, i) => (
            <div key={i} className="chunk">{c}</div>
          ))}
        </>
      )}
    </div>
  );
}

export default DevPanel;