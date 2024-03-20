import requests
import sqlite3
import base64

# Replace these with your actual API key and domain
API_KEY = '000000000000000000:X'
DOMAIN_NAME = 'mycompany.freshservice.com'  # Make sure to add .freshservice.com or your actual domain suffix

# Base64 encode the API key
encoded_api_key = base64.b64encode(API_KEY.encode()).decode()

# Construct the request URL
url = f'https://{DOMAIN_NAME}/api/v2/tickets?page=9'

# Headers for authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_api_key}'
}

# Perform the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Assuming the API might return multiple tickets, we iterate through them
    tickets = response.json().get('tickets', [])  # Adjusted to handle multiple tickets
    
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Create the tickets table if it does not exist
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY,
        subject TEXT,
        priority INTEGER,
        status INTEGER,
        requester_id INTEGER,
        responder_id INTEGER,
        created_at TEXT,
        updated_at TEXT,
        due_by TEXT,
        description_text TEXT
    );
    '''
    cursor.execute(create_table_query)
    
    # Prepare the insert query
    insert_query = '''INSERT INTO tickets (id, subject, priority, status, requester_id, responder_id, created_at, updated_at, due_by, description_text)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET
                      subject=excluded.subject,
                      priority=excluded.priority,
                      status=excluded.status,
                      requester_id=excluded.requester_id,
                      responder_id=excluded.responder_id,
                      created_at=excluded.created_at,
                      updated_at=excluded.updated_at,
                      due_by=excluded.due_by,
                      description_text=excluded.description_text;'''
    
    for ticket in tickets:  # Adjusting to iterate through potentially multiple tickets
        ticket_data = (
            ticket['id'],
            ticket['subject'],
            ticket['priority'],
            ticket['status'],
            ticket['requester_id'],
            ticket['responder_id'],
            ticket['created_at'],
            ticket['updated_at'],
            ticket['due_by'],
            ticket['description_text']
        )
        
        cursor.execute(insert_query, ticket_data)
    
    conn.commit()
    
    # Close the database connection
    conn.close()
    print(f"{len(tickets)} tickets inserted/updated successfully.")
else:
    print("Failed to retrieve ticket data. Status Code:", response.status_code)
