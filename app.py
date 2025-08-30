
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# # Replace with your own credentials
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Pranav%402003@localhost:3306/flaskdb"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # ---------------------------
# # MODELS
# # ---------------------------

# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), default="user")
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     created_sops = db.relationship(
#         "SOP",
#         foreign_keys="SOP.created_by",
#         backref="creator",
#         lazy=True,
#     )
#     modified_sops = db.relationship(
#         "SOP",
#         foreign_keys="SOP.last_modified_by",
#         backref="modifier",
#         lazy=True,
#     )

#     def __repr__(self):
#         return f"<User {self.username}>"


# class Service(db.Model):
#     __tablename__ = "services"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     version = db.Column(db.String(20), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationships
#     sops = db.relationship("SOP", backref="service", cascade="all, delete-orphan", lazy=True)

#     def __repr__(self):
#         return f"<Service {self.name} v{self.version}>"


# class SOP(db.Model):
#     __tablename__ = "sops"

#     id = db.Column(db.Integer, primary_key=True)
#     service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
#     alert = db.Column(db.String(100), nullable=False)
#     sop_title = db.Column(db.String(100), nullable=False)
#     sop_description = db.Column(db.Text)
#     sop_link = db.Column(db.String(255))

#     created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
#     last_modified_by = db.Column(db.Integer, db.ForeignKey("users.id"))

#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def __repr__(self):
#         return f"<SOP {self.sop_title} for Service {self.service_id}>"

# # ---------------------------
# # CREATE TABLES
# # ---------------------------
# with app.app_context():
#     db.create_all()

# # ---------------------------
# # ROUTES
# # ---------------------------

# @app.route("/")
# def hello():
#     return "Hello"

# # ---- USER DEMO ROUTES (kept from your code, but now use full User model) ----

# @app.route("/add_user", methods=["POST"])
# def add_user_json():
#     data = request.get_json()
#     username = data.get("username")
#     email = data.get("email")
#     password_hash = data.get("password")  # normally you'd hash this!
#     if not username or not email or not password_hash:
#         return {"error": "username, email, and password are required"}, 400
    
#     user = User(username=username, email=email, password_hash=password_hash)
#     db.session.add(user)
#     db.session.commit()
#     return {"message": f"User {username} added!"}, 201


# @app.route("/users")
# def get_users():
#     users = User.query.all()
#     return jsonify([{
#         "id": u.id,
#         "username": u.username,
#         "email": u.email,
#         "role": u.role
#     } for u in users])

# @app.route("/user/<int:id>")
# def get_user(id):
#     user = User.query.get(id)
#     if not user:
#         return {"error": "User not found"}, 404
#     return {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "role": user.role
#     }

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask
from flask_cors import CORS
from models import db
from routes import register_routes



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Pranav%402003@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Apply CORS globally, only allow frontend origin
CORS(app, origins=["http://192.168.64.1:5500"])  # Clean, production-safe




# Initialize DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Register routes
register_routes(app)



# Only run the server if executed directly, not when using 'flask run'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


