## DONE

import sqlite3

from api.models.base import Base
from api.models.Database_file import db_start

ITEM_TYPES = []


class Item_Types(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_types LIMIT 10"
        cursor.execute(query)
        item_types = cursor.fetchall()  # Fetch a single row
        
        if item_types is None:
            print("No item_types found")
            return None

        cursor.close()
        conn.close()
        return item_types

    def get(self, item_types_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_types WHERE id = ?"
        cursor.execute(query, (item_types_id,))
        item_type = cursor.fetchone()  # Fetch a single row
        
        if item_types_id is None:
            print(f"No item groups with id {item_types_id}")
            return None

        cursor.close()
        conn.close()
        return self.convert_to_dict(item_type)
        
    def add(self, item_type):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        item_type["created_at"] = self.get_timestamp()
        item_type["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO item_types (
            id, name, address, city, zip_code, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data = (
            item_type['id'], 
            item_type['name'], 
            item_type['address'], 
            item_type['city'], 
            item_type['zip_code'], 
            item_type['province'], 
            item_type['country'], 
            item_type['contact_name'], 
            item_type['contact_phone'], 
            item_type['contact_email'], 
            item_type['created_at'],
            item_type['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Item type {item_type['name']} added successfully.")

        cursor.close()
        conn.close()

    def update(self, item_type_id, item_type):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the item_type exists
            cursor.execute("SELECT * FROM item_types WHERE id = ?", (item_type_id,))
            item_type_old = cursor.fetchone()
            if item_type_old is None:
                print("Item type not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE item_types SET
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
                item_type['name'],
                item_type['address'],
                item_type['city'],
                item_type['zip_code'],
                item_type['province'],
                item_type['country'],
                item_type['contact_name'],
                item_type['contact_phone'],
                item_type['contact_email'],
                item_type['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                item_type_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Item type updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove(self, item_type_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM item_types WHERE id = {item_type_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()

    def convert_to_dict(self, item_type):
        """
        Converts an item_type tuple fetched from the database into a dictionary
        with the structure of the given JSON.
        """
        return {
            'id': item_type[0],  # ID of the item type
            'name': item_type[1],  # Name of the item type
            'description': item_type[2],  # Description of the item type
            'created_at': item_type[3],  # Creation timestamp
            'updated_at': item_type[4]  # Update timestamp
        }
