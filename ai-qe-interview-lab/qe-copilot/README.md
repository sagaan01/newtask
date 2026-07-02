# QE Copilot — AI-Powered Failure Triage Agent

One project covering every bullet of the "AI, LLMs & Agentic Systems" JD category:

| JD requirement | Where it lives |
|---|---|
| LLMs + prompt engineering | `src/llm_client.py` (guardrailed system prompt, temperature 0) |
| RAG + vector DB | `src/knowledge_base.py` (ChromaDB embeddings + semantic retrieval) |
| Model evaluation | `src/evaluate.py` (golden set, precision@3, accuracy, CI gate) |
| LangChain | `src/llm_client.py` (`ChatPromptTemplate`) |
| HuggingFace Transformers | `src/classifier.py` (zero-shot DistilBERT-MNLI classifier) |
| OpenAI / Ollama APIs | `src/llm_client.py` (one client, env-switchable provider) |
| LangGraph agentic framework | `src/agent_graph.py` (state graph with conditional routing) |
| GenAI QE solution / autonomous workflow | full pipeline: classify -> retrieve -> analyze -> decide |
| MCP-driven automation | `mcp_server.py` (FastMCP server, 3 tools) |
| CI/CD decision intelligence | `CI_ACTIONS` policy + confidence gate in `agent_graph.py` |

## What it does

Feed it a test failure. It:

1. **Classifies** the failure (HuggingFace zero-shot; rule fallback) — flaky-ui, product-defect, locator-issue, async-timing, infra
2. **Retrieves** the 3 most similar past incidents from a vector DB (RAG)
3. **Generates** a grounded triage analysis (OpenAI/Ollama; offline fallback)
4. **Decides** an advisory CI action (e.g. `block_merge_and_file_defect`) — or routes to `human_review` when confidence is low
5. **Reports** everything with citations

## Run it

```bash
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu   # optional, for HF classifier

python main.py --ingest            # build the vector index
python main.py --samples --no-hf   # triage 4 sample failures (fast, rule-based)
python main.py --samples           # same with HuggingFace classifier
python main.py "your failure text here"
python main.py --retrieve-only "refund stuck in pending"

python src/evaluate.py             # golden-set eval gate (exit 1 = block deploy)
```

### With a real LLM

```bash
export OPENAI_API_KEY=sk-...                      # OpenAI
# or point the same client at local Ollama:
export LLM_BASE_URL=http://localhost:11434/v1
export LLM_MODEL=llama3.1
```

### As an MCP server

```json
{
  "mcpServers": {
    "qe-copilot": {
      "command": "python3",
      "args": ["/path/to/qe-copilot/mcp_server.py"]
    }
  }
}
```

Tools exposed: `triage_failure`, `search_similar_incidents`, `list_ci_decision_policy`.

## Architecture

```
failure text
     |
     v
[classify]  HuggingFace zero-shot -> hybrid rule fallback
     |
     v
[retrieve]  ChromaDB vector search over past incidents (RAG)
     |
     v
[generate]  LangChain prompt -> OpenAI/Ollama (or offline template)
     |
     v
[decide]    confidence >= 0.6 -> auto CI action
     |       confidence <  0.6 -> human_review
     v
[report]    JSON: category, citations, analysis, ci_action (advisory)
```

Orchestrated by LangGraph; exposed to any MCP client via FastMCP.

## Design guardrails

- Prompt is context-only ("do not invent"), temperature 0
- Every answer cites incident IDs — verifiable in seconds
- Low confidence always routes to a human
- CI actions are **advisory**; deterministic gates still decide merges
- Eval gate (`evaluate.py`) blocks deploys if retrieval/classification regress
