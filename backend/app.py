from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@database/myapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

@app.route('/')
def hello():
    return "Hello from Flask!"

@app.route('/api/data')
def get_data():
    return jsonify({"message": "Hello from the backend API again!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
