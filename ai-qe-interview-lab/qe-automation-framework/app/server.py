#!/usr/bin/env python3
"""Mini Shop - tiny demo app under test (UI + JSON API, stdlib only)."""

import argparse
import json
import re
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ORDERS: dict[str, dict] = {}
INDEX_HTML = (Path(__file__).parent / "index.html").read_text()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body, ctype: str = "application/json") -> None:
        data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send(200, INDEX_HTML, "text/html")
        elif self.path == "/health":
            self._send(200, {"status": "ok"})
        elif m := re.fullmatch(r"/api/orders/([\w-]+)", self.path):
            order = ORDERS.get(m.group(1))
            if order:
                self._send(200, order)
            else:
                self._send(404, {"error": "order not found"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/orders":
            return self._send(404, {"error": "not found"})

        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "invalid json"})

        email = payload.get("email", "")
        total = payload.get("total")
        if not email or "@" not in email:
            return self._send(400, {"error": "email is required"})
        if not isinstance(total, (int, float)) or isinstance(total, bool) or total <= 0:
            return self._send(400, {"error": "total must be a positive number"})

        order_id = uuid.uuid4().hex[:8]
        order = {"id": order_id, "email": email, "total": total, "status": "CREATED"}
        ORDERS[order_id] = order
        self._send(201, order)

    def log_message(self, *args) -> None:  # keep test output clean
        pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Mini Shop running on http://localhost:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
