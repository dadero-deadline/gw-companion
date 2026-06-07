from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8000

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8'}
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

print('GW Companion (SERVE-ONLY, kein Rebuild) auf http://localhost:%d' % PORT)
HTTPServer(('localhost', PORT), Handler).serve_forever()
