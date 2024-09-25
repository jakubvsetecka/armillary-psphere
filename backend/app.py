from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@database/myapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class Osoba(db.Model):
    __tablename__ = 'OSOBA'
    ID_OSOBA = db.Column(db.Integer, primary_key=True)
    JMENO_OSOBA = db.Column(db.String(255), nullable=False)
    PRIJMENI_OSOBA = db.Column(db.String(255), nullable=False)

class Poslanec(db.Model):
    __tablename__ = 'POSLANEC'
    ID_POSLANEC = db.Column(db.Integer, primary_key=True)
    ID_OSOBA = db.Column(db.Integer, db.ForeignKey('OSOBA.ID_OSOBA'))
    osoba = db.relationship('Osoba', backref='poslanec')

class Hlasovani(db.Model):
    __tablename__ = 'HLASOVANI'
    ID_HLASOVANI = db.Column(db.Integer, primary_key=True)
    VYSLEDEK_HLASOVANI = db.Column(db.Text, nullable=False)
    NAZEV_HLASOVANI = db.Column(db.Text, nullable=False)
    DATUM_HLASOVANI = db.Column(db.Date, nullable=False)
    LEFT_SCORE = db.Column(db.Float)
    LIB_SCORE = db.Column(db.Float)

@app.route('/api/data/graph')
def get_graph():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'graph.json')
        with open(file_path, 'r') as f:
            graph = json.load(f)

        # Extract only the hlasovani part
        hlasovani = graph["hlasovani"]

        return jsonify(hlasovani)
    except FileNotFoundError:
        return jsonify({"error": "Graph file not found!"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in graph file!"}), 500
    except KeyError:
        return jsonify({"error": "No 'hlasovani' key found in the graph data!"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/poslanec/<int:poslanec_id>')
def get_poslanec_name(poslanec_id):
    poslanec = Poslanec.query.get(poslanec_id)
    if poslanec and poslanec.osoba:
        return jsonify({
            "id": poslanec.ID_POSLANEC,
            "name": f"{poslanec.osoba.JMENO_OSOBA} {poslanec.osoba.PRIJMENI_OSOBA}"
        })
    else:
        return jsonify({"error": "Poslanec not found"}), 404

@app.route('/api/hlasovani/<int:hlasovani_id>')
def get_hlasovani_name(hlasovani_id):
    hlasovani = Hlasovani.query.get(hlasovani_id)
    if hlasovani:
        return jsonify({
            "id": hlasovani.ID_HLASOVANI,
            "name": hlasovani.NAZEV_HLASOVANI
        })
    else:
        return jsonify({"error": "Hlasovani not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')