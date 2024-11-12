import psycopg2
from psycopg2 import sql

class db_start:
    def create_database(self):
        try:
            # Connect to PostgreSQL as an admin user
            conn = psycopg2.connect(
                database="postgres",  # Connect to the default 'postgres' database for admin actions
                user="postgres", 
                password="admin",
                host="localhost",  
                port=5432  # Default port for PostgreSQL, typically 5432
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Check if the 'Cargohub_db' database already exists
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'Cargohub_db'")
            exists = cursor.fetchone()
            
            if not exists:
                # Create the 'Cargohub_db' database if it doesn't exist
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("Cargohub_db")))
                print("Database Cargohub_db created.")
            else:
                print("Database Cargohub_db already exists.")

            # Close admin connection and cursor
            cursor.close()
            conn.close()

            # Now connect to the 'Cargohub_db' to create tables
            conn = psycopg2.connect(
                database="Cargohub_db",  
                user="postgres",
                password="admin",
                host="localhost",
                port=5432  # Adjust if your PostgreSQL server runs on a different port
            )
            conn.autocommit = True
            cursor = conn.cursor()

            create_table_clients = """
            CREATE TABLE IF NOT EXISTS clients (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            province TEXT NOT NULL,
            country TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            contact_phone TEXT,
            contact_email TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_inventory = """
            CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER NOT NULL,
            item_id TEXT NOT NULL,
            description TEXT NOT NULL,
            item_reference TEXT,
            total_on_hand INTEGER NOT NULL,
            total_expected INTEGER NOT NULL,
            total_ordered INTEGER NOT NULL,
            total_allocated INTEGER NOT NULL,
            total_available INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_items = """
            CREATE TABLE IF NOT EXISTS items (
            uid TEXT PRIMARY KEY,
            code TEXT NOT NULL,
            description TEXT NOT NULL,
            short_description TEXT,
            upc_code TEXT,
            model_number TEXT,
            commodity_code TEXT,
            item_line INTEGER,
            item_group INTEGER,
            item_type INTEGER,
            unit_purchase_quantity INTEGER,
            unit_order_quantity INTEGER,
            pack_order_quantity INTEGER,
            supplier_id INTEGER,
            supplier_code TEXT,
            supplier_part_number TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );"""

            create_table_locations = """
            CREATE TABLE IF NOT EXISTS locations (
            id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_orders = """
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER NOT NULL,
            source_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            request_date TEXT NOT NULL,
            reference TEXT NOT NULL,
            reference_extra TEXT,
            order_status TEXT NOT NULL,
            notes TEXT,
            shipping_notes TEXT,
            picking_notes TEXT,
            warehouse_id INTEGER NOT NULL,
            ship_to TEXT,
            bill_to TEXT,
            shipment_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            total_discount REAL NOT NULL,
            total_tax REAL NOT NULL,
            total_surcharge REAL NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_shipments = """
            CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            source_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            request_date TEXT NOT NULL,
            shipment_date TEXT NOT NULL,
            shipment_type TEXT NOT NULL,
            shipment_status TEXT NOT NULL,
            notes TEXT,
            carrier_code TEXT NOT NULL,
            carrier_description TEXT NOT NULL,
            service_code TEXT NOT NULL,
            payment_type TEXT NOT NULL,
            transfer_mode TEXT NOT NULL,
            total_package_count INTEGER NOT NULL,
            total_package_weight REAL NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_suppliers = """
            CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            address_extra TEXT,
            city TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            province TEXT NOT NULL,
            country TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            phonenumber TEXT NOT NULL,
            reference TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_transfers = """
            CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER NOT NULL,
            reference TEXT NOT NULL,
            transfer_from TEXT,
            transfer_to INTEGER NOT NULL,
            transfer_status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_warehouses = """
            CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER NOT NULL,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            zip TEXT NOT NULL,
            city TEXT NOT NULL,
            province TEXT NOT NULL,
            country TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            contact_phone TEXT NOT NULL,
            contact_email TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_item_groups = """
            CREATE TABLE IF NOT EXISTS item_groups (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """
            
            create_table_item_lines = """
            CREATE TABLE IF NOT EXISTS item_lines (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            create_table_item_types = """
            CREATE TABLE IF NOT EXISTS item_types (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            );
            """

            cursor.execute(create_table_clients)
            cursor.execute(create_table_inventory)
            cursor.execute(create_table_items)
            cursor.execute(create_table_locations)
            cursor.execute(create_table_orders)
            cursor.execute(create_table_shipments)
            cursor.execute(create_table_suppliers)
            cursor.execute(create_table_transfers)
            cursor.execute(create_table_warehouses)
            cursor.execute(create_table_item_groups)
            cursor.execute(create_table_item_lines)
            cursor.execute(create_table_item_types)

            cursor.close()
            conn.close()
            print("the database connection is closed")

        except psycopg2.Error as error: 
            print(error)
            print("Database Cargohub_db not formed.")

    def connection(self, database_name):
        try:
            conn = psycopg2.connect(
                database=database_name,  
                user="postgres",
                password="admin",
                host="localhost",
                port=5432
            )
            conn.autocommit = True
            return conn
        except psycopg2.Error as error:
            print(f"Error connecting to database {database_name}: {error}")
            return None