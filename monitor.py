from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('logs')  # Переходим в папку с логами

port = 8080
server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
print(f"Откройте в браузере: http://localhost:{port}")
print("Файл error_distribution.png будет автоматически обновляться")
server.serve_forever()