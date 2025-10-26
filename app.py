from flask import Flask
from flask_cors import CORS
from models import db
from routes import register_routes

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Pranav%402003@localhost:3306/flaskdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Apply CORS globally (only allow your frontend)
CORS(app)

# Initialize DB
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Register routes from routes.py
register_routes(app)

# Run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



