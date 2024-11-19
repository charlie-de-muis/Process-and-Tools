# DONE

import psycopg2

from models.base import Base
from models.Database_file import db_start

TRANSFERS = []

class Transfers(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_transfers (self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM transfers LIMIT 10"
        cursor.execute(query)
        transfers = cursor.fetchall()  # Fetch a single row
        
        if transfers is None:
            print("No transfers found")
            return None

        cursor.close()
        conn.close()
        return transfers

    def get_transfer(self, transfer_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM transfers  WHERE id = %s"
        cursor.execute(query, (transfer_id,))
        transfer = cursor.fetchone()  # Fetch a single row
        
        if transfer is None:
            print(f"No transfer with id {transfer_id}")
            return None

        cursor.close()
        conn.close()
        return transfer
        
    def get_items_in_transfer(self, transfer_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails

        try:
            cursor = conn.cursor()

            # Query to fetch the transfer details along with its items
            query = """
                SELECT items FROM transfers WHERE id = %s
            """
            cursor.execute(query, (transfer_id,))

            # Fetch the result
            result = cursor.fetchone()

            if result is None:
                print(f"Transfer with id {transfer_id} not found")
                return None

            # Assuming items is a JSON column in the 'transfers' table
            items = result[0]  # Extract the items from the result

            return items

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Return None in case of any error

        finally:
            cursor.close()
            conn.close()

    def add_transfer(self, transfer):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO transfers (
            id, code, name, address, zip, city, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        data = (
            transfer['reference'],
            transfer['transfer_from'],
            transfer['transfer_to'],
            transfer['transfer_status'],
            transfer['created_at'],
            transfer['updated_at'],
            transfer['items_item_id'],
            transfer['items_amount'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Transfer {transfer['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_transfer(self, transfer_id, transfer):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the transfer exists
            cursor.execute("SELECT * FROM transfers WHERE id = %s", (transfer_id,))
            transfer_old = cursor.fetchone()
            if transfer_old is None:
                print("Transfer not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Transfers SET
                    reference = %s,
                    transfer_from = %s,
                    transfer_to = %s,
                    transfer_status = %s,
                    created_at = %s
                    updated_at = %s
                    items_item_id = %s
                    items_amount = %s
                WHERE id = %s
            """

            # Execute the update query
            cursor.execute(update_query, (
                transfer['reference'],
                transfer['transfer_from'],
                transfer['transfer_to'],
                transfer['transfer_status'],
                transfer['created_at'],
                transfer['updated_at'],
                transfer['items_item_id'],
                transfer['items_amount'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                transfer_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Transfer updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_transfer (self, transfer_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM transfers WHERE id = {transfer_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()

