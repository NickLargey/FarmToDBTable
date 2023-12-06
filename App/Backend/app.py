from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json
import logging
from sqlalchemy.sql import text
from psycopg2.extras import RealDictCursor
from datetime import datetime
import psycopg2.extras

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)  # Set logging level

# Load database configuration from configparams.json
with open('configparams.json', 'r') as file:
    db_config = json.load(file)
    db_uri = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)


@app.route('/test-db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))

            # Process the results
            data = [{'column': row[0]} for row in result]

            return jsonify({'message': 'Database connection successful', 'result': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to get a database connection


def get_db_connection():
    return psycopg2.connect(**db_config)


class ProducerUser(db.Model):
    __tablename__ = 'producer'

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
    if request.method == 'OPTIONS':
        # Prepare response for OPTIONS preflight request
        response = current_app.make_default_options_response()
        return response
    data = request.json
    userType = data.get('userType')
    username = data.get('username')
    # Added logging
    app.logger.debug(
        f"Login attempt for userType: {userType}, username: {username}")

    if userType == 'producer':
        user = ProducerUser.query.filter_by(pro_name=username).first()
        if user:
            # Assuming 'producerName' is obtained after a successful login
            redirect_url = f'./Farm/producerLanding.html?producer={user.pro_name}'
            return jsonify({'message': "Login successful", 'redirect': redirect_url}), 200

        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    elif userType == 'school':
        user = SchoolUser.query.filter_by(sch_name=username).first()
        if user:
            redirect_url = f'./School/schoolLanding.html?school={user.sch_name}'
            return jsonify({'message': "Login successful", 'redirect': redirect_url}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    elif userType == 'volunteer':
        user = VolunteerUser.query.filter_by(vol_name=username).first()
        if user:
            redirect_url = f'./Volunteer/volunteerLanding.html?volunteer={user.vol_name}'
            return jsonify({'message': "Login successful", 'redirect': redirect_url}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/registerProducer', methods=['POST'])
def registerProducer():
    data = request.json
    userType = data.get('userType')
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    zip = data.get('zip')
    county = data.get('county')

    # Check if the username already exists in the database
    existing_user = ProducerUser.query.filter_by(
        pro_name=username, pro_address=address, pro_city=city).first()
    if existing_user:
        return jsonify({'message': 'Producer already exists in system'}), 400

    # Create a new user
    new_user = ProducerUser(pro_name=username, pro_email=email, pro_phone=phone,
                            pro_address=address, pro_city=city, pro_state=state, pro_zip=zip, pro_county=county)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


@app.route('/registerSchool', methods=['POST'])
def registerSchool():
    data = request.json
    userType = data.get('userType')
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    zip = data.get('zip')
    county = data.get('county')

    # Check if the username already exists in the database
    existing_user = SchoolUser.query.filter_by(
        sch_name=username, sch_address=address, sch_city=city).first()
    if existing_user:
        return jsonify({'message': 'School already exists in system'}), 400

    # Create a new user
    new_user = SchoolUser(sch_name=username, sch_email=email, sch_phone=phone,
                          sch_address=address, sch_city=city, sch_state=state, sch_zip=zip, sch_county=county)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


@app.route('/registerVolunteer', methods=['POST'])
def registerVolunteer():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    hub = data.get('hub')

    # Check if the username already exists in the database
    existing_user = VolunteerUser.query.filter_by(
        vol_name=username, vol_phone=phone).first()
    if existing_user:
        return jsonify({'message': 'Volunteer already exists in system'}), 400

    # Create a new user
    new_user = VolunteerUser(
        vol_name=username, vol_email=email, vol_phone=phone, vol_hub=hub)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


def is_date_attribute(attribute):
    # Define a function or logic to determine if an attribute is a date.
    # This could be a list of date attributes, a database schema lookup, etc.
    # For example:
    date_attributes = ['fi_date_harvested',
                       'fi_est_expiration', 'pur_date', 'vrol_dates']
    return attribute in date_attributes


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")
        table = data.get('table')
        attribute = data.get('attribute')
        query_param = data.get('query')
        date_from = data.get('dateFrom')
        date_to = data.get('dateTo')
        join_query = data.get('joinQuery')

        with open('configparams.json', 'r') as file:
            db_config = json.load(file)

        with psycopg2.connect(**db_config) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Build the SQL query
                sql_query = f"SELECT * FROM {table} "
                if join_query:
                    sql_query += join_query + " "

                params = []
                if is_date_attribute(attribute):
                    # Query for date range
                    sql_query += f"WHERE {table}.{attribute} BETWEEN %s AND %s"
                    params.extend([date_from, date_to])
                else:
                    # Query for text search
                    sql_query += f"WHERE {table}.{attribute} ILIKE %s"
                    params.append(f'%{query_param}%')

                # Execute the query
                cursor.execute(sql_query, params)
                results = cursor.fetchall()

        return jsonify({'results': results})

    except Exception as e:
        app.logger.error(f"An error occurred in /search: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/harvest-feed', methods=['GET'])
def get_harvest_feed():
    try:
        school_name = request.args.get('school')
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
        SELECT fi.fi_name, fi.fi_date_harvested, fi.fi_quantity
        FROM school s
        JOIN hub_school hs ON s.sch_id = hs.sch_id
        JOIN hub h ON hs.hub_id = h.hub_id
        JOIN hub_producer hp ON h.hub_id = hp.hub_id
        JOIN producer p ON hp.pro_id = p.pro_id
        JOIN producer_food_item pfi ON p.pro_id = pfi.pro_id
        JOIN food_item fi ON pfi.fi_id = fi.fi_id
        WHERE s.sch_name = %s
        ORDER BY fi.fi_date_harvested DESC
        LIMIT 20
        """
        cursor.execute(query, (school_name,))
        harvest_feed_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(harvest_feed_data)
    except Exception as e:
        app.logger.error(f"An error occurred in /api/harvest-feed: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search-food-items', methods=['GET'])
def search_food_items():
    try:
        school_name = request.args.get('school')
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
        SELECT fi.fi_id, fi.fi_name, fi.fi_date_harvested, fi.fi_est_expiration, fi.fi_quantity, 
               p.pro_name as farm_name
        FROM food_item fi
        JOIN producer_food_item pfi ON fi.fi_id = pfi.fi_id
        JOIN producer p ON pfi.pro_id = p.pro_id
        JOIN hub_producer hp ON p.pro_id = hp.pro_id
        JOIN hub h ON hp.hub_id = h.hub_id
        JOIN hub_school hs ON h.hub_id = hs.hub_id
        JOIN school s ON hs.sch_id = s.sch_id
        WHERE s.sch_name = %s AND fi.fi_est_expiration > CURRENT_DATE
        """
        cursor.execute(query, (school_name,))
        search_results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(search_results)
    except Exception as e:
        app.logger.error(
            f"An error occurred in /api/search-food-items: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Define an endpoint to receive and process SQL queries
@app.route('/run-sql', methods=['POST'])
def run_sql():
    try:
        data = request.get_json()
        sql_query = data['query']
        app.logger.debug(f"Executing SQL query: {sql_query}")  # Added logging
        # Call the execute_sql_query function with the SQL query
        with open('configparams.json', 'r') as file:
            db_config = json.load(file)

        # Connect to your PostgreSQL database
        with psycopg2.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)

                # Fetch the results (if any)
                results = cursor.fetchall()
                connection.commit()
                # Return the results as JSON
        return jsonify({'result': results})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")  # Added logging
        return jsonify({'error': str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()


@app.route('/api/create-purchase-order', methods=['POST'])
def create_purchase_order():
    try:
        data = request.json
        fi_id = int(data['fi_id'])
        quantity = int(data['quantity'])
        # Retrieve school_name from request data
        school_name = data.get('school_name')

        if not school_name:
            return jsonify({'message': 'School name is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the available quantity and cost per quantity of the food item
        cursor.execute(
            "SELECT fi_quantity, fi_cost_per_quantity FROM food_item WHERE fi_id = %s", (fi_id,))
        result = cursor.fetchone()
        available_quantity = result[0]
        cost_per_quantity = result[1]

        if available_quantity < quantity:
            return jsonify({'message': 'Not enough quantity available'}), 400

        # Calculate total price
        total_price = cost_per_quantity * quantity

        # Insert new purchase order into PURCHASE_ORDER table
        insert_query = """
        INSERT INTO purchase_order (pur_date, pur_quantity, pur_total_price, pur_fi_id, pur_status)
        VALUES (CURRENT_DATE, %s, %s, %s, 'Awaiting Fulfillment')
        RETURNING pur_id
        """
        cursor.execute(insert_query, (quantity, total_price, fi_id))
        pur_id = cursor.fetchone()[0]

        # Get school id based on school name
        cursor.execute(
            "SELECT sch_id FROM school WHERE sch_name = %s", (school_name,))
        sch_id = cursor.fetchone()[0]

        # Insert into SCHOOL_PURCHASE_ORDER table
        insert_spo_query = """
        INSERT INTO school_purchase_order (sch_id, pur_id)
        VALUES (%s, %s)
        """
        cursor.execute(insert_spo_query, (sch_id, pur_id))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({'message': 'Purchase order created', 'purchase_order_id': pur_id}), 201

    except psycopg2.Error as e:
        conn.rollback()
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': str(e.pgerror)}), 500
    except Exception as e:
        app.logger.error(
            f"An error occurred in /api/create-purchase-order: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/recent-orders', methods=['GET'])
def recent_orders():
    try:
        school_name = request.args.get('school')
        if not school_name:
            return jsonify({'message': 'School name is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """
        SELECT po.pur_id, po.pur_date, po.pur_status, po.pur_quantity as quantity,
               fi.fi_name as food_item_name
        FROM purchase_order po
        JOIN school_purchase_order spo ON po.pur_id = spo.pur_id
        JOIN school s ON spo.sch_id = s.sch_id
        JOIN food_item fi ON po.pur_fi_id = fi.fi_id
        WHERE s.sch_name = %s AND po.pur_status IN ('Awaiting Fulfillment', 'Ready at Hub')
        ORDER BY po.pur_date DESC
        LIMIT 10
        """
        cursor.execute(query, (school_name,))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(orders)

    except Exception as e:
        app.logger.error(f"An error occurred in /api/recent-orders: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-food-item', methods=['POST'])
def add_food_item():
    data = request.json
    producer_name = data.get('producerName')

    if not producer_name:
        return jsonify({'error': 'Producer name is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # First, get the producer ID based on the provided name
        cursor.execute(
            "SELECT pro_id FROM producer WHERE pro_name = %s", (producer_name,))
        producer_id_row = cursor.fetchone()
        if producer_id_row is None:
            return jsonify({'error': 'Producer not found'}), 404
        producer_id = producer_id_row[0]

        # Then, insert the food item
        insert_query = """
        INSERT INTO food_item (fi_name, fi_description, fi_macro, fi_quantity, fi_cost_per_quantity, fi_date_harvested, fi_est_expiration, fi_unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING fi_id
        """
        cursor.execute(insert_query, (data['fi_name'], data['fi_description'], data['fi_macro'], data['fi_quantity'],
                       data['fi_cost_per_quantity'], data['fi_date_harvested'], data['fi_est_expiration'], data['fi_unit']))
        fi_id = cursor.fetchone()[0]

        # Insert relation into PRODUCER_FOOD_ITEM
        relation_insert_query = "INSERT INTO producer_food_item (pro_id, fi_id) VALUES (%s, %s)"
        cursor.execute(relation_insert_query, (producer_id, fi_id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Food item added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to fetch in-stock items for a specific producer
@app.route('/api/in-stock-items', methods=['GET'])
def get_in_stock_items():
    producer_name = request.args.get('producerName')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """
        SELECT fi.* FROM food_item fi
        JOIN producer_food_item pfi ON fi.fi_id = pfi.fi_id
        JOIN producer p ON pfi.pro_id = p.pro_id
        WHERE p.pro_name = %s AND fi.fi_quantity > 0
        """
        cursor.execute(query, (producer_name,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(items)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/recent-producer-orders', methods=['GET'])
def recent_producer_orders():
    producer_name = request.args.get('producerName')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """
        SELECT po.pur_id, po.pur_date, po.pur_status, po.pur_quantity, fi.fi_name
        FROM purchase_order po
        JOIN food_item fi ON po.pur_fi_id = fi.fi_id
        JOIN producer_food_item pfi ON fi.fi_id = pfi.fi_id
        JOIN producer p ON pfi.pro_id = p.pro_id
        WHERE p.pro_name = %s AND po.pur_status NOT IN ('Completed Pickup')
        ORDER BY po.pur_date DESC
        """
        cursor.execute(query, (producer_name,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(orders)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/upcoming-roles', methods=['GET'])
def get_upcoming_roles():
    volunteer_name = request.args.get('volunteerName')

    if not volunteer_name:
        return jsonify({'error': 'Volunteer name is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = """
        SELECT rs.vrol_id, rs.vrol_name, rs.vrol_description, rs.vrol_dates, 
               rs.vrol_start_time::text, rs.vrol_end_time::text
        FROM volunteer v
        JOIN volunteer_role vr ON v.vol_id = vr.vol_id
        JOIN role_slot rs ON vr.vrol_id = rs.vrol_id
        WHERE v.vol_name = %s AND rs.vrol_dates >= CURRENT_DATE
        """
        cursor.execute(query, (volunteer_name,))
        roles = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(roles)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/create-role', methods=['POST'])
def create_role():
    data = request.json
    volunteer_name = data.get('volunteerName')

    if not volunteer_name:
        return jsonify({'error': 'Volunteer name is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # First, get the hub ID associated with the volunteer
        cursor.execute(
            "SELECT vol_hub FROM volunteer WHERE vol_name = %s", (volunteer_name,))
        vol_hub_row = cursor.fetchone()
        if vol_hub_row is None:
            return jsonify({'error': 'Volunteer not found or hub not set'}), 404
        hub_id = vol_hub_row[0]

        # Insert new role into ROLE_SLOT table
        insert_query = """
        INSERT INTO role_slot (vrol_name, vrol_description, vrol_dates, vrol_start_time, vrol_end_time)
        VALUES (%s, %s, %s, %s, %s) RETURNING vrol_id
        """
        cursor.execute(insert_query, (data['vrol_name'], data['vrol_description'],
                       data['vrol_dates'], data['vrol_start_time'], data['vrol_end_time']))
        vrol_id = cursor.fetchone()[0]

        # Associate the new role with the volunteer's hub
        hub_role_insert_query = "INSERT INTO hub_role (hub_id, vrol_id) VALUES (%s, %s)"
        cursor.execute(hub_role_insert_query, (hub_id, vrol_id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Role created successfully', 'vrol_id': vrol_id}), 201

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sign-up-for-role', methods=['POST'])
def sign_up_for_role():
    data = request.json
    volunteer_name = data.get('volunteerName')
    vrol_id = data.get('vrol_id')

    if not volunteer_name or not vrol_id:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve the volunteer ID
        cursor.execute(
            "SELECT vol_id FROM volunteer WHERE vol_name = %s", (volunteer_name,))
        vol_id_row = cursor.fetchone()
        if vol_id_row is None:
            return jsonify({'error': 'Volunteer not found'}), 404
        vol_id = vol_id_row[0]

        # Sign up the volunteer for the role
        insert_query = "INSERT INTO volunteer_role (vol_id, vrol_id) VALUES (%s, %s)"
        cursor.execute(insert_query, (vol_id, vrol_id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Signed up for role successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/available-roles', methods=['GET'])
def available_roles():
    volunteer_name = request.args.get('volunteerName')

    if not volunteer_name:
        return jsonify({'error': 'Volunteer name is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Retrieve the hub ID associated with the volunteer
        cursor.execute(
            "SELECT vol_hub FROM volunteer WHERE vol_name = %s", (volunteer_name,))
        vol_hub_row = cursor.fetchone()
        if vol_hub_row is None:
            return jsonify({'error': 'Volunteer not found or hub not set'}), 404
        hub_id = vol_hub_row['vol_hub']

        # Retrieve roles associated with the hub, not assigned to other volunteers, and for today or later
        query = """
        SELECT rs.vrol_id, rs.vrol_name, rs.vrol_description, rs.vrol_dates, 
               rs.vrol_start_time::text, rs.vrol_end_time::text
        FROM role_slot rs
        JOIN hub_role hr ON rs.vrol_id = hr.vrol_id
        LEFT JOIN volunteer_role vr ON rs.vrol_id = vr.vrol_id
        WHERE hr.hub_id = %s AND vr.vol_id IS NULL AND rs.vrol_dates >= CURRENT_DATE
        """
        cursor.execute(query, (hub_id,))
        roles = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(roles)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/edit-role', methods=['POST'])
def edit_role():
    data = request.json
    vrol_id = data.get('vrol_id')
    new_date = data.get('new_date')
    new_start_time = data.get('new_start_time')
    new_end_time = data.get('new_end_time')

    if not vrol_id or not new_date or not new_start_time or not new_end_time:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Begin transaction
        cursor.execute("BEGIN;")

        # Update the role
        update_query = """
        UPDATE role_slot
        SET vrol_dates = %s, vrol_start_time = %s, vrol_end_time = %s
        WHERE vrol_id = %s
        """
        cursor.execute(
            update_query, (new_date, new_start_time, new_end_time, vrol_id))

        # Integrity check
        cursor.execute("""
            SELECT 1 FROM role_slot
            WHERE vrol_id = %s AND vrol_start_time < vrol_end_time
        """, (vrol_id,))
        if cursor.fetchone() is None:
            cursor.execute("ROLLBACK;")
            return jsonify({'error': 'New end time is earlier than start time. Rolling back transaction.'}), 400

        # Commit transaction
        cursor.execute("COMMIT;")
        cursor.close()
        conn.close()
        return jsonify({'message': 'Role updated successfully'}), 200

    except Exception as e:
        # Rollback in case of any exception
        cursor.execute("ROLLBACK;")
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
