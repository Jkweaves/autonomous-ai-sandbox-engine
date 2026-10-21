# Autonomous Meta-Cognitive Self-Correction AI Engine

An autonomous multi-agent engineering framework that executes untrusted AI code inside a secure Docker container, captures system runtime telemetry, and uses a local vector database to achieve zero-token long-term memory recall.

## 🚀 Architectural Blueprint

* **The Actor:** Executes raw python scripts securely inside an isolated Docker sandbox.
* **The Sandbox:** Restricts network connectivity, caps CPU thresholds, limits memory allocations, and traps system stack traces natively.
* **The Critic (ChatGPT):** Evaluates runtime log crashes dynamically, maps alternative logic paths, and pushes code adjustments live.
* **Long-Term Storage (ChromaDB):** Persists successful logic overrides to a local vector collection, allowing the engine to flash past code configurations instantly on future runs without incurring API network delays or token billing costs.

## 📦 Local Prerequisites
* Windows 10/11
* Python 3.12+
* Docker Desktop
* OpenAI API Key

## 🛠️ Execution Layout
```powershell
pip install openai chromadb docker
python agent.py
```
