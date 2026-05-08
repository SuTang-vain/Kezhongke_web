import http.server
import socketserver
import urllib.request
import os

PORT = 3000
API_TARGET_URL = "http://127.0.0.1:8000"

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def handle_request(self):
        # API Proxy Logic
        if self.path.startswith('/api/'):
            url = API_TARGET_URL + self.path
            req = urllib.request.Request(url, method=self.command)
            
            # Forward headers
            for key, value in self.headers.items():
                if key.lower() not in ['host']:
                    req.add_header(key, value)
            
            # Forward body
            if self.command in ['POST', 'PATCH']:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    req.data = self.rfile.read(content_length)

            try:
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    for key, value in response.headers.items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(response.read())
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                for key, value in e.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return

        # Nginx URL routing logic for static files
        if self.path == '/':
            self.path = '/home/code.html'
        elif self.path.strip('/') in ['grow', 'path', 'atelier', 'journal', 'about']:
            self.path = f'/{self.path.strip("/")}/code.html'
        elif self.path.strip('/') == 'auth':
            self.path = '/auth/index.html'

        return super().do_GET()

Handler = ProxyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌟 Local Dev Server running at http://localhost:{PORT}")
    print(f"↪️  Proxying /api/ requests to {API_TARGET_URL}")
    httpd.serve_forever()
