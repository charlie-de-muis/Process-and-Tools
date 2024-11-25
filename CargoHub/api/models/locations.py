import sqlite3

from api.models.base import Base
from api.models.Database_file import db_start

LOCATIONS = []

# grotendeels klaar
class Locations(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets(self):
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

    def get(self, location_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        try:
            # Use the correct placeholder "?" for SQLite
            query = "SELECT * FROM locations WHERE id = ?"
            cursor.execute(query, (location_id,))  # Pass the client_id as a tuple
            location = cursor.fetchone()  # Fetch a single row
            
            if location is None:
                print(f"No client with id {location_id}")
                return None

            return self.convert_to_dict(location)

        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # def get_locations_in_warehouse(self, warehouse_id):
    #     conn = self.db.connection(self.dbfile)
    #     if conn is None:
    #         print("DB connection failed")
    #         return None  # Exit if connection fails
        
    #     try:
    #         cursor = conn.cursor()

    #         # Query to get locations where warehouse_id matches the given warehouse_id
    #         query = "SELECT * FROM locations WHERE warehouse_id = ?"
    #         cursor.execute(query, (warehouse_id,))
            
    #         locations = cursor.fetchall()  # Fetch all matching locations

    #         if not locations:
    #             print(f"No locations found for warehouse_id {warehouse_id}")
    #             return []  # Return an empty list if no locations are found

    #         return locations  # Return the list of locations
        
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return None
    #     finally:
    #         cursor.close()
    #         conn.close()

    def add(self, location):
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
        ) VALUES (?, ?, ?, ?, ?, ?);"""

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

    def update(self, location_id, location):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the location exists
            cursor.execute("SELECT * FROM locations WHERE id = ?", (location_id,))
            location_old = cursor.fetchone()
            if location_old is None:
                print("Location not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE locations SET
                    warehouse_id = ?,
                    code = ?,
                    name = ?,
                    created_at = ?,
                    updated_at = ?
                WHERE id = ?
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

    def remove(self, location_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM locations WHERE id = ?"
        cursor.execute(query, (location_id,))

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, location):
        """
        Converts a location tuple fetched from the database into a dictionary
        with the structure of the given JSON.
        """
        return {
            'id': location[0],  # Unique identifier for the location
            'warehouse_id': location[1],  # ID of the associated warehouse
            'code': location[2],  # Code of the location
            'name': location[3],  # Name of the location
            'created_at': location[4],  # Timestamp of when the location was created
            'updated_at': location[5],  # Timestamp of when the location was last updated
        }
