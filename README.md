🎓 College Visitor Management System

A simple, efficient web app built with Flask (Python) and HTML/CSS for managing campus visitors.

📘 Overview

The College Visitor Management System (CVMS) is a lightweight web application that helps colleges record and track visitors efficiently. It allows staff to log visitor details, assign meeting hosts (faculty or admin), and manage check-ins and check-outs digitally — replacing traditional paper registers.

Built using:

🐍 Backend: Python (Flask Framework)

💾 Database: SQLite (lightweight and auto-created)

🌐 Frontend: HTML, CSS, JavaScript

🧱 Architecture: MVC (Flask + Jinja2 templates)

🚀 Features

✅ Secure Login

Default admin: admin / admin123

Can be changed using environment variables:

export ADMIN_USER=myuser
export ADMIN_PASS=mypassword


✅ Visitor Check-In

Record name, phone, ID proof, vehicle number, purpose, and meeting host.

Prevents duplicate entries automatically.

✅ Check-Out System

Quickly mark visitors as checked out from the dashboard or visit list.

✅ Dashboard Analytics

See total visitors today, currently inside, and those who checked out.

✅ Manage Hosts

Add faculty or staff with department names.

✅ Visitor & Visit Records

View all past visitors and visits.

Filter visits by date or status (inside, checked-out, all).

✅ Export to CSV

Download complete visitor history for reporting or backup.

✅ Responsive UI

Works well on both desktop and mobile browsers.

🛠️ Tech Stack
Component	Technology
Frontend	HTML, CSS, Vanilla JavaScript
Backend	Python (Flask Framework)
Database	SQLite
Templating	Jinja2
ORM	Flask-SQLAlchemy
Hosting Ready	Works on Render, Railway, Heroku, or any WSGI-based server
📂 Project Structure
college_visitor_mgmt/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── visit_new.html
│   ├── visits_list.html
│   ├── hosts.html
│   └── visitors.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── instance/
    └── cvms.sqlite3   # auto-generated database

⚙️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/college_visitor_mgmt.git
cd college_visitor_mgmt

2️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate     # macOS/Linux
# On Windows: .venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python app.py

5️⃣ Access the App

Visit 👉 http://localhost:5000

Login credentials:

Username: admin
Password: admin123

🧠 Usage Flow

Login as admin.

Add hosts (professors/staff).

Check in visitors — capture name, purpose, and host.

Dashboard auto-updates with daily statistics.

Check out visitors when they leave.

Export CSV for attendance logs or audits.

📸 Screenshots (suggested to add)

You can include screenshots like:

Dashboard

New Visitor Form

Visit List

CSV Export Example

(Add them under a screenshots/ folder and reference here)

🔐 Environment Variables

You can override the default settings:

Variable	Description	Default
ADMIN_USER	Admin username	admin
ADMIN_PASS	Admin password	admin123
SECRET_KEY	Flask secret key	dev-secret-key

Example:

export ADMIN_USER=admin
export ADMIN_PASS=mysecurepass
export SECRET_KEY=somerandomsecret

🧱 Future Enhancements

📸 Visitor photo capture (via webcam or upload)

🧾 Visitor badge / pass print (PDF)

🔔 Email/SMS notification to host

🕒 Automatic check-out reminders

🧍 Role-based users (security, admin, front desk)

📊 Analytics dashboard with charts

🧑‍💻 Author

💼 GitHub Profile

💬 Built with ❤️ using Python & Flask

🪪 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it for educational or personal use.

Would you like me to generate a README badge section (e.g., Python version, Flask version, License, etc.) and GitHub-ready cover image/banner too? It’ll make your repo look professional.
