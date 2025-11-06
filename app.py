import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from io import StringIO
import csv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="templates")
    # Secret key for sessions
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    # SQLite database in instance folder
    db_path = os.path.join(app.instance_path, "cvms.sqlite3")
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # --- Auth helpers ---
    def require_login():
        if not session.get("user"):
            return redirect(url_for("login"))
        return None

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            # Default admin creds (override with env vars ADMIN_USER / ADMIN_PASS)
            admin_user = os.environ.get("ADMIN_USER", "admin")
            admin_pass = os.environ.get("ADMIN_PASS", "admin123")
            if username == admin_user and password == admin_pass:
                session["user"] = username
                flash("Logged in successfully.", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.", "error")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("Logged out.", "info")
        return redirect(url_for("login"))

    # --- Core routes ---
    @app.route("/")
    def dashboard():
        if (resp := require_login()) is not None:
            return resp
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        total_today = Visit.query.filter(Visit.check_in >= start, Visit.check_in <= end).count()
        inside_now = Visit.query.filter(Visit.check_out.is_(None)).count()
        checked_out_today = Visit.query.filter(Visit.check_out >= start, Visit.check_out <= end).count()
        hosts = Host.query.order_by(Host.name.asc()).all()
        return render_template("dashboard.html", total_today=total_today, inside_now=inside_now, checked_out_today=checked_out_today, hosts=hosts)

    @app.route("/visits/new", methods=["GET", "POST"])
    def visit_new():
        if (resp := require_login()) is not None:
            return resp
        if request.method == "POST":
            v_name = request.form.get("visitor_name", "").strip()
            v_phone = request.form.get("visitor_phone", "").strip()
            v_id = request.form.get("visitor_id", "").strip()
            purpose = request.form.get("purpose", "").strip()
            host_id = request.form.get("host_id")
            vehicle_no = request.form.get("vehicle_no", "").strip()
            if not v_name or not purpose or not host_id:
                flash("Visitor name, purpose, and host are required.", "error")
                return redirect(url_for("visit_new"))
            # Ensure visitor exists or create
            visitor = Visitor.query.filter_by(name=v_name, phone=v_phone).first()
            if visitor is None:
                visitor = Visitor(name=v_name, phone=v_phone, id_proof=v_id)
                db.session.add(visitor)
                db.session.flush()
            # Create visit
            visit = Visit(visitor_id=visitor.id, host_id=int(host_id), purpose=purpose, check_in=datetime.now(), vehicle_no=vehicle_no)
            db.session.add(visit)
            db.session.commit()
            flash("Visitor checked in successfully.", "success")
            return redirect(url_for("visits_list", status="inside"))
        hosts = Host.query.order_by(Host.name.asc()).all()
        return render_template("visit_new.html", hosts=hosts)

    @app.route("/visits")
    def visits_list():
        if (resp := require_login()) is not None:
            return resp
        # Filters
        status = request.args.get("status", "all")
        q = Visit.query.join(Visitor).join(Host)
        if status == "inside":
            q = q.filter(Visit.check_out.is_(None))
        elif status == "checkedout":
            q = q.filter(Visit.check_out.is_not(None))

        # Date range filters
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        if date_from:
            try:
                start = datetime.strptime(date_from, "%Y-%m-%d")
                q = q.filter(Visit.check_in >= start)
            except ValueError:
                pass
        if date_to:
            try:
                end = datetime.strptime(date_to, "%Y-%m-%d")
                end = datetime.combine(end, datetime.max.time())
                q = q.filter(Visit.check_in <= end)
            except ValueError:
                pass

        visits = q.order_by(Visit.check_in.desc()).all()
        return render_template("visits_list.html", visits=visits, status=status, date_from=date_from or "", date_to=date_to or "")

    @app.route("/visits/<int:visit_id>/checkout", methods=["POST"])
    def visit_checkout(visit_id):
        if (resp := require_login()) is not None:
            return resp
        visit = Visit.query.get_or_404(visit_id)
        if visit.check_out is None:
            visit.check_out = datetime.now()
            db.session.commit()
            flash("Visitor checked out.", "success")
        else:
            flash("Already checked out.", "info")
        return redirect(url_for("visits_list", status="inside"))

    @app.route("/hosts", methods=["GET", "POST"])
    def hosts_page():
        if (resp := require_login()) is not None:
            return resp
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            dept = request.form.get("department", "").strip()
            if not name:
                flash("Host name is required.", "error")
            else:
                db.session.add(Host(name=name, department=dept))
                db.session.commit()
                flash("Host added.", "success")
            return redirect(url_for("hosts_page"))
        hosts = Host.query.order_by(Host.name.asc()).all()
        return render_template("hosts.html", hosts=hosts)

    @app.route("/visitors")
    def visitors_page():
        if (resp := require_login()) is not None:
            return resp
        visitors = Visitor.query.order_by(Visitor.created_at.desc()).all()
        return render_template("visitors.html", visitors=visitors)

    @app.route("/export.csv")
    def export_csv():
        if (resp := require_login()) is not None:
            return resp
        q = Visit.query.join(Visitor).join(Host).order_by(Visit.check_in.desc()).all()
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(["Visit ID", "Visitor", "Phone", "ID Proof", "Host", "Department", "Purpose", "Vehicle No", "Check In", "Check Out"])
        for v in q:
            cw.writerow([
                v.id, v.visitor.name, v.visitor.phone or "",
                v.visitor.id_proof or "",
                v.host.name, v.host.department or "",
                v.purpose, v.vehicle_no or "",
                v.check_in.strftime("%Y-%m-%d %H:%M"),
                v.check_out.strftime("%Y-%m-%d %H:%M") if v.check_out else ""
            ])
        si.seek(0)
        return send_file(
            path_or_file=StringIO(si.read()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="visits_export.csv"
        )

    @app.route("/api/stats/today")
    def api_stats_today():
        if (resp := require_login()) is not None:
            return resp
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        return jsonify({
            "total_today": Visit.query.filter(Visit.check_in >= start, Visit.check_in <= end).count(),
            "inside_now": Visit.query.filter(Visit.check_out.is_(None)).count(),
            "checked_out_today": Visit.query.filter(Visit.check_out >= start, Visit.check_out <= end).count(),
        })

    return app

db = SQLAlchemy()

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    id_proof = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    visits = db.relationship("Visit", backref="visitor", lazy=True)

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120))
    visits = db.relationship("Visit", backref="host", lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitor.id"), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("host.id"), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    vehicle_no = db.Column(db.String(60))
    check_in = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    check_out = db.Column(db.DateTime)

if __name__ == "__main__":
    app = create_app()
    # Seed default hosts if none exist
    with app.app_context():
        if Host.query.count() == 0:
            db.session.add_all([
                Host(name="Prof. Sharma", department="Computer Science"),
                Host(name="Dr. Reddy", department="Mechanical"),
                Host(name="Admin Office", department="Administration"),
            ])
            db.session.commit()
    app.run(host="0.0.0.0", port=5000, debug=True)
