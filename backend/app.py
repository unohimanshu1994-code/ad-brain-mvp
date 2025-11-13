import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT = load_prompt("backend/prompts/system.txt")
EXAMPLE_PROMPT = load_prompt("backend/prompts/example.txt")
TEMPLATE_PROMPT = load_prompt("backend/prompts/template.txt")

@app.route("/generate", methods=["POST"])
def generate_ads():
    data = request.json or {}

    product = data.get("product", "")
    audience = data.get("audience", "")
    festival = data.get("festival", "None")

    user_prompt = TEMPLATE_PROMPT.format(
        product=product,
        audience=audience,
        festival=festival
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": EXAMPLE_PROMPT},
        {"role": "assistant", "content": "Okay, I will follow this style."},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0.7,
        max_tokens=800
    )

    text = response.choices[0].message["content"]

    return jsonify({"result": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
