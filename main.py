from flask import Flask, render_template

#flask pages
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

#run the web application
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False,host="0.0.0.0")