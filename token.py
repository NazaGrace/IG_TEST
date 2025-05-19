from flask import Flask, request

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
      
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
  
