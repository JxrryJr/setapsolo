"""Supervisor Finder: Flask routes, validation and SQLite persistence."""

from __future__ import annotations

import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="development-only-change-this-key",
        DATABASE=str(BASE_DIR / "instance" / "supervisor_finder.db"),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        schema = (BASE_DIR / "schema.sql").read_text()
        db.executescript(schema)
        if db.execute("SELECT COUNT(*) FROM staff").fetchone()[0] == 0:
            seed_data(db)
        db.commit()

    def staff_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "staff_id" not in session:
                flash("Please sign in as a staff member to access that page.", "warning")
                return redirect(url_for("login", next=request.path))
            return view(*args, **kwargs)
        return wrapped

    def owned_project_or_404(project_id):
        project = get_db().execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if project is None:
            abort(404)
        if project["staff_id"] != session["staff_id"]:
            abort(403)
        return project

    @app.route("/")
    def home():
        db = get_db()
        interests = db.execute("SELECT DISTINCT name FROM interests ORDER BY name").fetchall()
        latest_projects = db.execute(
            """SELECT p.*, s.full_name, s.department FROM projects p
               JOIN staff s ON s.id = p.staff_id ORDER BY p.id DESC LIMIT 3"""
        ).fetchall()
        return render_template("home.html", interests=interests, latest_projects=latest_projects)

    @app.route("/staff")
    def staff_directory():
        db = get_db()
        query = request.args.get("q", "").strip()
        interest = request.args.get("interest", "").strip()
        sql = "SELECT DISTINCT s.* FROM staff s LEFT JOIN interests i ON i.staff_id=s.id WHERE 1=1"
        params = []
        if query:
            sql += " AND (s.full_name LIKE ? OR s.department LIKE ? OR s.bio LIKE ?)"
            like = f"%{query}%"
            params.extend([like, like, like])
        if interest:
            sql += " AND i.name = ?"
            params.append(interest)
        sql += " ORDER BY s.full_name"
        staff = db.execute(sql, params).fetchall()
        interests = db.execute("SELECT DISTINCT name FROM interests ORDER BY name").fetchall()
        return render_template("staff_directory.html", staff=staff, interests=interests, query=query, selected_interest=interest)

    @app.route("/staff/<int:staff_id>")
    def staff_profile(staff_id):
        db = get_db()
        staff = db.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
        if staff is None:
            abort(404)
        interests = db.execute("SELECT * FROM interests WHERE staff_id = ? ORDER BY name", (staff_id,)).fetchall()
        projects = db.execute("SELECT * FROM projects WHERE staff_id = ? ORDER BY id DESC", (staff_id,)).fetchall()
        return render_template("staff_profile.html", staff=staff, interests=interests, projects=projects)

    @app.route("/projects/<int:project_id>")
    def project_detail(project_id):
        db = get_db()
        project = db.execute(
            "SELECT p.*, s.full_name, s.department, s.email FROM projects p JOIN staff s ON s.id=p.staff_id WHERE p.id=?",
            (project_id,),
        ).fetchone()
        if project is None:
            abort(404)
        saved = project_id in session.get("saved_projects", [])
        return render_template("project_detail.html", project=project, saved=saved)

    @app.post("/projects/<int:project_id>/save")
    def toggle_saved_project(project_id):
        if get_db().execute("SELECT id FROM projects WHERE id=?", (project_id,)).fetchone() is None:
            abort(404)
        saved = session.get("saved_projects", [])
        if project_id in saved:
            saved.remove(project_id)
            flash("Project removed from your saved list.", "info")
        else:
            saved.append(project_id)
            flash("Project saved for this browsing session.", "success")
        session["saved_projects"] = saved
        return redirect(url_for("project_detail", project_id=project_id))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            staff = get_db().execute("SELECT * FROM staff WHERE email=?", (email,)).fetchone()
            # Prototype-only comparison: production uses a salted password hash or SSO.
            if staff and staff["password"] == password:
                session.clear()
                session["staff_id"] = staff["id"]
                session["staff_name"] = staff["full_name"]
                flash(f"Welcome back, {staff['full_name']}.", "success")
                return redirect(request.args.get("next") or url_for("dashboard"))
            flash("Email or password was not recognised.", "error")
        return render_template("login.html")

    @app.post("/logout")
    def logout():
        session.clear()
        flash("You have been signed out.", "info")
        return redirect(url_for("home"))

    @app.route("/dashboard")
    @staff_required
    def dashboard():
        db = get_db()
        staff = db.execute("SELECT * FROM staff WHERE id=?", (session["staff_id"],)).fetchone()
        interests = db.execute("SELECT * FROM interests WHERE staff_id=? ORDER BY name", (staff["id"],)).fetchall()
        projects = db.execute("SELECT * FROM projects WHERE staff_id=? ORDER BY id DESC", (staff["id"],)).fetchall()
        return render_template("dashboard.html", staff=staff, interests=interests, projects=projects)

    @app.route("/dashboard/profile", methods=["GET", "POST"])
    @staff_required
    def edit_profile():
        db = get_db()
        staff = db.execute("SELECT * FROM staff WHERE id=?", (session["staff_id"],)).fetchone()
        if request.method == "POST":
            department = request.form.get("department", "").strip()
            bio = request.form.get("bio", "").strip()
            errors = validate_profile(department, bio)
            if not errors:
                db.execute("UPDATE staff SET department=?, bio=? WHERE id=?", (department, bio, staff["id"]))
                db.commit()
                flash("Your public profile was updated.", "success")
                return redirect(url_for("dashboard"))
            for error in errors:
                flash(error, "error")
            staff = dict(staff) | {"department": department, "bio": bio}
        return render_template("profile_form.html", staff=staff)

    @app.post("/dashboard/interests")
    @staff_required
    def add_interest():
        name = request.form.get("name", "").strip()
        error = validate_interest(name)
        db = get_db()
        if error:
            flash(error, "error")
        elif db.execute("SELECT 1 FROM interests WHERE staff_id=? AND lower(name)=lower(?)", (session["staff_id"], name)).fetchone():
            flash("That area of interest is already on your profile.", "error")
        else:
            db.execute("INSERT INTO interests (staff_id, name) VALUES (?, ?)", (session["staff_id"], name))
            db.commit()
            flash("Area of interest added.", "success")
        return redirect(url_for("dashboard"))

    @app.post("/dashboard/interests/<int:interest_id>/delete")
    @staff_required
    def delete_interest(interest_id):
        db = get_db()
        deleted = db.execute("DELETE FROM interests WHERE id=? AND staff_id=?", (interest_id, session["staff_id"])).rowcount
        db.commit()
        if not deleted:
            abort(403)
        flash("Area of interest removed.", "info")
        return redirect(url_for("dashboard"))

    @app.route("/dashboard/projects/new", methods=["GET", "POST"])
    @staff_required
    def create_project():
        if request.method == "POST":
            values, errors = project_values(request.form)
            if not errors:
                get_db().execute(
                    "INSERT INTO projects (staff_id,title,summary,skills,project_type,availability) VALUES (?,?,?,?,?,?)",
                    (session["staff_id"], *values),
                )
                get_db().commit()
                flash("Project idea published.", "success")
                return redirect(url_for("dashboard"))
            for error in errors:
                flash(error, "error")
            return render_template("project_form.html", project=request.form, heading="Create a project idea", submit_label="Publish project")
        return render_template("project_form.html", project={}, heading="Create a project idea", submit_label="Publish project")

    @app.route("/dashboard/projects/<int:project_id>/edit", methods=["GET", "POST"])
    @staff_required
    def edit_project(project_id):
        project = owned_project_or_404(project_id)
        if request.method == "POST":
            values, errors = project_values(request.form)
            if not errors:
                get_db().execute(
                    "UPDATE projects SET title=?,summary=?,skills=?,project_type=?,availability=? WHERE id=?",
                    (*values, project_id),
                )
                get_db().commit()
                flash("Project idea updated.", "success")
                return redirect(url_for("dashboard"))
            for error in errors:
                flash(error, "error")
            project = request.form
        return render_template("project_form.html", project=project, heading="Edit project idea", submit_label="Save changes")

    @app.post("/dashboard/projects/<int:project_id>/delete")
    @staff_required
    def delete_project(project_id):
        owned_project_or_404(project_id)
        get_db().execute("DELETE FROM projects WHERE id=?", (project_id,))
        get_db().commit()
        flash("Project idea deleted.", "info")
        return redirect(url_for("dashboard"))

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    with app.app_context():
        init_db()
    return app


