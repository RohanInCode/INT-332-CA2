# 🔐 File Integrity Checker

A beginner-friendly **File Integrity Checker** web application built with **Python + Flask**.  
It uses **SHA-256 hashing** to detect whether a file has been tampered with after registration.

---

## 📌 What It Does

- Upload any file and **register** its SHA-256 hash
- **Verify** the same file later to check if it has been modified
- Shows a **GREEN alert** if the file is safe (unchanged)
- Shows a **RED alert** if the file has been tampered with (hash mismatch)
- Maintains a **history table** of all registered/verified files

---

## 🗂️ Project Structure

```
devops_Ca-2/
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
└── app/
    ├── main.py                  # Flask application (4 routes)
    └── templates/
        └── index.html           # Single-page UI (dark theme)
```

---

## ⚙️ How It Works

```
1. User uploads a file → Flask reads the bytes → SHA-256 hash is computed
2. Hash is stored in memory (Python dictionary)
3. User uploads the same file again → new hash is computed
4. New hash is compared with the stored hash
5. Match = SAFE ✅ | Mismatch = TAMPERED 🚨
```

### SHA-256 Hashing (Python built-in — no extra libraries)
```python
import hashlib
sha256 = hashlib.sha256()
sha256.update(file_bytes)
hash_value = sha256.hexdigest()  # 64-character hex string
```

---

## 🚀 Running Locally (Python)

### Prerequisites
- Python 3.10 or higher installed

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/RohanInCode/INT-332-CA2.git
cd INT-332-CA2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
cd app
python main.py
```

Open your browser at → **http://localhost:5000**

---

## 🐳 Running with Docker

### Prerequisites
- Docker Desktop installed and running
- Internet connection (to pull base image first time)

### Steps
```bash
# 1. Build the Docker image
docker build -t file-integrity-checker .

# 2. Run the container
docker run -p 5000:5000 file-integrity-checker
```

Open your browser at → **http://localhost:5000**

### Stop the container
```bash
docker ps                    # get container ID
docker stop <container-id>
```

---

## 🔁 CI/CD Pipeline (GitHub Actions)

The `.github/workflows/ci.yml` file runs **3 jobs** automatically on every push to `main`:

| Job | What it does |
|-----|-------------|
| **Test** | Sets up Python, installs deps, runs `pytest --co -q` |
| **Docker Build** | Builds the Docker image and tags it with the commit SHA |
| **Docker Push** | Logs into Docker Hub and pushes the image |

### Setting up Docker Hub Secrets

Go to: **GitHub Repo → Settings → Secrets and variables → Actions**

| Secret Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Access token from hub.docker.com → Account Settings → Security |

---

## 🔬 Tamper Detection Demo

```
Step 1 → Create a text file (e.g. notes.txt) with some content
Step 2 → Go to http://localhost:5000
Step 3 → Click "Register Hash" → upload notes.txt
         Status shows: 🔒 Registered

Step 4 → Open notes.txt → change the text → Save

Step 5 → Click "Verify Integrity" → upload the modified notes.txt
         Result: 🚨 RED ALERT — TAMPERED
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web framework |
| `gunicorn` | Production WSGI server (used in Docker) |
| `pytest` | Test runner (used in CI pipeline) |
| `hashlib` | SHA-256 hashing — **built into Python, no install needed** |

---

## 🛡️ Security Features

- **Non-root Docker user** — container runs as `appuser`, not root
- **SHA-256 hashing** — cryptographically secure, collision-resistant
- **In-memory storage** — no database, no persistent attack surface
- **Gunicorn** — production-grade server instead of Flask dev server

---

## 👨‍💻 Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-orange?logo=githubactions)
