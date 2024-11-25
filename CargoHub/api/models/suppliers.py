# DONE

import sqlite3

from api.models.base import Base
from api.models.Database_file import db_start

SUPPLIERS = []

class Suppliers(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets (self):
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

    def get(self, supplier_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM suppliers  WHERE id = ?"
        cursor.execute(query, (supplier_id,))
        supplier = cursor.fetchone()  # Fetch a single row
        
        if supplier is None:
            print(f"No supplier with id {supplier_id}")
            return None

        cursor.close()
        conn.close()
        return self.convert_to_dict(supplier)
        
    def add(self, supplier):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()
        
        query = f"""INSERT INTO suppliers (
            id, code, name, address, address_extra, city, zip_code, province, country, 
            contact_name, phonenumber, reference, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data = (
            supplier['id'],
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

    def update(self, supplier_id, supplier):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the supplier exists
            cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
            supplier_old = cursor.fetchone()
            if supplier_old is None:
                print("Supplier not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE Suppliers SET
                    code = ?,
                    name = ?,
                    address = ?,
                    address_extra = ?,
                    city = ?
                    zip_code = ?
                    province = ?
                    country = ?
                    contact_name = ?
                    phonenumber = ?
                    reference = ?
                    created_at = ?
                    updated_at = ?
                WHERE id = ?
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

    def remove(self, supplier_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM suppliers WHERE id = {supplier_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, supplier):
        """
        Converts a supplier tuple fetched from the database into a dictionary
        with the structure of the given JSON.
        """
        return {
            'id': supplier[0],  # Unique identifier for the supplier
            'code': supplier[1],  # Supplier code
            'name': supplier[2],  # Supplier name
            'address': supplier[3],  # Address of the supplier
            'address_extra': supplier[4],  # Extra address information (optional)
            'city': supplier[5],  # City of the supplier
            'zip_code': supplier[6],  # Zip code of the supplier
            'province': supplier[7],  # Province of the supplier
            'country': supplier[8],  # Country of the supplier
            'contact_name': supplier[9],  # Contact person name
            'phonenumber': supplier[10],  # Contact phone number
            'reference': supplier[11],  # Reference of the supplier
            'created_at': supplier[12],  # Timestamp of when the supplier was created
            'updated_at': supplier[13],  # Timestamp of when the supplier was last updated
        }