def validate_profile(department, bio):
    errors = []
    if not (2 <= len(department) <= 100):
        errors.append("Department must contain between 2 and 100 characters.")
    if not (30 <= len(bio) <= 1000):
        errors.append("Biography must contain between 30 and 1,000 characters.")
    return errors


def validate_interest(name):
    if not (2 <= len(name) <= 60):
        return "An area of interest must contain between 2 and 60 characters."
    return None


def project_values(form):
    values = (
        form.get("title", "").strip(), form.get("summary", "").strip(), form.get("skills", "").strip(),
        form.get("project_type", "").strip(), form.get("availability", "").strip(),
    )
    title, summary, skills, project_type, availability = values
    errors = []
    if not (5 <= len(title) <= 120): errors.append("Title must contain between 5 and 120 characters.")
    if not (40 <= len(summary) <= 1500): errors.append("Summary must contain between 40 and 1,500 characters.")
    if not (2 <= len(skills) <= 200): errors.append("Skills must contain between 2 and 200 characters.")
    if project_type not in {"Research", "Development", "Data analysis", "Literature review"}: errors.append("Select a valid project type.")
    if availability not in {"Available", "Limited availability", "Allocated"}: errors.append("Select a valid availability status.")
    return values, errors


def seed_data(db):
    staff = [
        ("Dr Ada Bennett", "ada@university.ac.uk", "demo123", "School of Computing", "I supervise practical and research-led projects at the intersection of data, software engineering and responsible technology."),
        ("Dr James Okafor", "james.okafor@university.ac.uk", "demo123", "School of Computing", "My interests include networks, graph algorithms and the design of efficient, reliable systems."),
        ("Dr Priya Shah", "priya.shah@university.ac.uk", "demo123", "School of Computing", "I am interested in human-centred AI, accessible interaction design and evidence-based software evaluation."),
    ]
    db.executemany("INSERT INTO staff (full_name,email,password,department,bio) VALUES (?,?,?,?,?)", staff)
    interests = [(1,"Data analysis"),(1,"Software maintenance"),(1,"Machine learning"),(2,"Graph theory"),(2,"Computer networks"),(2,"Algorithms"),(3,"Human-computer interaction"),(3,"Accessible design"),(3,"Artificial intelligence")]
    db.executemany("INSERT INTO interests (staff_id,name) VALUES (?,?)", interests)
    projects = [
        (1,"Explaining software maintenance risk with repository data","Develop a dashboard that identifies code areas likely to require maintenance by combining commit history, code complexity and issue data.","Python, data visualisation, Git","Data analysis","Available"),
        (1,"Fairness checks for student-facing AI tools","Investigate practical fairness metrics and build a small prototype that helps developers inspect model outcomes across user groups.","Python, machine learning, ethics","Research","Limited availability"),
        (2,"Visualising resilient campus networks","Model a campus network as a graph and evaluate how failures affect connectivity and routing choices.","Graph theory, Python, networks","Development","Available"),
        (3,"Accessible feedback for programming learners","Design and evaluate an accessible interface that gives novice programmers clear, timely feedback on code exercises.","UX research, HTML/CSS, accessibility","Research","Available"),
    ]
    db.executemany("INSERT INTO projects (staff_id,title,summary,skills,project_type,availability) VALUES (?,?,?,?,?,?)", projects)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
