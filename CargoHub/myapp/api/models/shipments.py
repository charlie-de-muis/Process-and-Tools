import psycopg2

from models.base import Base
from providers import data_provider
from models.Database_file import db_start

SHIPMENTS = []


class Shipments(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_shipments(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM shipments LIMIT 10"
        cursor.execute(query)
        shipments = cursor.fetchall()  # Fetch a single row
        
        if shipments is None:
            print("No shipments found")
            return None

        cursor.close()
        conn.close()
        return shipments

    def get_shipment(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM shipments WHERE id = %s"
        cursor.execute(query, (shipment_id,))
        shipment = cursor.fetchone()  # Fetch a single row
        
        if shipment is None:
            print(f"No shipment with id {shipment_id}")
            return None

        cursor.close()
        conn.close()
        return shipment

    def get_items_in_shipment(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails

        try:
            cursor = conn.cursor()

            # Query the database for the shipment with the given shipment_id
            query = """
                SELECT items FROM shipments WHERE id = %s
            """
            cursor.execute(query, (shipment_id,))
            shipment = cursor.fetchone()

            if shipment is None:
                print(f"No shipment found with id {shipment_id}")
                return None

            # Assuming items are stored as a JSON column
            return shipment[0]  # Return the items from the shipment

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    def add_shipment(self, shipment):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None
        cursor = conn.cursor()

        # Set timestamps for creation and update
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()
        
        # Define the INSERT query for shipments table
        shipment_query = """
            INSERT INTO shipments (
                id, order_id, source_id, order_date, request_date, shipment_date,
                shipment_type, shipment_status, notes, carrier_code, carrier_description, 
                service_code, payment_type, transfer_mode, total_package_count, 
                total_package_weight, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Map data to the shipment_query
        shipment_data = (
            shipment['id'],
            shipment['order_id'],
            shipment['source_id'],
            shipment['order_date'],
            shipment['request_date'],
            shipment['shipment_date'],
            shipment['shipment_type'],
            shipment['shipment_status'],
            shipment['notes'],
            shipment['carrier_code'],
            shipment['carrier_description'],
            shipment['service_code'],
            shipment['payment_type'],
            shipment['transfer_mode'],
            shipment['total_package_count'],
            shipment['total_package_weight'],
            shipment['created_at'],
            shipment['updated_at']
        )

        # Execute the INSERT query for the shipment
        cursor.execute(shipment_query, shipment_data)

        # Insert shipment items in the `shipment_items` table
        for item in shipment['items']:
            item_query = """
                INSERT INTO shipment_items (shipment_id, item_id, amount) VALUES (%s, %s, %s);
            """
            cursor.execute(item_query, (shipment['id'], item['item_id'], item['amount']))

        conn.commit()
        print(f"Shipment {shipment['id']} added successfully.")

        cursor.close()
        conn.close()

    def update_shipment(self, shipment_id, shipment):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None

        try:
            cursor = conn.cursor()

            # Check if the shipment exists
            cursor.execute("SELECT * FROM shipments WHERE id = %s", (shipment_id,))
            shipment_old = cursor.fetchone()
            if shipment_old is None:
                print("Shipment not found")
                return None

            # Define the update query for the shipments table
            update_shipment_query = """
                UPDATE shipments SET
                    order_id = %s,
                    source_id = %s,
                    order_date = %s,
                    request_date = %s,
                    shipment_date = %s,
                    shipment_type = %s,
                    shipment_status = %s,
                    notes = %s,
                    carrier_code = %s,
                    carrier_description = %s,
                    service_code = %s,
                    payment_type = %s,
                    transfer_mode = %s,
                    total_package_count = %s,
                    total_package_weight = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s;
            """

            # Map data to the update_shipment_query
            update_data = (
                shipment['order_id'],
                shipment['source_id'],
                shipment['order_date'],
                shipment['request_date'],
                shipment['shipment_date'],
                shipment['shipment_type'],
                shipment['shipment_status'],
                shipment['notes'],
                shipment['carrier_code'],
                shipment['carrier_description'],
                shipment['service_code'],
                shipment['payment_type'],
                shipment['transfer_mode'],
                shipment['total_package_count'],
                shipment['total_package_weight'],
                shipment['created_at'],
                self.get_timestamp(),  # Current timestamp for `updated_at`
                shipment_id
            )

            # Execute the update query
            cursor.execute(update_shipment_query, update_data)

            # Delete existing items for this shipment
            cursor.execute("DELETE FROM shipment_items WHERE shipment_id = %s", (shipment_id,))

            # Re-insert shipment items in the `shipment_items` table
            for item in shipment['items']:
                item_query = """
                    INSERT INTO shipment_items (shipment_id, item_id, amount) VALUES (%s, %s, %s);
                """
                cursor.execute(item_query, (shipment_id, item['item_id'], item['amount']))

            conn.commit()
            print(f"Shipment {shipment_id} updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def update_items_in_shipment(self, shipment_id, items):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails

        try:
            cursor = conn.cursor()

            # Fetch the current shipment from the database
            shipment = self.get_shipment(shipment_id)
            if shipment is None:
                print(f"Shipment with id {shipment_id} not found")
                return None

            current_items = shipment["items"]

            # Process items that are no longer in the shipment
            for x in current_items:
                found = False
                for y in items:
                    if x["item_id"] == y["item_id"]:
                        found = True
                        break
                if not found:
                    inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(x["item_id"])
                    max_ordered = -1
                    max_inventory = None
                    for z in inventories:
                        if z["total_ordered"] > max_ordered:
                            max_ordered = z["total_ordered"]
                            max_inventory = z
                    if max_inventory:
                        max_inventory["total_ordered"] -= x["amount"]
                        max_inventory["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                        data_provider.fetch_inventory_pool().update_inventory(max_inventory["id"], max_inventory)

            # Process items that are updated or newly added in the shipment
            for x in current_items:
                for y in items:
                    if x["item_id"] == y["item_id"]:
                        inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(x["item_id"])
                        max_ordered = -1
                        max_inventory = None
                        for z in inventories:
                            if z["total_ordered"] > max_ordered:
                                max_ordered = z["total_ordered"]
                                max_inventory = z
                        if max_inventory:
                            max_inventory["total_ordered"] += y["amount"] - x["amount"]
                            max_inventory["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                            data_provider.fetch_inventory_pool().update_inventory(max_inventory["id"], max_inventory)

            # Update the shipment's items field in the database
            update_query = """
                UPDATE shipments SET items = %s, updated_at = %s WHERE id = %s
            """
            cursor.execute(update_query, (json.dumps(items), self.get_timestamp(), shipment_id))
            conn.commit()
            
            print(f"Shipment {shipment_id} updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs

        finally:
            cursor.close()
            conn.close()

    def remove_shipment(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM shipments WHERE id = {shipment_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()