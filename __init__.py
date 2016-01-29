from flask import Flask, render_template, request, url_for, redirect
from dbconnect import connection

from wtforms import Form #?

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login/", methods = ["GET", "POST"])
def login_page():

    error = None

    try:
        if request.method == "POST":
            attempted_username = request.form["username"]
            attempted_password = request.form["password"]
            

            if attempted_username == "admin":
                return redirect(url_for("dashboard"))
            else:
                error = "Fel fel blaha"

        return render_template("login.html", error=error)

    except Exception as e:
        return render_template("login.html", error = e)


class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min = 4, max = 20)])
    email = TextField("Email Address", [validators.Length(min = 6, max = 50)])
    password = PasswordField("Password", [validators.Required(),
                                          validators.EqualTo("confirm", message = "Passwords must match")])
    confirm = passwordField("Repeat Password")
    accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the Privacy Notice', validators.Required())


@app.route("/register/", methods = ["GET", "POST"])
def register_page():
    
    try:
        c, conn = connection()
        return "okay"
    except Exception as e:
        return string(e)


@app.errorhandler(404)
def page_not_found(e):
    return("four oh four")

@app.errorhandler(405)
def page_not_found(e):
    return("Request not permitted")

@app.errorhandler(500)
def page_not_found(e):
    return("five hundred")

if __name__ == "__main__":
    app.run()
