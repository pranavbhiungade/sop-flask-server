
from flask import Flask, jsonify, request
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

# 2. Add user (using POST request with JSON body)
@app.route("/add_user", methods=["POST"])
def add_user_json():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return {"error": "Name is required"}, 400
    
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return {"message": f"User {name} added!"}, 201

# 3. Get all users
@app.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

# 4. Get a single user by ID
@app.route("/user/<int:id>")
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    return {"id": user.id, "name": user.name}

# 5. Update a user
@app.route("/update/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    
    data = request.get_json()
    new_name = data.get("name")
    if not new_name:
        return {"error": "Name is required"}, 400
    
    user.name = new_name
    db.session.commit()
    return {"message": f"User {id} updated to {new_name}"}

# 6. Delete a user
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User not found"}, 404
    
    db.session.delete(user)
    db.session.commit()
    return {"message": f"User {id} deleted!"}

if __name__ == "__main__":
    app.run(debug=True)