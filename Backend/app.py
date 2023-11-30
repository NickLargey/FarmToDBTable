from flask import request, jsonify
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5433/farm2db'
db = SQLAlchemy()


class ProducerUser(db.Model):
    __tablename__ = 'producer'  # Match the table name in your PostgreSQL database

    pro_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pro_name = db.Column(db.Text)
    pro_email = db.Column(db.Text)
    pro_phone = db.Column(db.Text)
    pro_address = db.Column(db.Text)
    pro_city = db.Column(db.Text)
    pro_state = db.Column(db.String(2))
    pro_zip = db.Column(db.String(5))
    pro_county = db.Column(db.Text)

    def __init__(self, pro_name, pro_email, pro_phone, pro_address, pro_city, pro_state, pro_zip, pro_county):
        self.pro_name = pro_name
        self.pro_email = pro_email
        self.pro_phone = pro_phone
        self.pro_address = pro_address
        self.pro_city = pro_city
        self.pro_state = pro_state
        self.pro_zip = pro_zip
        self.pro_county = pro_county


class SchoolUser(db.Model):
    __tablename__ = 'school'  # Name of the table in the database

    sch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sch_name = db.Column(db.Text)
    sch_email = db.Column(db.Text)
    sch_phone = db.Column(db.Text)
    sch_address = db.Column(db.Text)
    sch_city = db.Column(db.Text)
    sch_state = db.Column(db.String(2))
    sch_zip = db.Column(db.String(5))
    sch_county = db.Column(db.Text)

    def __init__(self, sch_name, sch_email, sch_phone, sch_address, sch_city, sch_state, sch_zip, sch_county):
        self.sch_name = sch_name
        self.sch_email = sch_email
        self.sch_phone = sch_phone
        self.sch_address = sch_address
        self.sch_city = sch_city
        self.sch_state = sch_state
        self.sch_zip = sch_zip
        self.sch_county = sch_county


class VolunteerUser(db.Model):
    __tablename__ = 'volunteer'  # Name of the table in the database

    vol_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vol_name = db.Column(db.Text)
    vol_email = db.Column(db.Text)
    vol_phone = db.Column(db.Text)
    vol_hub = db.Column(db.Integer)

    def __init__(self, vol_name, vol_email, vol_phone, vol_hub):
        self.vol_name = vol_name
        self.vol_email = vol_email
        self.vol_phone = vol_phone
        self.vol_hub = vol_hub


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    userType = data.get('userType')
    username = data.get('username')

    if userType == 'producer':
        user = ProducerUser.query.filter_by(pro_name=username).first()
        if user:
            print(user.pro_id)
            return jsonify({'message': "Login successful",
                            'redirect': './Farm/farm_index.html'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    elif userType == 'school':
        user = SchoolUser.query.filter_by(sch_name=username).first()
        if user:
            return jsonify({'message': "Login successful",
                            'redirect': './School/school_index.html'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    elif userType == 'volunteer':
        user = VolunteerUser.query.filter_by(vol_name=username).first()
        if user:
            return jsonify({'message': "Login successful",
                            'redirect': './Volunteer/volunteer_index.html'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')

    # Check if the username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


def execute_sql_query(sql_query, cursor):
    try:
        cursor.execute(sql_query)

        # Fetch the results (if any)
        results = cursor.fetchall()

        # Commit the transaction and close the connection

        return results

    except Exception as e:
        return str(e)

# Define an endpoint to receive and process SQL queries


@app.route('/run-sql', methods=['POST'])
def run_sql():
    try:
        data = request.get_json()
        sql_query = data['query']
        print(str(sql_query))
        # Call the execute_sql_query function with the SQL query
        with open('configparams.json', 'r') as file:
            db_config = json.load(file)

        # Connect to your PostgreSQL database
        with psycopg2.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                query_result = execute_sql_query(sql_query, cursor)
                connection.commit()
                # Return the results as JSON
        return jsonify({'result': query_result})

    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        connection.close()


db.init_app(app)  # Register the SQLAlchemy instance with your Flask app

if __name__ == "__main__":
    app.run(debug=True)
