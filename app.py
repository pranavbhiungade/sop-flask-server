from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask! 🚀"

@app.route("/greet/<name>")
def greet(name):
    return render_template("index.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return f"Welcome, {username}!"
    return '''
        <form method="post">
            <input type="text" name="username">
            <input type="submit" value="Login">
        </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
