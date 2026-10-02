from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def generate():
    data = request.form.get("data", "").strip()
    filename = request.form.get("filename", "qr_code").strip() or "qr_code"
    if not data:
        return jsonify({"error": "Please enter text or a URL."}), 400

    safe_name = "".join(c for c in filename if c.isalnum() or c in ("-", "_")).strip() or "qr_code"
    img = qrcode.make(data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png", as_attachment=True,
                     download_name=f"{safe_name}.png")

if __name__ == "__main__":
    app.run(debug=True)
