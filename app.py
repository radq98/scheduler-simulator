from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
)
from datetime import datetime, timedelta
from random import randint

app = Flask(__name__)
app.config["SECRET_KEY"] = "5Q8wfQqmx67Ez0wondbxSeYXS8mE2gob"
app.config["DEBUG"] = True

#metadata
appversion = "0.1"
footertext = "Radosław Zegadło - Wroclaw University of Science 2020"

@app.route("/", methods=["GET", "POST"])
def index():

    context = {
        "appversion": appversion,
        "footertext": footertext,
    }
    return render_template("index.html", context=context)

@app.route("/results")
def results():
    context = {
        "appversion": appversion,
        "footertext": footertext,
    }
    return render_template("results.html", context=context)

if __name__ == "__main__":
    app.run()