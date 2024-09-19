from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@database/myapp'
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
