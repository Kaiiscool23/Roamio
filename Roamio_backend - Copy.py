from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok

# Initialize Flask app and enable ngrok for external access
app = Flask(__name__)
run_with_ngrok(app)  # Exposes the app to the public

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roamio.db'
db = SQLAlchemy(app)

# Define a model for the Destination table
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Destination {self.name}>"

# Create the database and tables (do this only once)
with app.app_context():
    db.create_all()

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to Roamio Backend!"

# Define a route to add destinations via POST
@app.route('/add_destination', methods=['POST'])
def add_destination():
    data = request.get_json()
    new_destination = Destination(
        name=data['name'],
        description=data['description']
    )
    db.session.add(new_destination)
    db.session.commit()
    return jsonify({"message": "Destination added!"}), 201

# Define a route to get all destinations via GET
@app.route('/get_destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([{
        'name': dest.name,
        'description': dest.description
    } for dest in destinations]), 200

if __name__ == '__main__':
    app.run()
