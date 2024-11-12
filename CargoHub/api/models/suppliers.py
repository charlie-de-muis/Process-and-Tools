# DONE

import psycopg2

from models.base import Base
from models.Database_file import db_start

SUPPLIERS = []

class Suppliers(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_suppliers (self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM suppliers LIMIT 10"
        cursor.execute(query)
        suppliers = cursor.fetchall()  # Fetch a single row
        
        if suppliers is None:
            print("No suppliers found")
            return None

        cursor.close()
        conn.close()
        return suppliers

    def get_supplier(self, supplier_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM suppliers  WHERE id = %s"
        cursor.execute(query, (supplier_id,))
        supplier = cursor.fetchone()  # Fetch a single row
        
        if supplier is None:
            print(f"No supplier with id {supplier_id}")
            return None

        cursor.close()
        conn.close()
        return supplier
        
    def add_supplier(self, supplier):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO suppliers (
            id, code, name, address, zip, city, province, country, 
            contact_name, contact_phone, contact_email, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        data = (
            supplier['code'],
            supplier['name'],
            supplier['address'],
            supplier['address_extra'],
            supplier['city'],
            supplier['zip_code'],
            supplier['province'],
            supplier['country'],
            supplier['contact_name'],
            supplier['phonenumber'],
            supplier['reference'],
            supplier['created_at'],
            supplier['updated_at'])
        
        cursor.execute(query, data)
        conn.commit()

        print(f"Supplier {supplier['name']} added successfully.")

        cursor.close()
        conn.close()

    def update_supplier(self, supplier_id, supplier):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the supplier exists
            cursor.execute("SELECT * FROM suppliers WHERE id = %s", (supplier_id,))
            supplier_old = cursor.fetchone()
            if supplier_old is None:
                print("Supplier not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Suppliers SET
                    code = %s,
                    name = %s,
                    address = %s,
                    address_extra = %s,
                    city = %s
                    zip_code = %s
                    province = %s
                    country = %s
                    contact_name = %s
                    phonenumber = %s
                    reference = %s
                    created_at = %s
                    updated_at = %s
                WHERE id = %s
            """

            # Execute the update query
            cursor.execute(update_query, (
                supplier['code'],
                supplier['name'],
                supplier['address'],
                supplier['address_extra'],
                supplier['city'],
                supplier['zip_code'],
                supplier['province'],
                supplier['country'],
                supplier['contact_name'],
                supplier['phonenumber'],
                supplier['reference'],
                supplier['created_at'],
                supplier['updated_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                supplier_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Supplier updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_supplier (self, supplier_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM suppliers WHERE id = {supplier_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()

