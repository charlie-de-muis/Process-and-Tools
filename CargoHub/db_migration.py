import json
import sqlite3
import os

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), "api/data")  # Directory containing the JSON files
DB_FILE = 'Cargohub_db.sqlite'

# Function to determine the default value for a field based on its data type
def get_default_value(field_name):
    if "created_at" in field_name or "updated_at" in field_name:
        return "1970-01-01 00:00:00"  # Default timestamp
    elif field_name in ["id", "zip", "contact_phone"]:
        return 0  # Default numeric value for IDs and numbers
    else:
        return "-"  # Default string value for other fields

# Connect to SQLite database
conn = sqlite3.connect(DB_FILE, timeout=10)
cursor = conn.cursor()

# Function to insert JSON data into SQLite
def insert_json_data(json_file, table_name):
    with open(json_file, "r") as f:
        data = json.load(f)

    # If the data is a single record, convert it to a list
    if isinstance(data, dict):
        data = [data]

    all_records_uploaded = True

    for record in data:
        # Prepare columns, values, and placeholders for insertion
        columns = ", ".join(record.keys())  
        placeholders = ", ".join(["?"] * len(record))

        # Handle lists and dictionaries in the record
        for key, value in record.items():
            if isinstance(value, list) or isinstance(value, dict):
                record[key] = json.dumps(value)  # Convert list or dict to JSON string

        # Replace missing values with default values
        values = [record.get(key, get_default_value(key)) for key in record.keys()]

        # Check if the 'id' already exists in the table, and skip insertion if so
        id_value = record.get("id")
        if id_value is not None:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?", (id_value,))
            existing_record_count = cursor.fetchone()[0]
            if existing_record_count > 0:
                all_records_uploaded = False
                continue  # Skip this record if the ID already exists

        
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            
            cursor.execute(sql, tuple(values))
        except sqlite3.IntegrityError as e:
            all_records_uploaded = False
        except sqlite3.ProgrammingError as e:
            print(f"Programming error inserting into {table_name}: {e}")
            all_records_uploaded = False
        except sqlite3.DataError as e:
            print(f"Data type error inserting into {table_name}: {e}")
            all_records_uploaded = False
        except sqlite3.DatabaseError as e:
            print(f"Database error inserting into {table_name}: {e}")
            all_records_uploaded = False
        except Exception as e:
            print(f"Unexpected error inserting into {table_name}: {e}")
            all_records_uploaded = False

    if all_records_uploaded:
        print(f"Successfully uploaded data from {json_file} to table {table_name}.")
    else:
        print(f"Failed to upload some data from {json_file} to table {table_name}.")

# Loop through all JSON files in the data directory
for file_name in os.listdir(DATA_DIR):
    if file_name.endswith(".json"):
        table_name = os.path.splitext(file_name)[0]  # Use the file name as the table name
        json_file = os.path.join(DATA_DIR, file_name)

        print(f"Processing {json_file} for table {table_name}...")

        try:
            insert_json_data(json_file, table_name)
        except Exception as e:
            print(f"Failed to upload data from {json_file} to table {table_name}. Error: {e}")

# Commit changes and close the database connection
conn.commit()
conn.close()

print("All files processed.")
