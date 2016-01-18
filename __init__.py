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
