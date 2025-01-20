# DONE

import sqlite3
import json

from api.models.base import Base
from api.models.Database_file import db_start

class Warehouses(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None
        cursor = conn.cursor()

        query = "SELECT * FROM warehouses LIMIT 10"
        cursor.execute(query)
        warehouses = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert rows into a list of dictionaries
        warehouse_list = []
        for warehouse in warehouses:
            warehouse_list.append(self.convert_to_dict(warehouse))

        return warehouse_list

    def get(self, warehouse_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None
        cursor = conn.cursor()

        query = "SELECT * FROM warehouses WHERE id = ?"
        cursor.execute(query, (warehouse_id,))
        warehouse = cursor.fetchone()

        cursor.close()
        conn.close()

        if warehouse is None:
            return None

        return self.convert_to_dict(warehouse)
        
    def add(self, warehouse):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        warehouse["created_at"] = self.get_timestamp()
        warehouse["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO warehouses (
            id, code, name, address, zip, city, province, country, 
            contact, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        contact = json.dumps(warehouse['contact'])
        data = (
            warehouse['id'],
            warehouse['code'],
            warehouse['name'],
            warehouse['address'],
            warehouse['zip'],
            warehouse['city'],
            warehouse['province'],
            warehouse['country'],
            contact,
            warehouse['created_at'],
            warehouse['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Warehouse {warehouse['name']} added successfully.")

        cursor.close()
        conn.close()

    def update(self, warehouse_id, warehouse):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the warehouse exists
            cursor.execute("SELECT * FROM warehouses WHERE id = ?", (warehouse_id,))
            warehouse_old = cursor.fetchone()
            if warehouse_old is None:
                print("Warehouse not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Warehouses SET
                    code = ?,
                    name = ?,
                    address = ?,
                    zip = ?,
                    city = ?,
                    province = ?,
                    country = ?,
                    contact = ?
                    created_at = ?
                    updated_at = ?
                WHERE id = ?
            """

            # Execute the update query
            cursor.execute(update_query, (
                warehouse['code'],
                warehouse['name'],
                warehouse['address'],
                warehouse['zip'],
                warehouse['city'],
                warehouse['province'],
                warehouse['country'],
                warehouse['contact'],
                warehouse['created_at'],
                warehouse['updated_at'],
                self.get_timestamp(), 
                warehouse_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Warehouse updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove(self, warehouse_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM warehouses WHERE id = {warehouse_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, warehouse_tuple):
        """Converts a warehouse tuple to a dictionary."""
        return {
            'id': warehouse_tuple[0],
            'code': warehouse_tuple[1],
            'name': warehouse_tuple[2],
            'address': warehouse_tuple[3],
            'zip': warehouse_tuple[4],
            'city': warehouse_tuple[5],
            'province': warehouse_tuple[6],
            'country': warehouse_tuple[7],
            'contact': json.loads(warehouse_tuple[8]),
            'created_at': warehouse_tuple[9],
            'updated_at': warehouse_tuple[10],
        }