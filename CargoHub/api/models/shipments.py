import sqlite3
import json

from api.models.base import Base
from api.models.Database_file import db_start

SHIPMENTS = []


class Shipments(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db.sqlite"
        self.db = db_start()

    def gets(self):
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

    def get(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM shipments WHERE id = ?"
        cursor.execute(query, (shipment_id,))
        shipment = cursor.fetchone()  # Fetch a single row
        
        if shipment is None:
            print(f"No shipment with id {shipment_id}")
            return None

        cursor.close()
        conn.close()
        return self.convert_to_dict(shipment)

    def get_items_in_shipment(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails

        try:
            cursor = conn.cursor()

            # Query the database for the shipment with the given shipment_id
            query = """
                SELECT items FROM shipments WHERE id = ?
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

    def add(self, shipment):
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
                total_package_weight, created_at, updated_at, items
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        items = json.dumps(shipment['items'])
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
            shipment['updated_at'],
            items
        )

        # Execute the INSERT query for the shipment
        cursor.execute(shipment_query, shipment_data)

        conn.commit()
        print(f"Shipment {shipment['id']} added successfully.")

        cursor.close()
        conn.close()

    def update(self, shipment_id, shipment):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None

        try:
            cursor = conn.cursor()

            # Check if the shipment exists
            cursor.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,))
            shipment_old = cursor.fetchone()
            if shipment_old is None:
                print("Shipment not found")
                return None

            # Define the update query for the shipments table
            update_shipment_query = """
                UPDATE shipments SET
                    order_id = ?,
                    source_id = ?,
                    order_date = ?,
                    request_date = ?,
                    shipment_date = ?,
                    shipment_type = ?,
                    shipment_status = ?,
                    notes = ?,
                    carrier_code = ?,
                    carrier_description = ?,
                    service_code = ?,
                    payment_type = ?,
                    transfer_mode = ?,
                    total_package_count = ?,
                    total_package_weight = ?,
                    created_at = ?,
                    updated_at = ?
                WHERE id = ?;
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
            cursor.execute("DELETE FROM shipment_items WHERE shipment_id = ?", (shipment_id,))

            # Re-insert shipment items in the `shipment_items` table
            for item in shipment['items']:
                item_query = """
                    INSERT INTO shipment_items (shipment_id, item_id, amount) VALUES (?, ?, ?);
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
            shipment = self.get(shipment_id)
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
                    # Update inventory for removed items
                    cursor.execute("SELECT * FROM inventories WHERE item_id = ?", (x["item_id"],))
                    inventories = cursor.fetchall()
                    max_ordered = -1
                    max_inventory = None
                    for z in inventories:
                        if z["total_ordered"] > max_ordered:
                            max_ordered = z["total_ordered"]
                            max_inventory = z
                    if max_inventory:
                        max_inventory["total_ordered"] -= x["amount"]
                        max_inventory["total_expected"] = max_inventory["total_on_hand"] + max_inventory["total_ordered"]
                        cursor.execute("UPDATE inventories SET total_ordered = ?, total_expected = ? WHERE id = ?", 
                                       (max_inventory["total_ordered"], max_inventory["total_expected"], max_inventory["id"]))

            # Process items that are updated or newly added in the shipment
            for y in items:
                found = False
                for x in current_items:
                    if x["item_id"] == y["item_id"]:
                        cursor.execute("SELECT * FROM inventories WHERE item_id = ?", (x["item_id"],))
                        inventories = cursor.fetchall()
                        max_ordered = -1
                        max_inventory = None
                        for z in inventories:
                            if z["total_ordered"] > max_ordered:
                                max_ordered = z["total_ordered"]
                                max_inventory = z
                        if max_inventory:
                            max_inventory["total_ordered"] += y["amount"] - x["amount"]
                            max_inventory["total_expected"] = max_inventory["total_on_hand"] + max_inventory["total_ordered"]
                            cursor.execute("UPDATE inventories SET total_ordered = ?, total_expected = ? WHERE id = ?", 
                                           (max_inventory["total_ordered"], max_inventory["total_expected"], max_inventory["id"]))
                            max_inventory["total_expected"] = max_inventory["total_on_hand"] + max_inventory["total_ordered"]
                    cursor.execute("SELECT * FROM inventories WHERE item_id = ?", (y["item_id"],))
                    inventories = cursor.fetchall()
                    max_ordered = -1
                    max_inventory = None
                    for z in inventories:
                        if z["total_ordered"] > max_ordered:
                            max_ordered = z["total_ordered"]
                            max_inventory = z
                    if max_inventory:
                        max_inventory["total_ordered"] += y["amount"]
                        max_inventory["total_expected"] = max_inventory["total_on_hand"] + max_inventory["total_ordered"]
                        cursor.execute("UPDATE inventories SET total_ordered = ?, total_expected = ? WHERE id = ?", 
                                       (max_inventory["total_ordered"], max_inventory["total_expected"], max_inventory["id"]))
                    if max_inventory:
                        max_inventory["total_ordered"] += y["amount"]
                        max_inventory["total_expected"] = max_inventory["total_on_hand"] + max_inventory["total_ordered"]
                        cursor.execute("UPDATE inventories SET total_ordered = ?, total_expected = ? WHERE id = ?", 
                                       (max_inventory["total_ordered"], max_inventory["total_expected"], max_inventory["id"]))

            # Update the shipment's items field in the database
            update_query = """
                UPDATE shipments SET items = ?, updated_at = ? WHERE id = ?
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

    def remove(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM shipments WHERE id = {shipment_id}"
        cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()

    def convert_to_dict(self, shipment):
        """
        Converts a shipment tuple fetched from the database into a dictionary
        with the structure of the given JSON.
        """
        # Handle the 'items' field as a list (assuming it's stored as a JSON string)
        try:
            items = json.loads(shipment[18]) if shipment[18] else []  # 'items' is stored as a JSON string
        except json.JSONDecodeError:
            items = []  # If decoding fails, set it as an empty list

        return {
            'id': shipment[0],  # Unique identifier for the shipment
            'order_id': shipment[1],  # ID of the associated order
            'source_id': shipment[2],  # Source of the shipment
            'order_date': shipment[3],  # Date of the order
            'request_date': shipment[4],  # Requested shipment date
            'shipment_date': shipment[5],  # Date the shipment was processed
            'shipment_type': shipment[6],  # Type of the shipment (e.g., air, ground)
            'shipment_status': shipment[7],  # Status of the shipment (e.g., pending, shipped)
            'notes': shipment[8],  # Additional notes about the shipment
            'carrier_code': shipment[9],  # Carrier code (e.g., UPS, FedEx)
            'carrier_description': shipment[10],  # Description of the carrier
            'service_code': shipment[11],  # Service code (e.g., next-day, standard)
            'payment_type': shipment[12],  # Payment type for the shipment
            'transfer_mode': shipment[13],  # Transfer mode for the shipment (e.g., air, sea)
            'total_package_count': shipment[14],  # Total number of packages in the shipment
            'total_package_weight': shipment[15],  # Total weight of the shipment
            'created_at': shipment[16],  # Timestamp of when the shipment was created
            'updated_at': shipment[17],  # Timestamp of when the shipment was last updated
            'items': items  # The list of items (parsed from JSON string)
        }
