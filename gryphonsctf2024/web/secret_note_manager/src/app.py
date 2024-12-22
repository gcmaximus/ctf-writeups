import secrets
import threading
import time
from functools import wraps

from flask import Flask, redirect, render_template, request, session
from utils import get_all_public_notes, get_user_notes, init_db, login_user

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(24)


def reset_loop():
    while True:
        time.sleep(60 * 5)
        print("Resetting database")
        init_db()
        print("Reset complete")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    notes = get_all_public_notes()
    username = session.get("username", "guest")
    return render_template("index.html", notes=notes, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = login_user(username, password)
        if user is None:
            return render_template("login.html", error="Invalid username or password")

        session["username"] = user[1]
        session["user_id"] = user[0]
        return redirect("/home")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/home")
@login_required
def home():
    notes = get_user_notes(session["user_id"])
    return render_template("home.html", notes=notes, username=session["username"])


if __name__ == "__main__":
    init_db()

    reset_thread = threading.Thread(target=reset_loop, daemon=True)
    reset_thread.start()

    app.run("0.0.0.0", 22222)
