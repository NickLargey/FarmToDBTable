import zipfile
import os
import psycopg2
import json
import shutil


def execute_sql(sql_folder, connection, output_file_path):
    with open(output_file_path, "w") as output_file:
        for root, _, files in os.walk(sql_folder):
            for file_name in files:
                if file_name.endswith(".sql"):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, "r") as sql_file:
                        sql_script = sql_file.read()
                        with connection.cursor() as cursor:
                            cursor.execute(sql_script)
                            results = cursor.fetchall()
                            output_file.write(
                                ' # '*10 + file_name + ' # '*10 + '\n\n' + str(results) + "\n\n")
                    connection.commit()


# Path to the zipped folder containing SQL files
zip_folder_path = "./queries.zip"
# Temporary folder to extract SQL files
extracted_folder = "temp_folder"
# Output file to read query results
output_file_path = "output.txt"

try:
    # Extract the zipped folder
    with zipfile.ZipFile(zip_folder_path, "r") as zip_ref:
        zip_ref.extractall(extracted_folder)
    # Load database configuration from json file
    with open('configparams.json', 'r') as file:
        db_config = json.load(file)

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            database=db_config["dbname"], user=db_config["user"], password=db_config["password"], host=db_config["host"], port=db_config["port"])

        # Execute SQL files in the extracted folder
        execute_sql(extracted_folder, conn, output_file_path)

    # Close the database conn
    conn.close()
except Exception as e:
    if not psycopg2.ProgrammingError:
        print(f"An error occurred: {str(e)}")
finally:
    # Clean up: remove the temporary folder
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)
