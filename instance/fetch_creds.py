import sqlite3

# Path to the SQLite database
db_path = "C:/Users/Ashay-PC/Desktop/Vishal N/m_mpharmacy/instance/pharmacy.db"  # Update this path

# Connect to the database
conn = sqlite3.connect(db_path)

# Create a cursor to interact with the database
cursor = conn.cursor()

# Fetch column names
try:
    cursor.execute("PRAGMA table_info(user);")  # Replace 'user' with your table name
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]  # Extract column names
    print(f"Columns in the 'user' table: {column_names}")

    # Fetch all rows
    cursor.execute("SELECT * FROM user;")
    rows = cursor.fetchall()
    print("\nRows in the 'user' table:")
    for row in rows:
        print(row)
except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.close()
