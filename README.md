# College Visitor Management System (Flask + SQLite)

A clean, production-ready starter for managing visitor check-ins, check-outs, hosts, and daily stats.

## Features
- Secure login (default: `admin` / `admin123`, override with env vars)
- New visitor check-in (name, phone, ID proof, vehicle, purpose, host)
- Check-out flow
- Dashboard stats (visitors today, inside now, checked-out today)
- Manage hosts (name + department)
- Visitors directory
- Filterable visit list by status and date range
- CSV export
- SQLite database auto-created in the `instance/` folder

## Quick Start

```bash
# 1) (Optional) set admin creds
export ADMIN_USER=admin
export ADMIN_PASS=admin123

# 2) Create venv and install deps
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3) Run the app
python app.py
# Visit http://localhost:5000 (login with admin/admin123)
```

## Project Structure
```
.
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── hosts.html
│   ├── login.html
│   ├── visit_new.html
│   ├── visitors.html
│   └── visits_list.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── instance/
    └── cvms.sqlite3  (auto-created)
```

## Notes
- Change the `SECRET_KEY` by setting env var `SECRET_KEY` for production.
- To reset the database, delete `instance/cvms.sqlite3` and restart.
- For deployment (gunicorn + nginx), use `create_app()` factory and WSGI.
```

