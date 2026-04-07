from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone
import requests
import os

app = Flask(__name__, template_folder=".")
CORS(app)

# 🔐 CONFIGURACIÓN SUPABASE
SUPABASE_URL = "https://pcjpnogwigzcmetglbyw.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjanBub2d3aWd6Y21ldGdsYnl3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU1ODc5ODYsImV4cCI6MjA5MTE2Mzk4Nn0.vbuUAYfeWcy_BkY7cKvHlGfvSCUIEpEqlg_Ql1MfuM8"

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

@app.route("/registro_alturas", methods=["POST"])
def registro_alturas():
    data = request.json

    try:
        url = f"{SUPABASE_URL}/rest/v1/autorreporte_alturas"

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "nombre": data["nombre"],
            "documento": data["documento"],
            "empresa": data["empresa"],
            "base_pozo": data["base_pozo"],
            "cliente": data["cliente"],
            "eps": data["eps"],
            "arl": data["arl"],

            "tension": data.get("tension", ""),
            "frecuencia": data.get("frecuencia", ""),
            "oxigeno": data.get("oxigeno", ""),

            "certifica": data["certifica"],

            "pregunta1": data["preguntas"][0],
            "pregunta2": data["preguntas"][1],
            "pregunta3": data["preguntas"][2],
            "pregunta4": data["preguntas"][3],
            "pregunta5": data["preguntas"][4],
            "pregunta6": data["preguntas"][5],
            "pregunta7": data["preguntas"][6],
            "pregunta8": data["preguntas"][7],
            "pregunta9": data["preguntas"][8],
            "pregunta10": data["preguntas"][9],

            "firma_trabajador": data["firma_trabajador"],
            "firma_coordinador": data["firma_coordinador"],

            "nombre_trabajador": data["nombre_trabajador"],
            "doc_trabajador": data["doc_trabajador"],
            "rol_trabajador": data["rol_trabajador"],
            "fecha_trabajador": data["fecha_trabajador"],

            "nombre_coord": data["nombre_coord"],
            "doc_coord": data["doc_coord"],
            "rol_coord": data["rol_coord"],
            "fecha_coord": data["fecha_coord"],

            "fechaRegistro": datetime.now(timezone.utc).isoformat()
        }

        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)