# ColisDZ Backend (Django REST API)

This is the backend for the ColisDZ parcel delivery management platform. It provides a RESTful API for vendors, relay operators, and administrators to manage orders, relay points, users, and more.

## Features

- User authentication (JWT)
- Vendor, relay operator, and admin roles
- Order and parcel management
- Relay point management
- Employment applications
- CORS enabled for frontend integration

## Technology Stack

- Python 3.10+
- Django 5
- Django REST Framework
- SQLite (default, can be changed)

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Navigate to the backend directory:
   ```bash
   cd Ncs_backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

- By default, SQLite is used. The database file is `db.sqlite3`.
- To apply migrations:
  ```bash
  python manage.py migrate
  ```
- To load initial/seed data (if provided):
  ```bash
  python seed_data.py
  ```

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at [http://localhost:8000](http://localhost:8000).

### API Endpoints

- The API is organized by apps: `users`, `vendors`, `relay`, `orders`, `logistics`, `employment`, etc.
- Example endpoints:
  - `/api/auth/` — Authentication (login, register)
  - `/api/orders/` — Orders management
  - `/api/relay/` — Relay points
  - `/api/vendors/` — Vendor management
  - `/api/employment/` — Employment applications

> **Note:** See each app's `urls.py` for detailed routes.

### CORS

CORS is enabled for local frontend development. Adjust settings in `base/settings.py` as needed.

## Connecting with the Frontend

- Make sure the backend is running before starting the frontend.
- The frontend (React) is in the project root (`NCS_HACK`). See the main [README.md](../README.md) for frontend setup.

## Project Structure

- `manage.py` — Django entry point
- `requirements.txt` — Python dependencies
- `core/`, `users/`, `vendors/`, etc. — Django apps

## Admin Panel

- Access the Django admin at `/admin/` (create a superuser with `python manage.py createsuperuser`)

---

© 2025 wassely Team
