"""FixFlow final: verified explain-and-fix chat with tuned defaults."""

from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Set OPENAI_API_KEY in your environment before running.")

client = OpenAI(api_key=api_key)

# Deliberate defaults for precise explain-and-fix replies.
FIXFLOW_MODEL = "gpt-4o-mini"
FIXFLOW_TEMPERATURE = 0.2
FIXFLOW_MAX_TOKENS = 500

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are FixFlow, a concise Python bug-fix assistant. "
            "Explain failures clearly and propose corrected code."
        ),
    }
]

app = Flask(__name__)


def explain_messages(code: str, error: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": (
                "Explain the error in this code without fixing it:\n\n"
                f"{code}\n\nError:\n\n{error}"
            ),
        }
    ]


def fix_messages(code: str, error: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": (
                "Fix this Python code based on the error. "
                "Return only the corrected code.\n\n"
                f"{code}\n\nError:\n\n{error}"
            ),
        }
    ]


def create_completion(messages: list[dict[str, str]]):
    return client.chat.completions.create(
        model=FIXFLOW_MODEL,
        messages=messages,
        temperature=FIXFLOW_TEMPERATURE,
        max_tokens=FIXFLOW_MAX_TOKENS,
    )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400

    conversation_history.append({"role": "user", "content": message})
    response = create_completion(conversation_history)
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply, "finish_reason": response.choices[0].finish_reason})


@app.post("/fix")
def fix():
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    error = (data.get("error") or "").strip()
    if not code or not error:
        return jsonify({"error": "code and error are required"}), 400

    explain_response = create_completion(explain_messages(code, error))
    explanation = explain_response.choices[0].message.content

    fix_response = create_completion(fix_messages(code, error))
    fixed_code = fix_response.choices[0].message.content

    conversation_history.append(
        {
            "role": "user",
            "content": f"Bug report:\n{code}\n\nError:\n{error}",
        }
    )
    conversation_history.append(
        {
            "role": "assistant",
            "content": (
                f"Explanation:\n{explanation}\n\n"
                f"Proposed fix:\n{fixed_code}"
            ),
        }
    )

    return jsonify(
        {
            "explanation": explanation,
            "fixed_code": fixed_code,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
