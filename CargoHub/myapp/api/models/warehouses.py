# DONE

import psycopg2

from models.base import Base
from models.Database_file import db_start

class Warehouses(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_warehouses (self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM warehouses LIMIT 10"
        cursor.execute(query)
        warehouses = cursor.fetchall()  # Fetch a single row
        
        if warehouses is None:
            print("No warehouses found")
            return None

        cursor.close()
        conn.close()
        return warehouses

    def get_warehouse(self, warehouse_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM warehouses WHERE id = %s"
        cursor.execute(query, (warehouse_id,))
        warehouse = cursor.fetchone()  # Fetch a single row
        
        if warehouse is None:
            print(f"No warehouse with id {warehouse_id}")
            return None

        cursor.close()
        conn.close()
        return warehouse
        
    def add_warehouse(self, warehouse):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        warehouse["created_at"] = self.get_timestamp()
        warehouse["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO warehouses (
            id, code, name, address, zip, city, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        data = (
            warehouse['code'],
            warehouse['name'],
            warehouse['address'],
            warehouse['zip'],
            warehouse['city'],
            warehouse['province'],
            warehouse['country'],
            warehouse['contact_name'],
            warehouse['contact_phone'],
            warehouse['contact_email'],
            warehouse['created_at'],
            warehouse['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Warehouse {warehouse['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_warehouse(self, warehouse_id, warehouse):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the warehouse exists
            cursor.execute("SELECT * FROM warehouses WHERE id = %s", (warehouse_id,))
            warehouse_old = cursor.fetchone()
            if warehouse_old is None:
                print("Warehouse not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Warehouses SET
                    code = %s,
                    name = %s,
                    address = %s,
                    zip = %s,
                    city = %s,
                    province = %s,
                    country = %s,
                    contact_name = %s,
                    contact_phone = %s,
                    contact_email = %s
                    created_at = %s
                    updated_at = %s
                WHERE id = %s
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
                warehouse['contact_name'],
                warehouse['contact_phone'],
                warehouse['contact_email'],
                warehouse['created_at'],
                warehouse['updated_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
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

    def remove_warehouse (self, warehouse_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM warehouses WHERE id = {warehouse_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()
