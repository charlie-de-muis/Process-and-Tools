## Done

import sqlite3

from models.base import Base
from models.Database_file import db_start

ITEM_GROUPS = []


class Item_Groups(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_item_groups(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_groups LIMIT 10"
        cursor.execute(query)
        item_groups = cursor.fetchall()  # Fetch a single row
        
        if item_groups is None:
            print("No item_groups found")
            return None

        cursor.close()
        conn.close()
        return item_groups

    def get_item_groups(self, item_groups_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_groups WHERE id = ?"
        cursor.execute(query, (item_groups_id,))
        item_group = cursor.fetchone()  # Fetch a single row
        
        if item_groups_id is None:
            print(f"No item groups with id {item_groups_id}")
            return None

        cursor.close()
        conn.close()
        return item_group
        
    def add_item_groups(self, item_group):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        item_group["created_at"] = self.get_timestamp()
        item_group["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO item_groups (
            id, name, address, city, zip_code, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data = (
            item_group['id'], 
            item_group['name'], 
            item_group['address'], 
            item_group['city'], 
            item_group['zip_code'], 
            item_group['province'], 
            item_group['country'], 
            item_group['contact_name'], 
            item_group['contact_phone'], 
            item_group['contact_email'], 
            item_group['created_at'],
            item_group['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Item group {item_group['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_item_groups(self, item_group_id, item_group):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the client exists
            cursor.execute("SELECT * FROM item_groups WHERE id = ?", (item_group_id,))
            item_group_old = cursor.fetchone()
            if item_group_old is None:
                print("Item group not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE item_groups SET
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
                item_group['name'],
                item_group['address'],
                item_group['city'],
                item_group['zip_code'],
                item_group['province'],
                item_group['country'],
                item_group['contact_name'],
                item_group['contact_phone'],
                item_group['contact_email'],
                item_group['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                item_group_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Item group updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_item_groups(self, item_group_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM item_groups WHERE id = {item_group_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()