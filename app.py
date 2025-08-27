
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your own credentials
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Pranav%402003@localhost:3306/flaskdb"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return f"Hello"

@app.route("/add/<name>")
def add_user(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return f"User {name} added!"

@app.route("/users")
def get_users():
    users = User.query.all()
    return { "users": [u.name for u in users] }

if __name__ == "__main__":
    app.run(debug=True)
