import psycopg2

from models.base import Base
from models.Database_file import db_start

ITEMS = []

# soort van klaar
class Items(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_items(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM items LIMIT 10"
        cursor.execute(query)
        items = cursor.fetchall()  # Fetch a single row
        
        if items is None:
            print("No items found")
            return None

        cursor.close()
        conn.close()
        return items

    def get_item(self, item_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM items WHERE id = %s"
        cursor.execute(query, (item_id,))
        item = cursor.fetchone()  # Fetch a single row
        
        if item is None:
            print(f"No item with id {item_id}")
            return None

        cursor.close()
        conn.close()
        return item

    def get_items_for_item_line(self, item_line_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get items where item_line matches the given item_line_id
            query = "SELECT * FROM items WHERE item_line = %s"
            cursor.execute(query, (item_line_id,))
            
            items = cursor.fetchall()  # Fetch all matching items

            if not items:
                print(f"No items found for item_line_id {item_line_id}")
                return []  # Return an empty list if no items are found

            return items  # Return the list of items
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_items_for_item_group(self, item_group_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get items where item_group matches the given item_group_id
            query = "SELECT * FROM items WHERE item_group = %s"
            cursor.execute(query, (item_group_id,))
            
            items = cursor.fetchall()  # Fetch all matching items

            if not items:
                print(f"No items found for item_group_id {item_group_id}")
                return []  # Return an empty list if no items are found

            return items  # Return the list of items
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_items_for_item_type(self, item_type_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get items where item_type matches the given item_type_id
            query = "SELECT * FROM items WHERE item_type = %s"
            cursor.execute(query, (item_type_id,))
            
            items = cursor.fetchall()  # Fetch all matching items

            if not items:
                print(f"No items found for item_type_id {item_type_id}")
                return []  # Return an empty list if no items are found

            return items  # Return the list of items
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_items_for_supplier(self, supplier_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get items where supplier_id matches the given supplier_id
            query = "SELECT * FROM items WHERE supplier_id = %s"
            cursor.execute(query, (supplier_id,))
            
            items = cursor.fetchall()  # Fetch all matching items

            if not items:
                print(f"No items found for supplier_id {supplier_id}")
                return []  # Return an empty list if no items are found

            return items  # Return the list of items
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def add_item(self, item):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        # Set timestamps
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()
        
        # Define the INSERT query with placeholders
        query = f"""INSERT INTO items (
            uid, code, description, short_description, upc_code, model_number,
            commodity_code, item_line, item_group, item_type, unit_purchase_quantity,
            unit_order_quantity, pack_order_quantity, supplier_id, supplier_code,
            supplier_part_number, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        # Define the data tuple
        data = (
            item['uid'], 
            item['code'], 
            item['description'], 
            item['short_description'], 
            item['upc_code'], 
            item['model_number'], 
            item['commodity_code'], 
            item['item_line'], 
            item['item_group'], 
            item['item_type'], 
            item['unit_purchase_quantity'], 
            item['unit_order_quantity'], 
            item['pack_order_quantity'], 
            item['supplier_id'], 
            item['supplier_code'], 
            item['supplier_part_number'], 
            item['created_at'], 
            item['updated_at']
        )
        
        # Execute the INSERT query
        cursor.execute(query, data)
        conn.commit()

        print(f"Item {item['uid']} added successfully.")

        # Close cursor and connection
        cursor.close()
        conn.close()

    def update_item(self, item_id, item):
        # Establish connection to the database
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Check if the item exists
            cursor.execute("SELECT * FROM items WHERE uid = %s", (item_id,))
            item_old = cursor.fetchone()
            if item_old is None:
                print("Item not found")
                return None

            # Define the update query with placeholders
            update_query = """
                UPDATE items SET
                    code = %s,
                    description = %s,
                    short_description = %s,
                    upc_code = %s,
                    model_number = %s,
                    commodity_code = %s,
                    item_line = %s,
                    item_group = %s,
                    item_type = %s,
                    unit_purchase_quantity = %s,
                    unit_order_quantity = %s,
                    pack_order_quantity = %s,
                    supplier_id = %s,
                    supplier_code = %s,
                    supplier_part_number = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE uid = %s
            """

            # Execute the update query
            cursor.execute(update_query, (
                item['code'],
                item['description'],
                item['short_description'],
                item['upc_code'],
                item['model_number'],
                item['commodity_code'],
                item['item_line'],
                item['item_group'],
                item['item_type'],
                item['unit_purchase_quantity'],
                item['unit_order_quantity'],
                item['pack_order_quantity'],
                item['supplier_id'],
                item['supplier_code'],
                item['supplier_part_number'],
                item['created_at'],
                self.get_timestamp(),  # Assuming this method returns the current timestamp
                item_id
            ))

            # Commit the changes to the database
            conn.commit()
            print("Item updated successfully.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_item(self, item_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM items WHERE id = {item_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()
