import psycopg2
import csv

# PostgreSQL Connection Details
DB_NAME = "EV"  # Change if different
DB_USER = "postgres"
DB_PASS = "@Ankur7753"  # Ensure this password is correct
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Define Insert Query
insert_query = """
INSERT INTO potential_locations (name, latitude, longitude, type) 
VALUES (%s, %s, %s, %s);
"""

# Read CSV and Insert Data
csv_filename = "potential_locations.csv"  # Ensure this file exists
with open(csv_filename, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        cursor.execute(insert_query, (row[0], float(row[1]), float(row[2]), row[3]))

# Commit & Close
conn.commit()
cursor.close()
conn.close()
print("✅ Data inserted into PostgreSQL successfully!")
