import React, { useState } from "react";

export default function LeoGame() {
  const [debris, setDebris] = useState(0.2);
  const [score, setScore] = useState(0);
  const [belief, setBelief] = useState(0.5); // probability opponent is hostile
  const [log, setLog] = useState([]);
  const [phase, setPhase] = useState("decision");
  const [lastCollision, setLastCollision] = useState(false);
  const [aiMode, setAiMode] = useState(false);

  function randomOpponentType() {
    return Math.random() < 0.5 ? "cooperative" : "aggressive";
  }

  function playTurn(action) {
    let opponentType = randomOpponentType();
    let newDebris = debris;
    let newScore = score;
    let message = `You chose ${action}. Opponent is hidden.`;

    // Subgame II: Bayesian Chicken
    if (action === "persist") {
      newScore += 1;
      newDebris += 0.05;
      if (opponentType === "aggressive") {
        message += " Opponent also persists → escalation risk!";
        if (Math.random() < 0.3) {
          message += " ⚠️ Collision!";
          newDebris += 0.3;
          setLastCollision(true);
          setPhase("attribution");
        }
      }
    } else {
      message += " You evaded (lost strategic value).";
      newScore -= 0.5;
    }

    // Subgame I: Responsibility / risky ops
    if (Math.random() < newDebris) {
      message += " Random debris interaction occurred.";
      newDebris += 0.1;
    }

    // Belief update (simple heuristic)
    let newBelief = belief;
    if (action === "persist") newBelief += 0.1;
    else newBelief -= 0.05;

    setBelief(Math.min(Math.max(newBelief, 0), 1));
    setDebris(Math.min(newDebris, 1));
    setScore(newScore);
    setLog([...log, message]);

    if (!lastCollision) {
      setPhase("decision");
    }
  }

  function attributionDecision(verify) {
    let message = "Attribution phase: ";
    let probAttribution = verify === "high" ? 0.6 : 0.2;

    if (aiMode) probAttribution *= 0.5; // AI reduces attribution

    if (Math.random() < probAttribution) {
      message += "Fault proven. Penalty applied.";
      setScore(score - 2);
    } else {
      message += "Attribution failed. No liability.";
    }

    setLog((prev) => [...prev, message]);
    setPhase("decision");
    setLastCollision(false);
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🚀 LEO POSG Game</h1>

      <div className="mb-4">
        <p>Debris (K): {debris.toFixed(2)}</p>
        <p>Score (Uᵢ): {score.toFixed(2)}</p>
        <p>Belief opponent hostile (μ): {belief.toFixed(2)}</p>
      </div>

      <div className="mb-4">
        <label className="mr-2">AI Acceleration</label>
        <input
          type="checkbox"
          checked={aiMode}
          onChange={() => setAiMode(!aiMode)}
        />
      </div>

      {phase === "decision" && (
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => playTurn("persist")}
            className="bg-red-500 text-white px-4 py-2 rounded"
          >
            Persist (Aggressive)
          </button>

          <button
            onClick={() => playTurn("evade")}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Evade (Safe)
          </button>
        </div>
      )}

      {phase === "attribution" && (
        <div className="flex gap-4 mb-4">
          <button
            onClick={() => attributionDecision("high")}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            High Verification (costly)
          </button>

          <button
            onClick={() => attributionDecision("low")}
            className="bg-gray-500 text-white px-4 py-2 rounded"
          >
            Low Verification
          </button>
        </div>
      )}

      <div className="bg-gray-100 p-3 rounded h-60 overflow-auto">
        {log.map((entry, i) => (
          <div key={i}>{entry}</div>
        ))}
      </div>
    </div>
  );
}
