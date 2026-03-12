from flask import Flask, render_template, redirect, request, session, flash, url_for

app = Flask(__name__)
app.secret_key = "sparkle_secret"

# Dummy user storage
users = {}

# ---------------- HOME ----------------
# Open site → Show Register page first
@app.route("/")
def home():
    if session.get("user"):
        return render_template("index.html")
    else:
        return redirect(url_for("register"))

# ---------------- INDEX ----------------
@app.route("/index")
def index():
    if not session.get("user"):
        return redirect(url_for("register"))
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user"):
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if email in users:
            flash("Email already registered ❌", "danger")
            return redirect(url_for("register"))

        users[email] = {"name": name, "password": password}
        flash("Registration Successful! Please Login 💖", "success")
        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email]["password"] == password:
            session["user"] = users[email]["name"]
            return redirect(url_for("index"))   # ❌ flash removed
        else:
            flash("Invalid Email or Password ❌", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged Out Successfully 💕", "info")
    return redirect(url_for("index"))

# ---------------- PROFILE ----------------
@app.route("/myprofile")
def myprofile():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("myprofile.html")

# ---------------- CONTACT ----------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Message Sent Successfully 💖", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)