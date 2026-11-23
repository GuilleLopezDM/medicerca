# 🩺 MediCerca — Interactive Medical Directory

[![Tests](https://github.com/GuilleLopezDM/medicerca/actions/workflows/tests.yml/badge.svg)](https://github.com/GuilleLopezDM/medicerca/actions/workflows/tests.yml)

🇪🇸 [Versión en español](README.md)

> Hackathon 2025 · Python + Flask + SQLite + Tailwind CSS + Leaflet.js

**MediCerca** is a web platform to find medical professionals in Paraguay. Users can search by specialty and city, see each doctor's office on an interactive map and read reviews from other patients.

Built by a team of developers using a feature-branch Git workflow and pull requests.

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Doctor directory** | Search and filters by specialty and city |
| 🗺️ **Interactive map** | Leaflet.js with office markers and a preview on click |
| 📍 **Office location** | Doctors set their office location by clicking on the map |
| 🧭 **Directions** | Detects the user's location and draws the route to the office |
| ⭐ **Ratings & reviews** | 1–5 star system with automatic average recalculation |
| 🔐 **Authentication** | Sign up and login with roles (patient / doctor / admin) |
| 🛠️ **Admin panel** | User and doctor management |
| 📧 **Email** | Separate transactional emails for patients and doctors |
| 🎓 **Full profile** | License number, university, hospital, experience, bio and profile photo |

## 🛠️ Tech stack

```
Backend:   Python 3.11 + Flask 3.0
Database:  SQLite (Flask-SQLAlchemy)
Auth:      Flask-Login + Werkzeug
Frontend:  Jinja2 + Tailwind CSS (CDN)
Map:       Leaflet.js + OpenStreetMap (no API key)
Testing:   pytest + GitHub Actions
Docker:    python:3.11-slim + gunicorn
```

## 🚀 Getting started

```bash
git clone https://github.com/GuilleLopezDM/medicerca.git
cd medicerca

python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env         # Windows: copy .env.example .env
python seeds.py              # load sample data
flask run
```

Open **http://127.0.0.1:5000**

## 🐳 Docker

```bash
docker build -t medicerca .
docker run -p 5000:5000 medicerca
```

On startup the container loads the sample data and serves the app with gunicorn at **http://localhost:5000**.

## 👤 Sample users

`python seeds.py` creates 10 doctors (3 reviews each) and 10 patients. Some examples:

| Email | Password | Role |
|---|---|---|
| `carlos.benitez@medicerca.com` | `medico1234` | Doctor — Cardiology |
| `maria.ramirez@medicerca.com` | `medico1234` | Doctor — Pediatrics |
| `juan.rios@gmail.com` | `paciente1234` | Patient |

## 🧪 Tests

```bash
pytest -v
```

20 tests (authentication, public routes, sign-up and doctors) run against an in-memory SQLite database. GitHub Actions runs them on every push and pull request, and also checks that the Docker image builds.

For the project structure, team roles and Git workflow, see the [Spanish README](README.md).
