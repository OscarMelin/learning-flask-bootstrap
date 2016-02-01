from flask import Flask, render_template, request, url_for, redirect, session
from dbconnect import connection

from wtforms import Form, TextField, validators, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart

import gc

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login_page"))


@app.route("/logout/")
def logout():
    session.clear()
    gc.collect()
    return redirect(url_for("homepage"))

@app.route("/login/", methods = ["GET", "POST"])
def login_page():

    error = None

    try:
        c, conn = connection()
        if request.method == "POST":
            
            data = c.execute("SELECT * FROM users WHERE username = ('{0}');".format(thwart(request.form["username"])))
            data = c.fetchone()[2] #password

            if sha256_crypt.verify(request.form["password"], data):
                session["logged_in"] = True
                session["username"] = request.form["username"]

                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        c.close() #Close db connection, saves ram
        gc.collect()

        return render_template("login.html", error = error)

    except Exception as e:
        error = "Invalid credentials, try again. {0}".format(str(e))
        return render_template("login.html", error = error)


class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min = 4, max = 20)])
    email = TextField("Email Address", [validators.Length(min = 6, max = 50)])
    password = PasswordField("Password", [validators.Required(),
                                          validators.EqualTo("confirm", message = "Passwords must match")])
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the Privacy Notice', [validators.Required()]) 


@app.route("/register/", methods = ["GET", "POST"])
def register_page():
    
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            c, conn = connection()
            ret = c.execute("SELECT * FROM users WHERE username = ('{0}');".format(thwart(username)))

            if int(ret) > 0:    
                return "Username taken"

            else:
                c.execute("INSERT INTO users (username, password, email) VALUES ('{0}', '{1}', '{2}')".format(thwart(username), thwart(password), thwart(email)))
                conn.commit()
                c.close() #Close db connection, saves ram
                conn.close()

                gc.collect()

                session["logged_in"] = True
                session["username"] = username
                
                return redirect(url_for("dashboard"))

        return render_template("register.html", form = form)

        

    except Exception as e:
        return str(e)

@app.errorhandler(Exception)
def exception_handler(error):
    return repr(error)

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
