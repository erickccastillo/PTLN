#!/usr/bin/env python3
import json
import os
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, 'jsf_mafigo_db.json')
PORT = int(os.environ.get('JSF_PORT', '8080'))
LOCK = threading.Lock()
DEFAULT = {"eventos":[],"atletas":[],"clubes":[],"inscripciones":[],"resultados":[]}

def load_db():
    with LOCK:
        if not os.path.exists(DB):
            return dict(DEFAULT)
        try:
            with open(DB, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return dict(DEFAULT)
            for k, v in DEFAULT.items():
                data.setdefault(k, v)
            return data
        except Exception:
            return dict(DEFAULT)

def save_db(data):
    tmp = DB + '.tmp'
    with LOCK:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DB)

class Handler(SimpleHTTPRequestHandler):
    def end_json(self, code, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            self.end_json(200, {"ok": True, "service": "JSF & MAFIGO SPORT SYSTEMS", "port": PORT})
            return
        if path == '/api/state':
            self.end_json(200, load_db())
            return
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != '/api/state':
            self.end_json(404, {"ok": False, "error": "Not found"})
            return
        try:
            n = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(n)
            data = json.loads(body.decode('utf-8'))
            if not isinstance(data, dict):
                raise ValueError('Estado inválido')
            for k, v in DEFAULT.items():
                data.setdefault(k, v)
            save_db(data)
            self.end_json(200, {"ok": True})
        except Exception as e:
            self.end_json(400, {"ok": False, "error": str(e)})

    def log_message(self, fmt, *args):
        print('[JSF SERVER] ' + (fmt % args))

if __name__ == '__main__':
    os.chdir(BASE)
    server = ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    print('==============================================')
    print(' JSF & MAFIGO SPORT SYSTEMS - SERVIDOR CENTRAL')
    print('==============================================')
    print(f' Laptop: http://localhost:{PORT}')
    print(f' Red local: http://IP-DE-LA-LAPTOP:{PORT}')
    print(' Base de datos: jsf_mafigo_db.json')
    print(' Presiona Ctrl+C para detener.')
    server.serve_forever()
