#!/usr/bin/env python3
"""MCP server: exposes the QE Copilot to any MCP client (Cursor, Claude, CI agents).

Client config:
    {
      "mcpServers": {
        "qe-copilot": {
          "command": "python3",
          "args": ["/path/to/qe-copilot/mcp_server.py"]
        }
      }
    }
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.server.fastmcp import FastMCP

from agent_graph import CI_ACTIONS, run_triage
from knowledge_base import retrieve

mcp = FastMCP("qe-copilot")


@mcp.tool()
def triage_failure(failure_text: str) -> dict:
    """Run the full agentic triage: classify, find similar incidents, recommend CI action."""
    # Rule-based classifier keeps MCP tool calls fast and dependency-light.
    return run_triage(failure_text, use_hf=False)


@mcp.tool()
def search_similar_incidents(query: str, top_k: int = 3) -> list[dict]:
    """Semantic search over the QE failure knowledge base (vector DB)."""
    return [
        {"id": c["id"], "metadata": c["metadata"], "summary": c["document"][:200]}
        for c in retrieve(query, top_k=top_k)
    ]


@mcp.tool()
def list_ci_decision_policy() -> dict:
    """Show which failure category maps to which advisory CI/CD action."""
    return dict(CI_ACTIONS)


if __name__ == "__main__":
    mcp.run()
