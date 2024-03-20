import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('tickets.db')
cursor = conn.cursor()

# SQL query to fetch all tickets from the database
query = "SELECT * FROM tickets"

try:
    cursor.execute(query)
    tickets = cursor.fetchall()  # Fetch all tickets from the database
    
    # Check if there are any tickets
    if tickets:
        print("Retrieved tickets from the database:")
        for ticket in tickets:
            print(f"ID: {ticket[0]}, Subject: {ticket[1]}, Priority: {ticket[2]}, Status: {ticket[3]}, " \
                  f"Requester ID: {ticket[4]}, Responder ID: {ticket[5]}, Created At: {ticket[6]}, " \
                  f"Updated At: {ticket[7]}, Due By: {ticket[8]}, Description: {ticket[9]}")
    else:
        print("No tickets found in the database.")
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Exception in _query: {e}")

# Close the database connection
conn.close()
