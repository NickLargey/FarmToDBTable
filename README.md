# FarmToDBTable
COS457 Group Project

# README: create_db_and_fill.py

## Overview

This Python script, `create_db_and_fill.py`, automates the population of a PostgreSQL database with data related to Maine's food hubs. It includes importing data from CSV files into various database tables, creating associations between entities like schools and producers, and initializing certain logistics information for food distribution.

## Prerequisites

Before running this script, you should have:

1. **Python**: Python installed. [Download Python](https://www.python.org/downloads/).

2. **PostgreSQL Database**: A running instance of PostgreSQL. This script is compatible with PostgreSQL 14/15 and similar versions. [Download PostgreSQL](https://www.postgresql.org/download/).

## Python Libraries

Install the required Python libraries using pip:

```bash
pip install psycopg2
```
- `psycopg2`: A PostgreSQL database adapter for Python.


## Required Files

Place the following files in the same directory as the script:

- `MainePublicSchools.csv`: Data on schools in Maine.
- `MaineProducers.csv`: Information about food producers in Maine.
- `CreateTables.sql`: SQL script to create database tables.
- `TruncateAndResetIndex.sql`: Resets tables and indices if needed.
- `configparams.json`: Database configuration (username, password, host, etc.).

## Configuration and Execution

### Database Configuration

Edit `configparams.json` with your database details:
```json
{
    "dbname": "your_database_name",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}
```
## Run the Script

Navigate to the script's directory in a terminal or command prompt and execute:

```bash
python import_create_table_data.py
```
## Run Table Statistics in pgAdmin

To verify table population using pgAdmin:

1. **Open pgAdmin**: Launch pgAdmin and connect to your PostgreSQL database.

2. **Navigate to Your Database**: In the Browser panel, navigate to your database.

3. **Open Query Tool**:
    - Right-click on your database.
    - Select 'Query Tool' from the context menu.

4. **Load and Execute Script**:
    - In the Query Tool, click on the 'Open File' icon.
    - Navigate to and select the `TableStats.sql` file.
    - After the file contents are loaded into the Query Tool, execute the script by clicking the 'Execute/Refresh' button (F5).

This will run the `TableStats.sql` script and display a count of records in each table, confirming the successful data import and associations.

Note: Ensure `TableStats.sql` is located in an accessible directory on your computer.


## Additional Information


The script assumes all entities are in Maine, using default values for missing data.
Some information is real and publicly available, such as the producers and public school-related tables.
Others, entirely fictional, made to fill out the database for us to test it out:
- Food items (inspired/filled with the top food items found in the MaineProducer.Csv file)
- Hubs (one for each county of Maine)
- Volunteers (check email for a blast from the past)


**Connection Issues:** If there are issues connecting to the database, check the PostgreSQL server status and configparams.json credentials.
This script will clobber any old versions of this database. If you see an error about being unable to delete because of another application using the database, please close out any open queries in pgadmin. 


