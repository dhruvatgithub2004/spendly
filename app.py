import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, get_user_by_id, create_user

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "POST":
        if "name" not in request.form or "email" not in request.form or "password" not in request.form:
            abort(400)

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not name:
            return render_template("register.html", error="Name is required.", name=name, email=email)

        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

        email = email.lower()

        if get_user_by_email(email):
            return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "POST":
        if "email" not in request.form or "password" not in request.form:
            abort(400)

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password.", email=email)

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
