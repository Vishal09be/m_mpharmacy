import sqlite3

# Path to the SQLite database
db_path = "pharmacy.db"

# Connect to the database
conn = sqlite3.connect(db_path)

# Fetch SQLite version
sqlite_version = sqlite3.sqlite_version
print(f"SQLite version: {sqlite_version}")

# Check database tables (optional)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables in the database: {tables}")

# Close the connection
conn.close()
