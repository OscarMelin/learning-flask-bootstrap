from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

@app.errorhandler(404)
def page_not_found(e):
    return("four oh four")

if __name__ == "__main__":
    app.run()
