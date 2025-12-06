#!/usr/bin/env python3
# app.py
import os
import json
import uuid
import logging
from pathlib import Path
from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string, abort

# Configure logging (structured-ish)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger("calc-app")

# Paths for persistence
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
HISTORY_DIR = DATA_DIR / "histories"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "please-set-secret")
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ---------- Helpers ----------
def get_session_id():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
        logger.debug(f"New session created: {session['sid']}")
    return session["sid"]

def history_file(session_id: str) -> Path:
    return HISTORY_DIR / f"{session_id}.json"

def load_history(session_id: str):
    p = history_file(session_id)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text())
    except Exception as e:
        logger.error("Failed to read history file", exc_info=e)
        return []

def save_history(session_id: str, history):
    p = history_file(session_id)
    try:
        p.write_text(json.dumps(history, indent=None))
    except Exception as e:
        logger.error("Failed to write history file", exc_info=e)

def compute(a, b, op):
    # a, b are floats
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
    raise ValueError("Unsupported operator")

def validate_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")
    if 'a' not in data or 'b' not in data or 'op' not in data:
        raise ValueError("Payload requires 'a', 'b' and 'op' fields")
    try:
        a = float(data['a'])
        b = float(data['b'])
    except Exception:
        raise ValueError("'a' and 'b' must be numbers")
    op = data['op']
    if op not in ['+', '-', '*', '/']:
        raise ValueError("Operator must be one of: +, -, *, /")
    return a, b, op

# ---------- Routes ----------
@app.get("/")
def home():
    # Simple HTML UI (form)
    return render_template_string("""
    <!doctype html>
    <html>
    <head><title>Flask Calculator</title></head>
    <body>
      <h1>Calculator (Flask)</h1>
      <form id="calc" method="post" action="/calculate">
        <input name="a" placeholder="Number A" required>
        <select name="op">
          <option value="+">+</option>
          <option value="-">-</option>
          <option value="*">*</option>
          <option value="/">/</option>
        </select>
        <input name="b" placeholder="Number B" required>
        <button type="submit">Compute</button>
      </form>
      <h2>History</h2>
      <div id="history"></div>
      <script>
        async function loadHistory() {
          const res = await fetch('/history');
          const h = await res.json();
          document.getElementById('history').innerText = JSON.stringify(h, null, 2);
        }
        document.getElementById('calc').addEventListener('submit', async (e) => {
          e.preventDefault();
          const form = new FormData(e.target);
          const payload = { a: form.get('a'), b: form.get('b'), op: form.get('op') };
          const r = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const data = await r.json();
          alert(JSON.stringify(data));
          loadHistory();
        });
        loadHistory();
      </script>
    </body>
    </html>
    """)

@app.post("/calculate")
def calculate():
    """
    Accepts JSON payload or form:
      { "a": number, "b": number, "op": "+|-|*|/" }
    Returns result and stores it in session history.
    """
    sid = get_session_id()
    try:
        if request.is_json:
            payload = request.get_json()
        else:
            # support form submit
            payload = { 'a': request.form.get('a'), 'b': request.form.get('b'), 'op': request.form.get('op') }
        a, b, op = validate_payload(payload)
    except ValueError as e:
        logger.info("Validation error: %s", e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Unexpected error parsing payload")
        return jsonify({"error": "Invalid payload"}), 400

    try:
        result = compute(a, b, op)
    except ZeroDivisionError as e:
        logger.info("Division by zero attempt, sid=%s", sid)
        return jsonify({"error": "Division by zero"}), 400
    except Exception as e:
        logger.exception("Computation failed")
        return jsonify({"error": "Computation error"}), 500

    entry = {
        "a": a,
        "b": b,
        "op": op,
        "result": result,
        "id": str(uuid.uuid4())
    }

    # persist to history
    history = load_history(sid)
    history.append(entry)
    save_history(sid, history)
    logger.info("Computed for sid=%s: %s %s %s = %s", sid, a, op, b, result)
    return jsonify(entry), 201

@app.get("/history")
def get_history():
    sid = get_session_id()
    history = load_history(sid)
    return jsonify(history)

@app.delete("/history")
def clear_history():
    sid = get_session_id()
    p = history_file(sid)
    try:
        if p.exists():
            p.unlink()
    except Exception as e:
        logger.error("Failed to delete history", exc_info=e)
        return jsonify({"error": "Could not clear history"}), 500
    return jsonify({"message": "history cleared"}), 200

@app.get("/health")
def health():
    return "OK", 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.exception("Server error")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") in ("1","true","True")
    app.run(host="0.0.0.0", port=5000, debug=debug)
