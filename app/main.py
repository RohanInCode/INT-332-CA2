from flask import Flask, request, render_template, redirect, url_for
import hashlib
from datetime import datetime

app = Flask(__name__)

file_registry = {}


def compute_hash(file_bytes):
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()


@app.route("/")
def home():
    return render_template("index.html", registry=file_registry)


@app.route("/register", methods=["POST"])
def register():
    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return redirect(url_for("home"))

    file_bytes = uploaded_file.read()
    file_hash = compute_hash(file_bytes)
    filename = uploaded_file.filename

    file_registry[filename] = {
        "hash": file_hash,
        "status": "Registered",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return redirect(url_for("home"))


@app.route("/verify", methods=["POST"])
def verify():
    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return redirect(url_for("home"))

    filename = uploaded_file.filename

    if filename not in file_registry:
        return redirect(url_for("home"))

    file_bytes = uploaded_file.read()
    current_hash = compute_hash(file_bytes)
    original_hash = file_registry[filename]["hash"]

    if current_hash == original_hash:
        status = "SAFE"
    else:
        status = "TAMPERED"

    file_registry[filename]["status"] = status
    file_registry[filename]["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template("index.html", registry=file_registry, result=status, filename=filename)


@app.route("/clear")
def clear():
    file_registry.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
