from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/igcallback")
def root():
    return {"response": "Active!"}


#Generate or load your verify token
VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN") or secrets.token_urlsafe(32)
print(f"Your VERIFY_TOKEN is: {VERIFY_TOKEN}") 
# Print it once for setup

class MetaWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if parsed_url.path == "/webhook":
            mode = query_params.get("hub.mode", [None])[0]
            token = query_params.get("hub.verify_token", [None])[0]
            challenge = query_params.get("hub.challenge", [None])[0]

            if mode == "subscribe" and token == VERIFY_TOKEN:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(challenge.encode())
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Verification failed")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/webhook":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # Log or process the webhook payload
            print("Received webhook event:", body.decode())

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"EVENT_RECEIVED")
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MetaWebhookHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Meta Webhook server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

port = int(os.environ.get("PORT", 8000))
run(port=port)
