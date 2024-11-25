import sqlite3

from models.base import Base
from models.Database_file import db_start

LOCATIONS = []

# grotendeels klaar
class Locations(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_locations(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM locations LIMIT 10"
        cursor.execute(query)
        locations = cursor.fetchall()  # Fetch a single row
        
        if locations is None:
            print("No locations found")
            return None

        cursor.close()
        conn.close()
        return locations

    def get_location(self, location_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM locations WHERE id = %s"
        cursor.execute(query, (location_id,))
        location = cursor.fetchone()  # Fetch a single row
        
        if location is None:
            print(f"No location with id {location_id}")
            return None

        cursor.close()
        conn.close()
        return location

    def get_locations_in_warehouse(self, warehouse_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get locations where warehouse_id matches the given warehouse_id
            query = "SELECT * FROM locations WHERE warehouse_id = %s"
            cursor.execute(query, (warehouse_id,))
            
            locations = cursor.fetchall()  # Fetch all matching locations

            if not locations:
                print(f"No locations found for warehouse_id {warehouse_id}")
                return []  # Return an empty list if no locations are found

            return locations  # Return the list of locations
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def add_location(self, location):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        # Set timestamps for creation and update
        location["created_at"] = self.get_timestamp()
        location["updated_at"] = self.get_timestamp()
        
        # Define the INSERT query with placeholders
        query = f"""INSERT INTO locations (
            id, warehouse_id, code, name, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s);"""

        # Define the data tuple for location
        data = (
            location['id'], 
            location['warehouse_id'], 
            location['code'], 
            location['name'], 
            location['created_at'], 
            location['updated_at']
        )
        
        # Execute the INSERT query
        cursor.execute(query, data)
        conn.commit()

        print(f"Location {location['name']} added successfully.")

        # Close cursor and connection
        cursor.close()
        conn.close()

    def update_location(self, location_id, location):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the location exists
            cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
            location_old = cursor.fetchone()
            if location_old is None:
                print("Location not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE locations SET
                    warehouse_id = %s,
                    code = %s,
                    name = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s
            """

            # Execute the update query
            cursor.execute(update_query, (
                location['warehouse_id'],
                location['code'],
                location['name'],
                location['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                location_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Location updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_location(self, location_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM clients WHERE id = {location_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()
