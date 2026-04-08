from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone
import requests
import os

app = Flask(__name__, template_folder=".")
CORS(app)

# 🔐 CONFIGURACIÓN SUPABASE
SUPABASE_URL = "https://ybkycakkwudoluirrcio.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlia3ljYWtrd3Vkb2x1aXJyY2lvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDkwODYsImV4cCI6MjA5MTIyNTA4Nn0.IoDGWdDVnOIBFTjnWD80fckOJzO4RshU8IfTtcu2xW8"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/data_alturas")
def data_alturas():
    url = f"{SUPABASE_URL}/rest/v1/autorreporte_alturas"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }

    r = requests.get(url, headers=headers)
    return jsonify(r.json())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/registro_ficha", methods=["POST", "OPTIONS"])
def registro_ficha():

    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json

    try:
        url = f"{SUPABASE_URL}/rest/v1/ficha_medica"

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "nombre": data["nombre"],
            "documento": data["documento"],
            "fecha_nacimiento": data["fecha_nacimiento"],
            "empresa": data["empresa"],
            "cargo": data["cargo"],
            "locacion": data["locacion"],
            "fecha_ingreso": data["fecha_ingreso"],
            "telefono": data["telefono"],
            "email": data["email"],
            "eps": data["eps"],
            "arl": data["arl"],

            "enfermedad_actual": data["enfermedad_actual"],
            "diagnostico": data["diagnostico"],
            "otra_enfermedad": data["otra_enfermedad"],
            "cirugias": data["cirugias"],
            "traumas": data["traumas"],
            "medicamentos": data["medicamentos"],
            "tipo_sangre": data["tipo_sangre"],
            "alergias": data["alergias"],
            "condiciones": data["condiciones"],
            "contacto_emergencia": data["contacto_emergencia"],

            "fechaRegistro": datetime.now(timezone.utc).isoformat()
        }

        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data_ficha")
def data_ficha():
    url = f"{SUPABASE_URL}/rest/v1/ficha_medica"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    r = requests.get(url, headers=headers)
    return jsonify(r.json())

@app.route("/registro_medico", methods=["POST","OPTIONS"])
def registro_medico():

    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json

    url = f"{SUPABASE_URL}/rest/v1/ficha_medica"

    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=data, headers=headers)

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)