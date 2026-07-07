
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db:5432/northwind'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        db.session.execute(text('SELECT 1'))
    print('connection Successful!')
 
except Exception as e:
    print(f'Error connecting to database: {e}')

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    comapny_name = db.Column(db.String(100))
    contact_name = db.Column(db.String(100))
    city = db.Column(db.String(50))


@app.route('/')
def index():
    # fetch data from table
    customers = Customer.query.all()
    return render_template('index.html',customers=customers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
