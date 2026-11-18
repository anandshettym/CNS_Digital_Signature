
import base64

from flask import Flask, render_template, request, jsonify

from crypto_utils import (
    calculate_hash,
    sign_file,
    verify_file
)

app = Flask(__name__)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Generate Digital Signature
@app.route("/sign", methods=["POST"])
def sign():

    if "file" not in request.files:
        return jsonify({"error": "Please select a file"}), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_data = uploaded_file.read()

    if not file_data:
        return jsonify({"error": "Empty file is not allowed"}), 400

    try:
        # Generate SHA-256 hash
        file_hash = calculate_hash(file_data)

        # Generate RSA digital signature
        digital_signature = sign_file(file_data)

        # Convert signature to Base64
        encoded_signature = base64.b64encode(
            digital_signature
        ).decode("utf-8")

        return jsonify({
            "message": "Digital signature generated successfully!",
            "filename": uploaded_file.filename,
            "hash": file_hash,
            "signature": encoded_signature
        })

    except Exception:
        return jsonify({
            "error": "Digital signature generation failed"
        }), 500


# Verify Digital Signature
@app.route("/verify", methods=["POST"])
def verify():

    if "file" not in request.files or "signature" not in request.files:
        return jsonify({
            "error": "Upload both file and signature"
        }), 400

    uploaded_file = request.files["file"]
    signature_file = request.files["signature"]

    file_data = uploaded_file.read()
    signature_text = signature_file.read()

    if not file_data or not signature_text:
        return jsonify({
            "error": "Empty file or signature"
        }), 400

    try:
        # Decode Base64 signature
        digital_signature = base64.b64decode(
            signature_text.strip(),
            validate=True
        )

        # Generate current file hash
        file_hash = calculate_hash(file_data)

        # Verify RSA digital signature
        is_valid = verify_file(
            file_data,
            digital_signature
        )

        if is_valid:
            return jsonify({
                "status": "Verified",
                "message": "Digital signature is valid. File integrity confirmed.",
                "hash": file_hash
            })

        return jsonify({
            "status": "Failed",
            "message": "Invalid signature. File may have been modified.",
            "hash": file_hash
        })

    except Exception:
        return jsonify({
            "status": "Failed",
            "message": "Invalid signature format or verification error."
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
