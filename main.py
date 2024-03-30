# Python code (app.py)
from flask import Flask, render_template, jsonify, request
import json
import requests
import dotenv
import os

app = Flask(__name__)
dotenv.load_dotenv()

Bearer = f"Bearer {os.getenv('EDEN_AI_KEY')}"
headers = {"Authorization": Bearer}

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/generateImages", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")
    url = "https://api.edenai.run/v2/image/generation"
    payload = {
        "providers": "amazon",
        "text": prompt,
        "resolution": "512x512",
        "fallback_providers": "",
        "num_images": 3
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    images = result['amazon']['items']
    image_urls = [n['image_resource_url'] for n in images]
    return jsonify({"images": image_urls})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
