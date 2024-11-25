# DONE

import sqlite3
import json

from api.models.base import Base
from api.models.Database_file import db_start

TRANSFERS = []

class Transfers(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets (self):
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

    def get(self, transfer_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM transfers  WHERE id = ?"
        cursor.execute(query, (transfer_id,))
        transfer = cursor.fetchone()  # Fetch a single row
        
        if transfer is None:
            print(f"No transfer with id {transfer_id}")
            return None

        cursor.close()
        conn.close()
        return self.convert_to_dict(transfer)
        
    # def get_items_in_transfer(self, transfer_id):
        # conn = self.db.connection(self.dbfile)
        # if conn is None:
        #     print("DB connection failed")
        #     return None  # Exit if connection fails

        # try:
        #     cursor = conn.cursor()

        #     # Query to fetch the transfer details along with its items
        #     query = """
        #         SELECT items FROM transfers WHERE id = ?
        #     """
        #     cursor.execute(query, (transfer_id,))

        #     # Fetch the result
        #     result = cursor.fetchone()

        #     if result is None:
        #         print(f"Transfer with id {transfer_id} not found")
        #         return None

        #     # Assuming items is a JSON column in the 'transfers' table
        #     items = result[0]  # Extract the items from the result

        #     return items

        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     return None  # Return None in case of any error

        # finally:
        #     cursor.close()
        #     conn.close()

    def add(self, transfer):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO transfers (
            id, reference, transfer_from, transfer_to, transfer_status, created_at, updated_at, items
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
        
        items = json.dumps(transfer['items'])
        data = (
            transfer['id'],
            transfer['reference'],
            transfer['transfer_from'],
            transfer['transfer_to'],
            transfer['transfer_status'],
            transfer['created_at'],
            transfer['updated_at'],
            items)
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Transfer {transfer['reference']} added successfully.")

        cursor.close()
        conn.close()

    def update(self, transfer_id, transfer):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the transfer exists
            cursor.execute("SELECT * FROM transfers WHERE id = ?", (transfer_id,))
            transfer_old = cursor.fetchone()
            if transfer_old is None:
                print("Transfer not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Transfers SET
                    reference = ?,
                    transfer_from = ?,
                    transfer_to = ?,
                    transfer_status = ?,
                    created_at = ?
                    updated_at = ?
                    items_item_id = ?
                    items_amount = ?
                WHERE id = ?
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

    def remove(self, transfer_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM transfers WHERE id = {transfer_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, transfer):
        """
        Converts a transfer tuple fetched from the database into a dictionary
        with the structure of the given JSON.
        """
        # If 'items' is a JSON string, you may want to convert it back to a list (assumed)
        items = transfer[7]
        if items:
            items = json.loads(items)  # If 'items' is a JSON string, parse it as a list
        else:
            items = []

        return {
            'id': transfer[0],  # Unique identifier for the transfer
            'reference': transfer[1],  # Transfer reference
            'transfer_from': transfer[2],  # Origin of the transfer
            'transfer_to': transfer[3],  # Destination of the transfer (typically an integer or ID)
            'transfer_status': transfer[4],  # Status of the transfer
            'created_at': transfer[5],  # Timestamp of when the transfer was created
            'updated_at': transfer[6],  # Timestamp of when the transfer was last updated
            'items': items,  # List of items (parsed from JSON string if applicable)
        }
