# FarmToDBTable Project Comprehensive README

Link: https://github.com/NickLargey/FarmToDBTable/

## Introduction

FarmToDBTable is an innovative project designed to enhance the food supply chain in Maine by connecting local producers, schools, and volunteers through a robust database system. This system, leveraging a PostgreSQL database and a Flask-based web application, facilitates the sourcing, distribution, and management of locally produced food.

## Getting Started

### Step 1: Clone the Repository

Start by cloning the FarmToDBTable repository to your local machine:

```bash
git clone https://github.com/NickLargey/FarmToDBTable/
```

### Step 2: Install Dependencies

Navigate to the cloned repository and install the necessary Python libraries(and if neccessary Python itself):

```bash
pip install Flask flask_cors flask_sqlalchemy psycopg2
```

### Step 3: Configure Database Connection

1. In a text editor, open `App/Backend/configparams.json`.

2. Install Postgres/pgAdmin and record the user, password, and port details in the json file and save.

Note: Ensure you use PostgreSQL version 15.x or earlier as later versions may have compatibility issues.

3. In pgAdmin, navigate to 'Object Explorer' > Servers > PostgreSQL version 15.x. Enter the password to connect.

4. Update `configparams.json` with your database details (user, password, host, port).

### Step 4: Populate Database

From the command line, navigate to `App/Backend` in the cloned repository:

```bash
cd path/to/FarmToDBTable/App/Backend
```

Run the script to create and populate the database:

```bash
python create_db_and_fill.py
```
You must go into Pgadmin and click on the FarmtoDB to initialize your server, then minimize.

### Step 5: Launch the Flask Backend

Still in the `App/Backend` directory, start the Flask app:

```bash
python app.py
```

Keep this terminal open to maintain the backend service.

### Step 6: Access the Frontend Application

1. Navigate to `FarmToDBTable/App/FrontEnd` in a file browser.

2. Open `index.html`. This should launch the web application in your default browser.

## Using the Application

### User Registration and Login

- Register as a School, Volunteer, or Producer, it will allow you to bypass login and go straight to the dashboard.
- Login using existing credentials.

### Dashboard Functionality

- **School Dashboard**:
  - View the latest food items at the school's hub (Harvest Feed).
  - Create Purchase Orders from available food items.
  - View recent Purchase Orders.
  - Access the Advanced Search Widget.

- **Producer Dashboard**:
  - Track items available at the hub.
  - Add new food items to the hub.
  - Monitor Orders in Progress.
  - Use the Advanced Search Widget.

- **Volunteer Dashboard**:
  - See upcoming roles.
  - Create new roles for the hub.
  - Sign up for hub roles.
  - Edit existing roles.

## Additional Information

- **Flask Backend**: The Flask backend serves the web application's API. Ensure it's always running while using the app.

- **Database Setup**: The `create_db_and_fill.py` script initializes the database with mock data for testing, you don't need to run this again each time you use the app locally. If you do, know that all queries must be closed in Pgadmin before running as it deletes and rebuilds the database/it's contents to ensure reproducability without room for leftovers causing variance. 

- **Frontend Application**: The `index.html` in the `FrontEnd` folder is the entry point for the web application.

## Troubleshooting

- **Database Connection**: If connection issues arise, verify PostgreSQL server status and `configparams.json` credentials.

- **Web Application**: Ensure the Flask backend is running (on port 5001 by default) before accessing the frontend application.

## Contact

For any queries or issues, feel free to reach out to the development team.

---

