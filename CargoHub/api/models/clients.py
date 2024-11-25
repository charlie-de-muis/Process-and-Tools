# DONE

import sqlite3

from models.base import Base
from models.Database_file import db_start

class Clients(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def get_clients(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM clients LIMIT 10"
        cursor.execute(query)
        clients = cursor.fetchall()  # Fetch a single row
        
        if clients is None:
            print("No clients found")
            return None

        cursor.close()
        conn.close()
        return clients

    def get_client(self, client_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        try:
            # Use the correct placeholder "?" for SQLite
            query = "SELECT * FROM clients WHERE id = ?"
            cursor.execute(query, (client_id,))  # Pass the client_id as a tuple
            client = cursor.fetchone()  # Fetch a single row
            
            if client is None:
                print(f"No client with id {client_id}")
                return None

            return client

        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()
        
    def add_client(self, client):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        client["created_at"] = self.get_timestamp()
        client["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO clients (
            id, name, address, city, zip_code, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data = (
            client['id'], 
            client['name'], 
            client['address'], 
            client['city'], 
            client['zip_code'], 
            client['province'], 
            client['country'], 
            client['contact_name'], 
            client['contact_phone'], 
            client['contact_email'], 
            client['created_at'],
            client['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Client {client['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_client(self, client_id, client):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the client exists
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client_old = cursor.fetchone()
            if client_old is None:
                print("Client not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE clients SET
                    name = ?,
                    address = ?,
                    city = ?,
                    zip_code = ?,
                    province = ?,
                    country = ?,
                    contact_name = ?,
                    contact_phone = ?,
                    contact_email = ?,
                    created_at = ?,
                    updated_at = ?
                WHERE id = ?
            """

            # Execute the update query
            cursor.execute(update_query, (
                client['name'],
                client['address'],
                client['city'],
                client['zip_code'],
                client['province'],
                client['country'],
                client['contact_name'],
                client['contact_phone'],
                client['contact_email'],
                client['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                client_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Client updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_client(self, client_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM clients WHERE id = {client_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
