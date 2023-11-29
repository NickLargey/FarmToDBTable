from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
CORS(app)
# Define a function to execute SQL queries


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


if __name__ == "__main__":
    app.run(debug=True)
