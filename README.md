# 🧠 Recursive Predictive Logic Engine (RPLE) v1.3

**“It doesn’t guess. It learns — and then it loops.”**  
A deterministic, self-refining insight engine that transforms raw operational data into structured, actionable intelligence.  
No cloud dependencies. No black-box AI. Just Python, Flask, and clarity.

---

## 🚀 Overview

The **RPLE** ingests structured metadata (CSV), identifies emerging patterns, filters noise, and outputs continuously improving predictions and insights.  
Each cycle compounds analytical clarity — meaning **the more you use it, the smarter it gets.**

Built for transparency, not mystery: every decision is logged, scored, and explainable.

---

## ⚙️ Core Capabilities

- 📊 **CSV Ingestion & Normalization** — feed any structured operational dataset  
- 🔁 **Recursive Insight Loop** — learns from every cycle, compounding precision  
- 🧩 **Constructive Feedback Engine** — outputs clear insights, not just numbers  
- 🧠 **Memory Reservoir** — tracks persisting vs. novel patterns over time  
- 🪶 **Lightweight Deployment** — pure Python + Flask, no external APIs or services

---

## 🧩 Architecture

```mermaid
graph TD
A[CSV Upload] --> B[Data Normalization]
B --> C[Pattern Detection & Scoring]
C --> D[Insight Generation]
D --> E[Human Feedback + Memory Reservoir]
E --> C
````

---

## 💻 How It Works

1. Upload a CSV file (any dataset with `value_1`, `value_2`, and optional `risk` columns).
2. The engine analyzes:

   * Trends
   * Correlation shifts
   * Anomalies
   * Risk alignments
3. It generates **insight cards** with:

   * Confidence
   * Novelty
   * Severity
   * Suggested actions
   * Status (🆕 *new* / ♻️ *persisting*)
4. The engine stores each insight in its memory reservoir for future comparison.

---

## 🔍 Example Insights

| Domain      | Insight                                               | Confidence | Novelty | Status |
| ----------- | ----------------------------------------------------- | ---------- | ------- | ------ |
| Primary     | Primary metric trending up                            | 0.86       | 0.82    | 🆕     |
| Correlation | Relationship between value_1 and value_2 strengthened | 0.72       | 0.75    | ♻️     |
| Anomaly     | Anomaly burst detected (3 spikes)                     | 0.91       | 0.88    | 🆕     |
| Risk        | Risk and primary metric are aligned (corr=0.52)       | 0.67       | 0.64    | 🆕     |

---

## 🧮 Installation & Run

```bash
git clone https://github.com/<your-handle>/recursive-logic-engine.git
cd recursive-logic-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)** and upload your dataset.

---

## 📈 Example Dataset

`sample_input.csv`

```csv
timestamp,value_1,value_2,risk
2025-10-01,10,12,0.20
2025-10-02,11,12,0.21
2025-10-03,13,13,0.22
2025-10-04,15,14,0.25
2025-10-05,18,14,0.30
2025-10-06,16,13,0.28
2025-10-07,19,15,0.33
2025-10-08,21,16,0.36
2025-10-09,24,17,0.40
```

---

## 🧠 Memory & Learning

Each loop stores a hashed summary of every insight in `insight_memory.json`.
Future runs detect whether insights are:

* **🆕 New:** unseen patterns
* **♻️ Persisting:** confirmed patterns continuing across cycles

This creates a real-time feedback model that grows smarter with use.

---

## 🧱 Tech Stack

* Python 3.9+
* Flask 3.x
* Pandas + NumPy
* JSON + Local Storage (no external API)
* SHA-256 integrity for insight memory

---

## 👨‍💻 Author

**Joseph Wells**
📍 Indianapolis, IN
📧 [joepwells95@gmail.com](mailto:joepwells95@gmail.com)
🔗 [Foxhunter Labs](https://github.com/FoxhunterLabs)

---

## 🧩 Related Systems

* 🦊 **Foxhunter Pro** — Human-Gated Reconnaissance & Ethical Autonomy System
* 🧬 **Enigma²** — Safety & Kill-Switch Engine
* 🛰️ **Swarm** — Deterministic Multi-Agent Coordination Framework

---

## ⚖️ License

MIT License © 2025 Joseph Wells
Use freely for educational and research purposes. Attribution required.

---

## 🧭 Tagline

> “Predictive clarity doesn’t just happen — it compounds.”

