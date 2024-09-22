import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="database",
    user="user",
    password="password",
    database="myapp"
)
cursor = conn.cursor()

# List of tables to truncate
tables = ['hlasovani', 'osoba', 'poslanec', 'poslanec_hlasovani', 'tisky', 'hist']

try:
    # Disable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # Truncate each table
    for table in tables:
        print(f"Truncating table: {table}")
        cursor.execute(f"TRUNCATE TABLE {table};")

    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Commit the changes
    conn.commit()

    print("All tables have been truncated successfully.")

except mysql.connector.Error as err:
    print(f"An error occurred: {err}")
    conn.rollback()

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
