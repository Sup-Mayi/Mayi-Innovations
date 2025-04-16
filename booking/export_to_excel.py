import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect('db.sqlite3')  # Replace with your database file path

# Query the data from your desired table
df = pd.read_sql_query("SELECT * FROM your_table_name;", conn)  # Replace with your table name

# Export the data to an Excel file
df.to_excel('output.xlsx', index=False)

# Close the database connection
conn.close()

print("Data has been exported to 'output.xlsx' successfully.")
