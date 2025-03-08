# OCPP Backend

This project is an **OCPP (Open Charge Point Protocol) backend** built using **Django and Django Channels**. It manages WebSocket connections from EV chargers and processes OCPP 1.6 messages.

## Features
- WebSocket-based communication with EV chargers using OCPP 1.6.
- Tracks charger sessions and handles heartbeat, boot notifications, and more.
- RESTful API for charger management.
- Simulator script (`ocpp_simulator.py`) to test the system.

## 🏗️ Folder Structure
```
ocpp_backend
├── chargers               # Charger app handling OCPP messages
│   ├── chargerSession.py  # Handles charger session state
│   ├── consumers.py       # WebSocket consumer for charger connections
│   ├── ocpp_handler.py    # Processes OCPP messages
│   ├── models.py          # Database models
│   ├── routing.py         # WebSocket routing
│   ├── views.py           # REST API views
│   ├── admin.py, apps.py, tests.py  # Django app files
├── ocpp_backend           # Main Django project folder
│   ├── settings.py        # Project settings
│   ├── asgi.py            # ASGI server configuration (WebSockets)
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI server configuration
├── ocpp_simulator.py      # Simulator for testing OCPP messages
├── manage.py              # Django management script
├── requirments.txt        # Dependencies
```

---
## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone git@github.com:Mostafa95/ocpp_module.git
cd ocpp_backend
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
```sh
python3 -m venv env
source env/bin/activate

pip install -r requirments.txt
```

### 3️⃣ Apply Migrations & Start Django Server
```sh
python manage.py migrate
python manage.py runserver
```
The Django server will start at `http://127.0.0.1:8000/`

---
## ⚡ Running the OCPP WebSocket Server
To enable WebSocket communication for chargers:
```sh
daphne -b 0.0.0.0 -p 8000 ocpp_backend.asgi:application -v2
```
This will listen for WebSocket connections at:
```
ws://127.0.0.1:8000/ws/ocpp/<charger_id>/
```

---
## 🏎️ Running the OCPP Simulator
You can simulate an EV charger connecting to the backend:
```sh
python ocpp_simulator.py
```
This will send test OCPP messages (e.g., BootNotification, Heartbeat) to the server.

---
## 📡 API Endpoints
### 🔹 **WebSocket Endpoint**
- `ws://127.0.0.1:8000/ws/ocpp/<charger_id>/`
  - Handles OCPP 1.6 messages
  - Expects JSON-formatted messages

### 🔹 **REST API Endpoints**
| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET    | `/chargers/` | List all chargers |
| GET    | `/chargers/<id>/status` | Retrieve charger details |
| GET    | `get_logs/`  | retrieve logs




For further issues, check the logs using:
```sh
tail -f logs/debug.log
```



