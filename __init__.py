from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login/", methods = ["GET", "POST"])
def login_page():
    return render_template("login.html")

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
