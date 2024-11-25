import sqlite3
import json

from api.models.base import Base
from api.models.Database_file import db_start

INVENTORIES = []

class Inventories(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM inventories LIMIT 10"
        cursor.execute(query)
        inventories = cursor.fetchall()  # Fetch a single row
        
        if inventories is None:
            print("No inventories found")
            return None

        cursor.close()
        conn.close()
        return inventories

    def get(self, inventory_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        try:
            # Use the correct placeholder "?" for SQLite
            query = "SELECT * FROM inventories WHERE id = ?"
            cursor.execute(query, (inventory_id,))  # Pass the client_id as a tuple
            inv = cursor.fetchone()  # Fetch a single row
            
            if inv is None:
                print(f"No inventory with id {inventory_id}")
                return None

            return self.convert_to_dict(inv)

        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # def get_inventories_for_item(self, item_id):
    #     conn = self.db.connection(self.dbfile)
    #     if conn is None:
    #         print("DB connection failed")
    #         return None  # Exit if connection fails
        
    #     try:
    #         cursor = conn.cursor()

    #         # Parameterized query to prevent SQL injection
    #         query = "SELECT * FROM inventories WHERE item_id = ?"
    #         cursor.execute(query, (item_id,))
            
    #         inventories = cursor.fetchall()  # Fetch all records matching the item_id

    #         if not inventories:
    #             print(f"No inventories found for item ID {item_id}")
    #             return []  # Return empty list if no records are found

    #         return inventories  # Return the list of inventory records
        
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return None
    #     finally:
    #         cursor.close()
    #         conn.close()

    # def get_inventory_totals_for_item(self, item_id):
        # result = {
        #     "total_expected": 0,
        #     "total_ordered": 0,
        #     "total_allocated": 0,
        #     "total_available": 0
        # }

        # conn = self.db.connection(self.dbfile)
        # if conn is None:
        #     print("DB connection failed")
        #     return None  # Exit if connection fails
        
        # try:
        #     cursor = conn.cursor()

        #     # Parameterized query to get totals for each column
        #     query = """
        #         SELECT total_expected, total_ordered, total_allocated, total_available
        #         FROM inventories
        #         WHERE item_id = ?
        #     """
        #     cursor.execute(query, (item_id,))
            
        #     inventories = cursor.fetchall()  # Fetch all inventory records

        #     if not inventories:
        #         print(f"No inventories found for item ID {item_id}")
        #         return result  # Return default result if no records found

        #     # Summing up the totals for the given item_id
        #     for inventory in inventories:
        #         result["total_expected"] += inventory[0]
        #         result["total_ordered"] += inventory[1]
        #         result["total_allocated"] += inventory[2]
        #         result["total_available"] += inventory[3]

        #     return result  # Return the calculated totals
        
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     return None
        # finally:
        #     cursor.close()
        #     conn.close()

    def add(self, inventory):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        
        cursor = conn.cursor()

        # Setting timestamps
        inventory["created_at"] = self.get_timestamp()
        inventory["updated_at"] = self.get_timestamp()
        
        # Inserting data into the inventories table
        query = """INSERT INTO inventories (
            id, item_id, description, item_reference, locations, 
            total_on_hand, total_expected, total_ordered, 
            total_allocated, total_available, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        location = json.dumps(inventory['locations'])
        # Preparing the data tuple, including serializing locations as a JSON string
        data = (
            inventory['id'],
            inventory['item_id'],
            inventory['description'],
            inventory['item_reference'],
            location,
            inventory['total_on_hand'],
            inventory['total_expected'],
            inventory['total_ordered'],
            inventory['total_allocated'],
            inventory['total_available'],
            inventory['created_at'],
            inventory['updated_at']
        )
        
        try:
            cursor.execute(query, data)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting inventory data: {e}")
            return None

        print(f"Inventory item {inventory['item_id']} added successfully.")

        cursor.close()
        conn.close()

    def update(self, inventory_id, inventory):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the inventory item exists
            cursor.execute("SELECT * FROM inventories WHERE id = ?", (inventory_id,))
            inventory_old = cursor.fetchone()
            if inventory_old is None:
                print("Inventory item not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE inventories SET
                    item_id = ?,
                    description = ?,
                    item_reference = ?,
                    locations = ?,
                    total_on_hand = ?,
                    total_expected = ?,
                    total_ordered = ?,
                    total_allocated = ?,
                    total_available = ?,
                    created_at = ?,
                    updated_at = ?
                WHERE id = ?
            """

            # Prepare the data to be updated
            data = (
                inventory['item_id'],
                inventory['description'],
                inventory['item_reference'],
                json.dumps(inventory['locations']),  # Convert locations list to JSON string
                inventory['total_on_hand'],
                inventory['total_expected'],
                inventory['total_ordered'],
                inventory['total_allocated'],
                inventory['total_available'],
                inventory['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                inventory_id
            )

            # Execute the update query
            cursor.execute(update_query, data)

            # Commit the changes to the database
            conn.commit()
            print("Inventory item updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove(self, inventory_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM inventories WHERE id = {inventory_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, inv):
        """
        Converts the inventory tuple fetched from the database into a dictionary
        with the structure of the given JSON. Handles 'locations' properly.
        """
        locations_str = inv[4]  # The 'locations' field from the database
        
        # Check if locations contain square brackets and strip them out
        if locations_str:
            # Remove square brackets if they exist and then split by commas
            locations_str = locations_str.strip('[]')  # Strip any square brackets
            locations = [int(loc) for loc in locations_str.split(',')] if locations_str else []
        else:
            locations = []

        return {
            'id': inv[0],
            'item_id': inv[1],
            'description': inv[2],
            'item_reference': inv[3],
            'locations': locations,  # The corrected list of locations
            'total_on_hand': inv[5],
            'total_expected': inv[6],
            'total_ordered': inv[7],
            'total_allocated': inv[8],
            'total_available': inv[9],
            'created_at': inv[10],
            'updated_at': inv[11]
        }