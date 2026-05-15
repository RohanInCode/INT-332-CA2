# Import Flask and related tools to build the web app
from flask import Flask, request, render_template, redirect, url_for

# Import hashlib — Python's built-in library for hashing (no pip install needed)
import hashlib

# Import datetime so we can record the time each file was registered or verified
from datetime import datetime

# Create the Flask application object — this IS the web app
app = Flask(__name__)

# This dictionary acts as our in-memory "database"
# Key = filename (string), Value = dict with hash, status, and time
file_registry = {}

# ─────────────────────────────────────────────
# HELPER FUNCTION — compute SHA256 hash
# ─────────────────────────────────────────────

def compute_hash(file_bytes):
    # Create a new SHA256 hash object from hashlib
    sha256 = hashlib.sha256()

    # Feed the raw file bytes into the hash object
    sha256.update(file_bytes)

    # Return the hex digest — a 64-character string representing the hash
    return sha256.hexdigest()

# ─────────────────────────────────────────────
# ROUTE 1 — Home Page  ( GET / )
# ─────────────────────────────────────────────

@app.route("/")  # This decorator maps the URL "/" to the function below
def home():
    # Pass the current registry to the template so it can display history
    return render_template("index.html", registry=file_registry)

# ─────────────────────────────────────────────
# ROUTE 2 — Register File  ( POST /register )
# ─────────────────────────────────────────────

@app.route("/register", methods=["POST"])  # Only accept POST requests (form submissions)
def register():
    # Get the uploaded file from the HTML form field named "file"
    uploaded_file = request.files.get("file")

    # If no file was uploaded, go back to the home page
    if not uploaded_file:
        return redirect(url_for("home"))

    # Read the raw bytes from the uploaded file
    file_bytes = uploaded_file.read()

    # Compute the SHA256 hash of those bytes
    file_hash = compute_hash(file_bytes)

    # Get the original filename from the uploaded file object
    filename = uploaded_file.filename

    # Store the file's hash and metadata in our in-memory dictionary
    file_registry[filename] = {
        "hash": file_hash,          # The SHA256 hash string
        "status": "Registered",     # Current status label
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp as a readable string
    }

    # Redirect back to the home page after registering
    return redirect(url_for("home"))

# ─────────────────────────────────────────────
# ROUTE 3 — Verify File  ( POST /verify )
# ─────────────────────────────────────────────

@app.route("/verify", methods=["POST"])  # Only accept POST requests
def verify():
    # Get the uploaded file from the form field named "file"
    uploaded_file = request.files.get("file")

    # If no file was provided, redirect to home
    if not uploaded_file:
        return redirect(url_for("home"))

    # Get the filename from the uploaded file object
    filename = uploaded_file.filename

    # Check if this file has been registered before — if not, redirect to home
    if filename not in file_registry:
        return redirect(url_for("home"))

    # Read the raw bytes of the uploaded file to recompute its hash
    file_bytes = uploaded_file.read()

    # Compute the SHA256 hash of the current version of the file
    current_hash = compute_hash(file_bytes)

    # Retrieve the original hash that was saved during registration
    original_hash = file_registry[filename]["hash"]

    # Compare the current hash with the original hash
    if current_hash == original_hash:
        # Hashes match → file has NOT been changed → it is SAFE
        status = "SAFE"
    else:
        # Hashes do NOT match → file content has changed → it is TAMPERED
        status = "TAMPERED"

    # Update the registry with the new status and verification timestamp
    file_registry[filename]["status"] = status
    file_registry[filename]["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pass the verification result to the template along with the registry
    return render_template("index.html", registry=file_registry, result=status, filename=filename)

# ─────────────────────────────────────────────
# ROUTE 4 — Clear History  ( GET /clear )
# ─────────────────────────────────────────────

@app.route("/clear")  # Maps /clear URL to the function below
def clear():
    # Remove all entries from the dictionary — wipes the in-memory history
    file_registry.clear()

    # Redirect back to the home page after clearing
    return redirect(url_for("home"))

# ─────────────────────────────────────────────
# ENTRY POINT — run with: python main.py
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Start the Flask development server on all interfaces (0.0.0.0) at port 5000
    # debug=True gives helpful error pages during development
    app.run(host="0.0.0.0", port=5000, debug=True)
