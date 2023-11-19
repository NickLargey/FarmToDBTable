import csv
import psycopg2
import json
from collections import Counter
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

def database_exists(conn, dbname):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        return cur.fetchone() is not None

def drop_and_create_database(db_config):
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(user=db_config["user"], password=db_config["password"], host=db_config["host"], port=db_config["port"])
    
    # Set the isolation level for the connection to AUTOCOMMIT
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        with conn.cursor() as cur:
            # Drop the database if it exists
            cur.execute(f"DROP DATABASE IF EXISTS {db_config['dbname']}")
            # Create a new database
            cur.execute(f"CREATE DATABASE {db_config['dbname']}")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()
            
def execute_sql_file(filename, connection):
    with open(filename, 'r') as file:
        sql_script = file.read()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_script)
            connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()


def import_schools(cursor):
    # Open and parse the CSV file
    with open('MainePublicSchools.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract data from each row
            sch_name = row['School Name']
            sch_id = row['School ID']
            sch_email = row['Contact Email']
            sch_phone = row['Phone']
            sch_address = row['Mailing Street']
            sch_city = row['Mailing City']
            sch_state = 'ME'  # Assuming all schools are in Maine
            sch_zip = row['Mailing Zip']
            sch_county = row['County']

            # Insert data into the SCHOOL table
            cursor.execute("""
                INSERT INTO SCHOOL (sch_id, sch_name, sch_email, sch_phone, sch_address, sch_city, sch_state, sch_zip, sch_county)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (sch_id, sch_name, sch_email, sch_phone, sch_address, sch_city, sch_state, sch_zip, sch_county))

def create_hubs(cursor):
    # List of counties in Maine
    counties = ["Cumberland", "Franklin", "Piscataquis", "Kennebec", "Oxford", "Androscoggin", "Waldo", "Washington", "York", "Lincoln", "Knox", "Hancock", "Sagadahoc", "Somerset", "Aroostook", "Penobscot"]
    
    for county in counties:
        # Create a hub for each county (adjust the values as needed)
        hub_name = county + " Hub"
        hub_address = "Some address in " + county  # Placeholder address
        hub_city = "City in " + county  # Placeholder city
        hub_zip = "00000"  # Placeholder ZIP code
        hub_hours = "9AM - 5PM"  # Placeholder hours

        cursor.execute("""
            INSERT INTO HUB (hub_name, hub_address, hub_city, hub_state, hub_zip, hub_hours, hub_county)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (hub_name, hub_address, hub_city, 'ME', hub_zip, hub_hours, county))
        
def import_producers(cursor):
    with open('MaineProducers.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pro_name = row['Farm/Producer']
            pro_email = row.get('Email', 'Not provided')  # Default value if not provided
            pro_phone = row.get('Phone', 'Not provided')
            pro_address = row['Address']
            pro_city = row['Town']
            pro_state = 'ME'  # Assuming Maine
            pro_zip = '00000'  # Not provided in our data
            pro_county = row['County']

            cursor.execute("""
                INSERT INTO PRODUCER (pro_name, pro_email, pro_phone, pro_address, pro_city, pro_state, pro_zip, pro_county)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (pro_name, pro_email, pro_phone, pro_address, pro_city, pro_state, pro_zip, pro_county))


def get_food_item_counts(macro_columns):
    food_counter = Counter()
    with open('MaineProducers.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for macro in macro_columns:
                if row[macro]:  # Check if the macro column is not empty
                    # Remove punctuation, split the string into individual words, make lowercase and strip spaces
                    translator = str.maketrans('', '', string.punctuation)
                    items = [word.translate(translator).strip().lower() 
                             for item in row[macro].split(',') 
                             for word in item.split()]
                    # Filter out empty strings
                    items = [item for item in items if item]
                    # Update the counter with the list of food items
                    food_counter.update(items)
    return food_counter.most_common(100)  # Return the top 100 most common items

def associate_producers_with_hubs(cursor):
    cursor.execute("SELECT hub_id, hub_county FROM hub")
    hub_map = {county: hub_id for hub_id, county in cursor.fetchall()}

    cursor.execute("SELECT pro_id, pro_county FROM producer")
    producers = cursor.fetchall()
    for pro_id, pro_county in producers:
        hub_id = hub_map.get(pro_county)
        if hub_id:
            cursor.execute("INSERT INTO hub_producer (hub_id, pro_id) VALUES (%s, %s)", (hub_id, pro_id))

def associate_schools_with_hubs(cursor):
    cursor.execute("SELECT hub_id, hub_county FROM hub")
    hub_map = {county: hub_id for hub_id, county in cursor.fetchall()}

    cursor.execute("SELECT sch_id, sch_county FROM school")
    schools = cursor.fetchall()
    for sch_id, sch_county in schools:
        hub_id = hub_map.get(sch_county)
        if hub_id:
            cursor.execute("INSERT INTO hub_school (hub_id, sch_id) VALUES (%s, %s)", (hub_id, sch_id))
 
 
def associate_producers_with_food_items(cursor):
    # Define the date range and create a list of months
    start_date = datetime(2022, 8, 1)
    end_date = datetime(2023, 8, 31)
    months = [start_date + timedelta(days=i * 30) for i in range(12)]
    
    food_macro_dict = {
    'vegetables': {'items': ['greens', 'tomatoes', 'carrots', 'potatoes', 'garlic', 'squash', 'lettuce', 'onions', 'peppers', 'corn', 'beets', 'cucumbers'], 'unit': 'lb'},
    'meat': {'items': ['beef', 'pork', 'chicken', 'sausage'], 'unit': 'lb'},
    'seafood': {'items': ['clam', 'oyster', 'scallop', 'cod', 'haddock', 'crab', 'mussel'], 'unit': 'lb'},
    'eggs': {'items': ['eggs'], 'unit': 'each'},
    'dairy': {'items': ['milk', 'cheese', 'yogurt'], 'unit': 'lb'},
    'fruits': {'items': ['apples', 'blueberries', 'strawberries', 'beans', 'raspberries', 'peaches', 'pears'], 'unit': 'lb'},
    'grains': {'items': ['flour', 'oats', 'cornmeal'], 'unit': 'lb'},
    'maple': {'items': ['maple syrup'], 'unit': 'pint'}
    }
    
    # Initialize the macro index
    macro_index = 0
    
    # Define attribute ranges
    quantity_range = (1, 1000)  # Example: Quantity range from 1 to 1000
    cost_range = (1.0, 5.0)  # Example: Cost per quantity range from 1.0 to 5.0
    
    # Initialize attribute values
    current_quantity = quantity_range[0]
    current_cost = cost_range[0]
    
    # Loop through producer IDs in the range 1 to 517
    for pro_id in range(1, 518):
        for month in months:
            # Get the current macro and its associated food items
            current_macro = list(food_macro_dict.keys())[macro_index]
            food_items = food_macro_dict[current_macro]['items']
            unit = food_macro_dict[current_macro]['unit']

            # Choose a food item from the current macro's list based on the month
            food_item = food_items[(month.month - 1) % len(food_items)]  # Repeat available items

            # Extract the relevant values from food_macro_dict
            fi_name = food_item
            fi_macro = current_macro
            fi_date_harvested = month
            fi_est_expiration = month + timedelta(days=7)
            fi_unit = unit

            # Insert the food item into the database with producer information
            cursor.execute("""
                INSERT INTO food_item (fi_name, fi_macro, fi_date_harvested, fi_est_expiration, fi_unit, fi_quantity, fi_cost_per_quantity) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING fi_id
            """, (fi_name, fi_macro, fi_date_harvested, fi_est_expiration, fi_unit, current_quantity, current_cost))

            fi_id = cursor.fetchone()[0]

            # Associate the producer with the food item
            cursor.execute("""
                INSERT INTO producer_food_item (pro_id, fi_id) 
                VALUES (%s, %s)
            """, (pro_id, fi_id))

            # Increment attribute values (within defined ranges)
            current_quantity = (current_quantity % quantity_range[1]) + 1
            current_cost = (current_cost % cost_range[1]) + 1.0

            # Move to the next macro (cycling back to the first macro if necessary)
            macro_index = (macro_index + 1) % len(food_macro_dict)
            
        cursor.connection.commit()  # Commit the changes to the database
            
            
def create_purchase_orders_for_schools(cursor):
    start_date = datetime(2022, 8, 1)
    end_date = datetime(2023, 7, 31)
    current_date = start_date

    # List of different quantities
    order_quantities = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

    while current_date <= end_date:
        for hub_id in range(1, 17):
            
            # Define the first and last day of the current month
            first_day_of_month = current_date.replace(day=1)
            if current_date.month == 12:
                last_day_of_month = current_date.replace(day=31)
            else:
                last_day_of_month = current_date.replace(day=1, month=current_date.month + 1, year=current_date.year) - timedelta(days=1)
            
            # Retrieve food items for the hub
            cursor.execute("""
                SELECT fi.fi_id, fi.fi_quantity
                FROM food_item fi
                INNER JOIN producer_food_item pfi ON fi.fi_id = pfi.fi_id
                INNER JOIN hub_producer hp ON pfi.pro_id = hp.pro_id
                WHERE hp.hub_id = %s 
                AND fi.fi_date_harvested <= %s 
                AND fi.fi_est_expiration >= %s 
                AND fi.fi_quantity > 0
                ORDER BY fi.fi_id
            """, (hub_id, last_day_of_month, first_day_of_month))
            food_items = cursor.fetchall()

            if not food_items:
                continue

            # Retrieve schools for the hub
            cursor.execute("""
                SELECT s.sch_id
                FROM school s
                INNER JOIN hub_school hs ON s.sch_id = hs.sch_id
                WHERE hs.hub_id = %s
            """, (hub_id,))
            schools = cursor.fetchall()

            if not schools:
                continue

            for school in schools:
                fi_id, fi_quantity = food_items[0]
                order_quantity = min(fi_quantity, order_quantities[school[0] % len(order_quantities)])  # Use order_quantities list
                purchase_order = (current_date, order_quantity, order_quantity * 2.5, fi_id, 'Awaiting Fulfillment')

                # Insert purchase order
                cursor.execute("""
                    INSERT INTO purchase_order (pur_date, pur_quantity, pur_total_price, pur_fi_id, pur_status)
                    VALUES (%s, %s, %s, %s, %s) RETURNING pur_id
                """, purchase_order)
                pur_id = cursor.fetchone()[0]

                # Insert school_purchase_order
                cursor.execute("""
                    INSERT INTO school_purchase_order (sch_id, pur_id)
                    VALUES (%s, %s)
                """, (school[0], pur_id))

                # Update food item quantity
                new_quantity = fi_quantity - order_quantity
                cursor.execute("""
                    UPDATE food_item
                    SET fi_quantity = %s
                    WHERE fi_id = %s
                """, (new_quantity, fi_id))

                # Check if the food item is still available, if not, remove it from the list
                if new_quantity <= 0:
                    food_items.pop(0)

                cursor.connection.commit()

        current_date += relativedelta(months=1)
        
        
def populate_volunteers_and_roles(cursor):
    # Volunteer first names and role names
    volunteer_first_names = ["Aimee", "Nick", "Sean"]
    role_names = ["Hub Attendant", "Producer Pick Up", "School Drop Off"]

    # Start and end dates for the roles
    start_date = datetime(2022, 8, 1)
    end_date = datetime(2023, 7, 31)

    # Query to get hub data
    cursor.execute("SELECT hub_id, hub_county FROM hub")
    hubs = cursor.fetchall()

    for hub_id, hub_county in hubs:
        current_date = start_date
        volunteer_last_name = hub_county

        # Add volunteers for this hub
        for first_name in volunteer_first_names:
            vol_name = f"{first_name} {volunteer_last_name}"
            cursor.execute("""
                INSERT INTO volunteer (vol_name, vol_hub) VALUES (%s, %s)
            """, (vol_name, hub_id))
            cursor.connection.commit()

        while current_date <= end_date:
            for role_name in role_names:
                # Create multiple role slots per month for each role
                for week in range(1, 5):  # Assuming 4 weeks in a month
                    vrol_description = f"{role_name} role for {hub_county} hub, week {week}"
                    role_date = current_date + timedelta(days=7 * (week - 1))

                    cursor.execute("""
                        INSERT INTO role_slot (vrol_name, vrol_description, vrol_dates, vrol_start_time, vrol_end_time)
                        VALUES (%s, %s, %s, '09:00:00', '17:00:00')
                    """, (role_name, vrol_description, role_date))
                    cursor.connection.commit()
                    
                    # Create a hub_role association for each role_slot
                    cursor.execute("SELECT LASTVAL()")
                    last_vrol_id = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO hub_role (hub_id, vrol_id) VALUES (%s, %s)
                    """, (hub_id, last_vrol_id))
                    cursor.connection.commit()

                    # Randomly decide whether to fill this role slot
                    if week % 2 == 0:  # Example condition to fill some slots
                        cursor.execute("SELECT vol_id FROM volunteer WHERE vol_hub = %s LIMIT 1", (hub_id,))
                        volunteer = cursor.fetchone()
                        if volunteer:
                            # Get the last inserted vrol_id
                            cursor.execute("SELECT LASTVAL()")
                            last_vrol_id = cursor.fetchone()[0]

                            cursor.execute("""
                                INSERT INTO volunteer_role (vol_id, vrol_id) VALUES (%s, %s)
                            """, (volunteer[0], last_vrol_id))
                            cursor.connection.commit()

                # Move to the next month
                current_date += relativedelta(months=1)




def main():
    # Load database configuration from json file
    with open('configparams.json', 'r') as file:
        db_config = json.load(file)
    
    # Drop the existing database (if it exists) and create a new one
    drop_and_create_database(db_config)
    
    # Wait for a moment to ensure the database server has registered the new database
    time.sleep(5)


    # Connect to the PostgreSQL database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Execute the CreateTable.sql script
            execute_sql_file('CreateTables.sql', conn)

            # Execute the TruncateAndResetIndex.sql script in case index is left over from old db
            execute_sql_file('TruncateAndResetIndex.sql', conn)
            
            # Fill the tables
            import_schools(cursor)
            create_hubs(cursor)
            import_producers(cursor)
            associate_producers_with_hubs(cursor)
            associate_schools_with_hubs(cursor)
            associate_producers_with_food_items(cursor)
            create_purchase_orders_for_schools(cursor)
            populate_volunteers_and_roles(cursor)
            
            

if __name__ == "__main__":
    main()

