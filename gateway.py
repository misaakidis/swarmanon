#!/usr/bin/env python3
"""Loopback-only, read-only bridge to our local Swarm gateway."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
import re

UPSTREAM = 'http://127.0.0.1:13000'
MAX_SIZE = 2 * 1024 * 1024
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path)
        if path.scheme or path.netloc or not re.fullmatch(r'/bzz/[0-9a-fA-F]{64}(?:/[^?#]*)?', path.path) or path.query:
            self.send_error(400, 'Expected /bzz/<64-character hex reference>/...')
            return
        try:
            with urlopen(Request(UPSTREAM + path.path, headers={'User-Agent': 'swarm-nym-prototype'}), timeout=30) as response:
                body = response.read(MAX_SIZE + 1)
                if len(body) > MAX_SIZE:
                    self.send_error(502, 'Response exceeds prototype limit')
                    return
                self.send_response(response.status)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/octet-stream'))
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except HTTPError as exc:
            self.send_error(exc.code, 'Swarm upstream returned an error')
        except (URLError, TimeoutError, OSError):
            self.send_error(502, 'Swarm upstream unavailable')
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', 18080), Handler).serve_forever()
