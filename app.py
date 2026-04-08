from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import requests

app = Flask(__name__, template_folder=".")
CORS(app)

# 🔐 SUPABASE
SUPABASE_URL = "https://ybkycakkwudoluirrcio.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlia3ljYWtrd3Vkb2x1aXJyY2lvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDkwODYsImV4cCI6MjA5MTIyNTA4Nn0.IoDGWdDVnOIBFTjnWD80fckOJzO4RshU8IfTtcu2xW8"

def hora_colombia():
    return (datetime.utcnow() - timedelta(hours=5)).isoformat()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 🔹 INSERTAR DATOS
@app.route("/registro_medico", methods=["POST", "OPTIONS"])
def registro_medico():

    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        data = request.json

        url = f"{SUPABASE_URL}/rest/v1/ficha_medica"

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        data["fecha_registro"] = hora_colombia()

        print("📤 ENVIANDO:", data)

        r = requests.post(url, json=data, headers=headers)

        print("📥 RESPUESTA:", r.text)

        r.raise_for_status()

        return jsonify({"ok": True})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500


# 🔹 CONSULTAR DATOS
@app.route("/data_ficha")
def data_ficha():

    url = f"{SUPABASE_URL}/rest/v1/ficha_medica?select=*"

    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }

    r = requests.get(url, headers=headers)
    return jsonify(r.json())


if __name__ == "__main__":
    app.run(debug=True)