# FarmToDBTable
COS457 Group Project

# README: import_create_table_data.py

## Overview

This Python script, `import_create_table_data.py`, automates the population of a PostgreSQL database with data related to Maine's food hubs. It includes importing data from CSV files into various database tables, creating associations between entities like schools and producers, and initializing certain logistics information for food distribution.

## Prerequisites

Before running this script, you should have:

1. **Python**: Python 3.6 or higher installed. [Download Python](https://www.python.org/downloads/).

2. **PostgreSQL Database**: A running instance of PostgreSQL. This script is compatible with PostgreSQL 14/15 and similar versions. [Download PostgreSQL](https://www.postgresql.org/download/).

## Python Libraries

Install the required Python libraries using pip:

```bash
pip install psycopg2
- `psycopg2`: A PostgreSQL database adapter for Python.
```

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

Navigate to the script's directory in a terminal or command prompt, and execute:

```bash
python import_create_table_data.py
```
**Database Verification:** Post-execution, check the database to ensure proper data population and associations.

### Additional Information
The script assumes all entities are in Maine, using default values for missing data.
Some of the information is real and publicly available, such as the producers and public school related tables.
Others, entirely fictional, made to fill out the database for us to test it out:
- Food items (inspired/filled with the top food items found in the MaineProducer.Csv file)
- Hubs (one for each county of Maine)
- Volunteers (check email for a blast from the past)


**Connection Issues:** If there are issues connecting to the database, check the PostgreSQL server status and configparams.json credentials.
This script will clobber any old versions of this database. If you see an error about not being able to delete due to another application using the database, close out any open queries in pgadmin. 


