## DONE

import psycopg2

from models.base import Base
from models.Database_file import db_start

ITEM_LINES = []


class Item_Lines(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_item_lines(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_lines LIMIT 10"
        cursor.execute(query)
        item_lines = cursor.fetchall()  # Fetch a single row
        
        if item_lines is None:
            print("No item_lines found")
            return None

        cursor.close()
        conn.close()
        return item_lines

    def get_item_lines(self, item_lines_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM item_lines WHERE id = %s"
        cursor.execute(query, (item_lines_id,))
        item_line = cursor.fetchone()  # Fetch a single row
        
        if item_lines_id is None:
            print(f"No item groups with id {item_lines_id}")
            return None

        cursor.close()
        conn.close()
        return item_line
        
    def add_item_lines(self, item_line):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        item_line["created_at"] = self.get_timestamp()
        item_line["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO item_lines (
            id, name, address, city, zip_code, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        data = (
            item_line['id'], 
            item_line['name'], 
            item_line['address'], 
            item_line['city'], 
            item_line['zip_code'], 
            item_line['province'], 
            item_line['country'], 
            item_line['contact_name'], 
            item_line['contact_phone'], 
            item_line['contact_email'], 
            item_line['created_at'],
            item_line['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Item line {item_line['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_item_lines(self, item_line_id, item_line):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the client exists
            cursor.execute("SELECT * FROM item_lines WHERE id = %s", (item_line_id,))
            item_line_old = cursor.fetchone()
            if item_line_old is None:
                print("Item line not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE item_lines SET
                    name = %s,
                    address = %s,
                    city = %s,
                    zip_code = %s,
                    province = %s,
                    country = %s,
                    contact_name = %s,
                    contact_phone = %s,
                    contact_email = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s
            """

            # Execute the update query
            cursor.execute(update_query, (
                item_line['name'],
                item_line['address'],
                item_line['city'],
                item_line['zip_code'],
                item_line['province'],
                item_line['country'],
                item_line['contact_name'],
                item_line['contact_phone'],
                item_line['contact_email'],
                item_line['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                item_line_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Item line updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_item_lines(self, item_line_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM item_lines WHERE id = {item_line_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()