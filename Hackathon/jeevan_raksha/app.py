from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib
import re

app = Flask(__name__)
app.secret_key = "jeevan_raksha_secret"

# ---------- DATABASE CONNECTION ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Janhavi@08",
    database="jeevan_raksha"
)
cursor = db.cursor()

# ---------- VALIDATION ----------
def valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]{3,50}", name))

def valid_mobile(mobile):
    return bool(re.fullmatch(r"[6-9][0-9]{9}", mobile))

# ---------- ROUTES ----------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

# ---------- REGISTER ----------
@app.route("/register_user", methods=["POST"])
def register_user():
    name = request.form["name"].strip()
    mobile = request.form["mobile"].strip()
    password = request.form["password"]

    if not valid_name(name):
        flash("❌ Name should contain only letters and spaces", "error")
        return redirect(url_for("register"))

    if not valid_mobile(mobile):
        flash("❌ Enter a valid 10-digit mobile number", "error")
        return redirect(url_for("register"))

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute(
            "INSERT INTO users (name, mobile, password) VALUES (%s, %s, %s)",
            (name, mobile, hashed_password)
        )
        db.commit()
        flash("✅ Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    except mysql.connector.errors.IntegrityError:
        flash("⚠️ User already exists with this mobile number", "error")
        return redirect(url_for("register"))

# ---------- LOGIN ----------
@app.route("/login_user", methods=["POST"])
def login_user():
    mobile = request.form["mobile"].strip()
    password = request.form["password"]

    if not valid_mobile(mobile):
        flash("❌ Invalid mobile number format", "error")
        return redirect(url_for("login"))

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "SELECT id, name FROM users WHERE mobile=%s AND password=%s",
        (mobile, hashed_password)
    )
    user = cursor.fetchone()

    if user:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return redirect(url_for("dashboard"))
    else:
        flash("❌ Wrong mobile number or password", "error")
        return redirect(url_for("login"))

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("⚠️ Please login first", "error")
        return redirect(url_for("login"))

    return render_template("dashboard.html", name=session["user_name"])

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Logged out successfully", "success")
    return redirect(url_for("login"))

# ---------- MODULE PLACEHOLDERS ----------
@app.route("/medilingo")
def medilingo():
    return "Medilingo Module Coming Soon"

@app.route("/arogyamitra")
def arogyamitra():
    return "ArogyaMitra Module Coming Soon"

@app.route("/appointment")
def appointment():
    return "Doctor Appointment Module Coming Soon"

@app.route("/medicine")
def medicine():
    return "Medicine Booking Module Coming Soon"

if __name__ == "__main__":
    app.run(debug=True, port=5003)
