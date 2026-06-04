import http.server
import socketserver
import os
import threading
from websockets.asyncio.server import serve
import asyncio

# --- Configuration ---
PORT = 9000
WS_PORT = 9005# Make sure this matches your script.js

# 1. The Web Server (serves your index.html)
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_web():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"✅ Website online: http://192.168.1.12:{PORT}")
        httpd.serve_forever()

# 2. The Chat Engine (WebSocket)
async def chat_handler(ws):
    print("User connected to Chat Engine")
    async for msg in ws:
        await ws.send(msg) # Echoes the message back

async def run_ws():
    print(f"✅ Chat Engine online: ws://192.168.1.12:{WS_PORT}")
    async with serve(chat_handler, "0.0.0.0", WS_PORT):
        await asyncio.Future()

# Start both
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(run_ws())