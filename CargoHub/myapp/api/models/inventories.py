import psycopg2

from models.base import Base
from models.Database_file import db_start

INVENTORIES = []
# soort van klaar

class Inventories(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_inventories(self):
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

    def get_inventory(self, inventory_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM inventories WHERE id = %s"
        cursor.execute(query, (inventory_id,))
        inventories = cursor.fetchone()  # Fetch a single row
        
        if inventories is None:
            print(f"No inventory with id {inventory_id}")
            return None

        cursor.close()
        conn.close()
        return inventories

    def get_inventories_for_item(self, item_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Parameterized query to prevent SQL injection
            query = "SELECT * FROM inventories WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            
            inventories = cursor.fetchall()  # Fetch all records matching the item_id

            if not inventories:
                print(f"No inventories found for item ID {item_id}")
                return []  # Return empty list if no records are found

            return inventories  # Return the list of inventory records
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_inventory_totals_for_item(self, item_id):
        result = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0
        }

        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Parameterized query to get totals for each column
            query = """
                SELECT total_expected, total_ordered, total_allocated, total_available
                FROM inventories
                WHERE item_id = %s
            """
            cursor.execute(query, (item_id,))
            
            inventories = cursor.fetchall()  # Fetch all inventory records

            if not inventories:
                print(f"No inventories found for item ID {item_id}")
                return result  # Return default result if no records found

            # Summing up the totals for the given item_id
            for inventory in inventories:
                result["total_expected"] += inventory[0]
                result["total_ordered"] += inventory[1]
                result["total_allocated"] += inventory[2]
                result["total_available"] += inventory[3]

            return result  # Return the calculated totals
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def add_inventory(self, inventory):
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
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        # Preparing the data tuple, including serializing locations as a JSON string
        data = (
            inventory['id'],
            inventory['item_id'],
            inventory['description'],
            inventory['item_reference'],
            json.dumps(inventory['locations']),  # Store locations as JSON array
            inventory['total_on_hand'],
            inventory['total_expected'],
            inventory['total_ordered'],
            inventory['total_allocated'],
            inventory['total_available'],
            inventory['created_at'],
            inventory['updated_at']
        )
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Inventory item {inventory['item_id']} added successfully.")

        cursor.close()
        conn.close()

    def update_inventory(self, inventory_id, inventory):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the inventory item exists
            cursor.execute("SELECT * FROM inventories WHERE id = %s", (inventory_id,))
            inventory_old = cursor.fetchone()
            if inventory_old is None:
                print("Inventory item not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE inventories SET
                    item_id = %s,
                    description = %s,
                    item_reference = %s,
                    locations = %s,
                    total_on_hand = %s,
                    total_expected = %s,
                    total_ordered = %s,
                    total_allocated = %s,
                    total_available = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s
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

    def remove_inventory(self, inventory_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM inventories WHERE id = {inventory_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()
