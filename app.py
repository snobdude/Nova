import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return jsonify({"error": "Groq API key is missing"}), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is empty"}), 400

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Nova, a friendly and intelligent AI assistant. Be helpful, natural, and conversational."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            },
            timeout=60
        )

        if not response.ok:
            return jsonify({
                "error": "Groq API error",
                "details": response.text[:500]
            }), response.status_code

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        return jsonify({"reply": answer})

    except requests.RequestException:
        return jsonify({"error": "Could not connect to Groq"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
