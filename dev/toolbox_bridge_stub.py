#!/usr/bin/env python3
"""
Lightweight local HTTP stub to prototype a connection between
the Guild Wars Companion page (browser) and a future GWToolbox++ plugin.

Run locally:
  python dev/toolbox_bridge_stub.py --port 61337

Then from the page (or browser console):
  fetch('http://127.0.0.1:61337/ping').then(r=>r.json()).then(console.log)

Endpoints (CORS enabled):
  GET  /ping                    -> { ok: true, name: 'stub', version: '0.1' }
  GET  /status                  -> simple example state
  POST /chat {msg}              -> prints message to stdout, returns ok
  POST /progress {id,done}      -> echoes back; placeholder for future sync

This mimics what a GWToolbox++ plugin could expose later on localhost.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import argparse


class StubHandler(BaseHTTPRequestHandler):
    server_version = "GWCompanionStub/0.1"

    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/ping"):
            self._json({"ok": True, "name": "gwtoolbox-bridge-stub", "version": "0.1"})
            return
        if self.path.startswith("/status"):
            data = {
                "ok": True,
                "zone": "Isle of the Nameless",
                "party_size": 1,
                "player_prof": "monk",
            }
            self._json(data)
            return
        self.send_response(404)
        self._set_cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(body.decode("utf-8") or "{}")
        except Exception:
            payload = {}

        if self.path.startswith("/chat"):
            msg = payload.get("msg", "")
            print(f"[stub] CHAT -> {msg}")
            self._json({"ok": True})
            return

        if self.path.startswith("/progress"):
            # Example echo; in a real plugin, this would forward to the app
            self._json({"ok": True, "echo": payload})
            return

        self.send_response(404)
        self._set_cors()
        self.end_headers()

    def _json(self, data, code=200):
        blob = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self._set_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=61337)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    httpd = HTTPServer((args.host, args.port), StubHandler)
    print(f"GWToolbox bridge stub listening on http://{args.host}:{args.port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()

