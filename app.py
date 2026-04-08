from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone
import requests

app = Flask(__name__, template_folder=".")
CORS(app)

# 🔐 SUPABASE
SUPABASE_URL = "https://ybkycakkwudoluirrcio.supabase.co"
SUPABASE_ANON_KEY = "TU_ANON_KEY_AQUI"

# 🏠 HOME
@app.route("/")
def home():
    return render_template("index.html")

# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 📥 OBTENER DATOS
@app.route("/data_ficha")
def data_ficha():
    url = f"{SUPABASE_URL}/rest/v1/ficha_medica"

    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }

    r = requests.get(url, headers=headers)

    return jsonify(r.json())

# 🚀 REGISTRO PRINCIPAL
@app.route("/registro_medico", methods=["POST", "OPTIONS"])
def registro_medico():

    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json

    try:
        url = f"{SUPABASE_URL}/rest/v1/ficha_medica"

        headers = {
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        payload = {
            "nombre": data["nombre"],
            "documento": data["documento"],
            "fecha_nacimiento": data["fecha_nacimiento"],
            "empresa": data["empresa"],
            "cargo": data["cargo"],
            "locacion": data["locacion"],
            "fecha_ingreso": data.get("fecha_ingreso"),
            "telefono": data["telefono"],
            "correo": data["correo"],
            "eps": data["eps"],
            "arl": data["arl"],

            "enfermedad_actual": data.get("enfermedad_actual"),
            "enfermedades": data.get("enfermedades"),
            "otra_enfermedad": data.get("otra_enfermedad"),
            "cirugias": data.get("cirugias"),
            "traumas": data.get("traumas"),
            "medicamentos": data.get("medicamentos"),
            "sangre": data["sangre"],
            "alergias": data.get("alergias"),
            "condicion": data.get("condicion"),
            "emergencia": data["emergencia"],

            "fecha_registro": datetime.now(timezone.utc).isoformat()
        }

        print("📤 ENVIANDO A SUPABASE:")
        print(payload)

        r = requests.post(url, json=payload, headers=headers)

        print("📥 RESPUESTA SUPABASE:", r.text)

        r.raise_for_status()

        return jsonify({"ok": True})

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)