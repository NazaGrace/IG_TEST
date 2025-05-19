from typing import Union
from flask import Flask, request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

app = Flask(IG_TEST)
VERIFY_TOKEN = "igcallback_token"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Extract the GET params from Meta
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Check if verify token matches
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Forbidden", 403

    elif request.method == 'POST':
        # Handle the webhook events (e.g., messages)
        data = request.get_json()
        print("Webhook received:", data)
        return "EVENT_RECEIVED", 200
