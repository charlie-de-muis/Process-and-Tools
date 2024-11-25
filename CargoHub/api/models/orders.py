import sqlite3

from models.base import Base
from providers import data_provider
from models.Database_file import db_start

ORDERS = []


class Orders(Base):
    def __init__(self):
        self.dbfile = "Cargohub_db"
        self.db = db_start()

    def get_orders(self):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM orders LIMIT 10"
        cursor.execute(query)
        orders = cursor.fetchall()  # Fetch a single row
        
        if orders is None:
            print("No orders found")
            return None

        cursor.close()
        conn.close()
        return orders

    def get_order(self, order_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = "SELECT * FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()  # Fetch a single row
        
        if order is None:
            print(f"No order with id {order_id}")
            return None

        cursor.close()
        conn.close()
        return order

    def get_items_in_order(self, order_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get the order by id
            query = "SELECT items FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))

            order = cursor.fetchone()  # Fetch the single order

            if order is None:
                print(f"No order found with id {order_id}")
                return None

            return order[0]  # Return the 'items' field (assuming it is a JSON array or similar)

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_orders_in_shipment(self, shipment_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get all orders that belong to the given shipment_id
            query = "SELECT id FROM orders WHERE shipment_id = %s"
            cursor.execute(query, (shipment_id,))

            orders = cursor.fetchall()  # Fetch all orders for the shipment

            if not orders:
                print(f"No orders found for shipment_id {shipment_id}")
                return []

            return [order[0] for order in orders]  # Return a list of order ids

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_orders_for_client(self, client_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Query to get all orders where the client_id matches either 'ship_to' or 'bill_to'
            query = """
                SELECT * FROM orders WHERE ship_to = %s OR bill_to = %s
            """
            cursor.execute(query, (client_id, client_id))

            orders = cursor.fetchall()  # Fetch all matching orders

            if not orders:
                print(f"No orders found for client_id {client_id}")
                return []

            return orders  # Return the list of orders

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def add_order(self, order):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None
        cursor = conn.cursor()

        # Set timestamps for creation and update
        order["created_at"] = self.get_timestamp()
        order["updated_at"] = self.get_timestamp()
        
        # Define the INSERT query for orders table
        order_query = """
            INSERT INTO orders (
                id, source_id, order_date, request_date, reference, reference_extra, 
                order_status, notes, shipping_notes, picking_notes, warehouse_id, 
                ship_to, bill_to, shipment_id, total_amount, total_discount, 
                total_tax, total_surcharge, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Map data to the order_query
        order_data = (
            order['id'],
            order['source_id'],
            order['order_date'],
            order['request_date'],
            order['reference'],
            order['reference_extra'],
            order['order_status'],
            order['notes'],
            order['shipping_notes'],
            order['picking_notes'],
            order['warehouse_id'],
            order['ship_to'],
            order['bill_to'],
            order['shipment_id'],
            order['total_amount'],
            order['total_discount'],
            order['total_tax'],
            order['total_surcharge'],
            order['created_at'],
            order['updated_at']
        )

        # Execute the INSERT query for the order
        cursor.execute(order_query, order_data)

        # Insert order items in the `order_items` table
        for item in order['items']:
            item_query = """
                INSERT INTO order_items (order_id, item_id, amount) VALUES (%s, %s, %s);
            """
            cursor.execute(item_query, (order['id'], item['item_id'], item['amount']))

        conn.commit()
        print(f"Order {order['reference']} added successfully.")

        cursor.close()
        conn.close()

    def update_order(self, order_id, order):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None

        try:
            cursor = conn.cursor()

            # Check if the order exists
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order_old = cursor.fetchone()
            if order_old is None:
                print("Order not found")
                return None

            # Define the update query for the orders table
            update_order_query = """
                UPDATE orders SET
                    source_id = %s,
                    order_date = %s,
                    request_date = %s,
                    reference = %s,
                    reference_extra = %s,
                    order_status = %s,
                    notes = %s,
                    shipping_notes = %s,
                    picking_notes = %s,
                    warehouse_id = %s,
                    ship_to = %s,
                    bill_to = %s,
                    shipment_id = %s,
                    total_amount = %s,
                    total_discount = %s,
                    total_tax = %s,
                    total_surcharge = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s;
            """

            # Map data to the update_order_query
            update_data = (
                order['source_id'],
                order['order_date'],
                order['request_date'],
                order['reference'],
                order['reference_extra'],
                order['order_status'],
                order['notes'],
                order['shipping_notes'],
                order['picking_notes'],
                order['warehouse_id'],
                order['ship_to'],
                order['bill_to'],
                order['shipment_id'],
                order['total_amount'],
                order['total_discount'],
                order['total_tax'],
                order['total_surcharge'],
                order['created_at'],
                self.get_timestamp(),  # Current timestamp for `updated_at`
                order_id
            )

            # Execute the update query
            cursor.execute(update_order_query, update_data)

            # Delete existing items for this order
            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))

            # Re-insert order items in the `order_items` table
            for item in order['items']:
                item_query = """
                    INSERT INTO order_items (order_id, item_id, amount) VALUES (%s, %s, %s);
                """
                cursor.execute(item_query, (order_id, item['item_id'], item['amount']))

            conn.commit()
            print(f"Order {order_id} updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def update_items_in_order(self, order_id, items):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Get the current order's items from the database
            query = "SELECT items FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            order = cursor.fetchone()

            if order is None:
                print(f"No order found with id {order_id}")
                return None

            current_items = order[0]  # Assuming items are stored in a JSON-like column

            # Remove items that are no longer in the new order
            for current_item in current_items:
                found = False
                for new_item in items:
                    if current_item["item_id"] == new_item["item_id"]:
                        found = True
                        break
                if not found:
                    # Adjust inventory for removed item
                    inventories = self.get_inventories_for_item(current_item["item_id"])
                    min_ordered = float('inf')
                    min_inventory = None
                    for inventory in inventories:
                        if inventory["total_allocated"] < min_ordered:
                            min_ordered = inventory["total_allocated"]
                            min_inventory = inventory
                    if min_inventory:
                        min_inventory["total_allocated"] -= current_item["amount"]
                        min_inventory["total_expected"] = min_inventory["total_on_hand"] + min_inventory["total_ordered"]
                        self.update_inventory(min_inventory["id"], min_inventory)

            # Add or update items in the order
            for current_item in current_items:
                for new_item in items:
                    if current_item["item_id"] == new_item["item_id"]:
                        # Adjust inventory for updated item
                        inventories = self.get_inventories_for_item(current_item["item_id"])
                        min_ordered = float('inf')
                        min_inventory = None
                        for inventory in inventories:
                            if inventory["total_allocated"] < min_ordered:
                                min_ordered = inventory["total_allocated"]
                                min_inventory = inventory
                        if min_inventory:
                            min_inventory["total_allocated"] += new_item["amount"] - current_item["amount"]
                            min_inventory["total_expected"] = min_inventory["total_on_hand"] + min_inventory["total_ordered"]
                            self.update_inventory(min_inventory["id"], min_inventory)

            # Update the order's items in the database
            update_query = """
                UPDATE orders SET items = %s, updated_at = %s WHERE id = %s
            """
            cursor.execute(update_query, (json.dumps(items), self.get_timestamp(), order_id))

            # Commit changes to the database
            conn.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def update_orders_in_shipment(self, shipment_id, orders):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # Exit if connection fails
        
        try:
            cursor = conn.cursor()

            # Get the current orders in the shipment
            query = "SELECT id FROM orders WHERE shipment_id = %s"
            cursor.execute(query, (shipment_id,))
            packed_orders = cursor.fetchall()

            packed_order_ids = [order[0] for order in packed_orders]

            # Remove orders that are no longer in the new shipment
            for order_id in packed_order_ids:
                if order_id not in orders:
                    # Set shipment_id to -1 and status to "Scheduled"
                    update_query = """
                        UPDATE orders SET shipment_id = %s, order_status = %s WHERE id = %s
                    """
                    cursor.execute(update_query, (-1, "Scheduled", order_id))

            # Add or update orders in the shipment
            for order_id in orders:
                if order_id not in packed_order_ids:
                    # Set shipment_id to the new shipment and status to "Packed"
                    update_query = """
                        UPDATE orders SET shipment_id = %s, order_status = %s WHERE id = %s
                    """
                    cursor.execute(update_query, (shipment_id, "Packed", order_id))

            # Commit changes to the database
            conn.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()  # Rollback if any error occurs
        finally:
            cursor.close()
            conn.close()

    def remove_order(self, order_id):
        conn = self.db.connection(self.dbfile)
        if conn is None:
            print("DB connection failed")
            return None  # If connection fails, return None
        cursor = conn.cursor()

        query = f"DELETE FROM orders WHERE id = {order_id}"
        cursor.execute(query)

        conn.commit
        cursor.close()
        conn.close()
