import pytest
from django.urls import reverse
from rest_framework import status

# HI I DID IT?????
@pytest.mark.django_db
def test_api_app_status(client):
    # URL for the api_app endpoint (you can replace this with the correct URL pattern if needed)
    url = '/api_app/'  # Adjust this to the actual endpoint if needed
#     # Send a GET request to the URL
    response = client.get(url)
#     # Assert that the status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

# # TODO: replace with test server url
# BASE_URL = "http://145.24.223.64:80/api/v1"

# # Test auth with missing API key
# def test_auth_get_clients():
#     response = requests.get(f"{BASE_URL}/clients/")
#     assert response.status_code == 401

# # Test creating a new client
# def test_data_post_client():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     client = {
#         "id": 10000,
#         "name": "Raymond Inc",
#         "address": "1296 Daniel Road Apt. 349",
#         "city": "Pierceview",
#         "zip_code": "28301",
#         "province": "Colorado",
#         "country": "United States",
#         "contact_name": "Bryan Clark",
#         "contact_phone": "242.732.3483x2573",
#         "contact_email": "robertcharles@example.net",
#     }
#     response = requests.post(f"{BASE_URL}/clients/", headers=header, json=client)
#     assert response.status_code == 201

# # Test retrieving the client
# def test_data_get_client():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/clients/10000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary

# # Test updating the client
# def test_data_update_clients():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"name": "Updated Client Name"}
#     response = requests.put(f"{BASE_URL}/clients/10000/", headers=header, json=data)
#     assert response.status_code == 200

# # Test deleting the client
# def test_data_delete_clients():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.delete(f"{BASE_URL}/clients/10000/", headers=header)
#     assert response.status_code == 204

# # Test confirming client deletion
# def test_data_check_deleted_client():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/clients/10000/", headers=header)
#     assert response.status_code == 404  # Expect Not Found





# # IT-auth-get-inventories - checken of API key goed werkt
# def test_auth_get_inventories():
#     response = requests.get(f"{BASE_URL}/inventories/")
#     assert response.status_code == 401
# # IT-data-post-inventories - checken of uploaden goed gaat
# def test_data_post_inventories():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     inventory = {
#         "id": 20000,
#         "item_id": "P000001",
#         "description": "Face-to-face clear-thinking complexity",
#         "item_reference": "sjQ23408K",
#         "locations": [
#             3211,
#             24700,
#             14123,
#             19538,
#             31071,
#             24701,
#             11606,
#             11817
#         ],
#         "total_on_hand": 262,
#         "total_expected": 0,
#         "total_ordered": 80,
#         "total_allocated": 41,
#         "total_available": 141,
#         "created_at": "2015-02-19 16:08:24",
#         "updated_at": "2015-09-26 06:37:56"
#     }
#     response = requests.post(f"{BASE_URL}/inventories/", headers=header, json=inventory)
#     assert response.status_code == 201
# # IT-data-get-inventories - checken of je de verwachte data terug krijgt
# def test_data_get_inventories():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/inventories/20000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary

# # IT-data-update-inventories
# def test_data_update_inventories():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"item": "Updated Item Name"}

#     response = requests.put(f"{BASE_URL}/inventories/20000/", headers=header, json=data)
#     assert response.status_code == 200
#     # IT-data-delete-inventories
# # IT-data-delete-inventories
# def test_data_delete_inventories():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/inventories/20000/", headers=header)
#     assert response.status_code == 204
# # check if inventory is not found
# def test_data_check_deleted_inv():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/inventories/20000/", headers=header)
#     assert response.status_code == 404




# # IT-auth-get-items - checken of API key goed werkt
# def test_auth_get_items():
#     response = requests.get(f"{BASE_URL}/items/")
#     assert response.status_code == 401
# # IT-data-post-items - checken of uploaden goed gaat
# def test_data_post_items():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     items = {
#         "uid": "P500000",
#         "code": "sjQ23408K",
#         "description": "Face-to-face clear-thinking complexity",
#         "short_description": "must",
#         "upc_code": "6523540947122",
#         "model_number": "63-OFFTq0T",
#         "commodity_code": "oTo304",
#         "item_line": 11,
#         "item_group": 73,
#         "item_type": 14,
#         "unit_purchase_quantity": 47,
#         "unit_order_quantity": 13,
#         "pack_order_quantity": 11,
#         "supplier_id": 34,
#         "supplier_code": "SUP423",
#         "supplier_part_number": "E-86805-uTM",
#         "created_at": "2015-02-19 16:08:24",
#         "updated_at": "2015-09-26 06:37:56"
#     }
#     response = requests.post(f"{BASE_URL}/items/", headers=header, json=items)
#     assert response.status_code == 201
# # IT-data-get-items - checken of je de verwachte data terug krijgt
# def test_data_get_items():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/items/P500000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-items
# def test_data_update_items():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"description": "Updated Item Description"}

#     response = requests.put(f"{BASE_URL}/items/P500000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-items
# def test_data_delete_items():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/items/P500000/", headers=header)
#     assert response.status_code == 204
# # check if item is not found
# def test_data_check_delete_item():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/items/P500000/", headers=header)
#     assert response.status_code == 404




# # IT-auth-get-locations - checken of API key goed werkt
# def test_auth_get_locations():
#     response = requests.get(f"{BASE_URL}/locations/")
#     assert response.status_code == 401
# # IT-data-post-locations - checken of uploaden goed gaat
# def test_data_post_locations():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     locations = {
#         "id": 1000000,
#         "warehouse_id": 1,
#         "code": "A.1.0",
#         "name": "Row: A, Rack: 1, Shelf: 0",
#         "created_at": "1992-05-15 03:21:32",
#         "updated_at": "1992-05-15 03:21:32"
#     }
#     response = requests.post(f"{BASE_URL}/locations/", headers=header, json=locations)
#     assert response.status_code == 201
# # IT-data-get-locations - checken of je de verwachte data terug krijgt
# def test_data_get_locations():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/locations/1000000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-locations
# def test_data_update_locations():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"address": "Updated Location Address"}

#     response = requests.put(f"{BASE_URL}/locations/1000000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-locations
# def test_data_delete_locations():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/locations/1000000/", headers=header)
#     assert response.status_code == 204
# # check if location is not found
# def test_data_check_delete_location():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/locations/1000000/", headers=header)
#     assert response.status_code == 404




# # IT-auth-get-orders - checken of API key goed werkt
# def test_auth_get_orders():
#     response = requests.get(f"{BASE_URL}/orders/")
#     assert response.status_code == 401
# # IT-data-post-orders - checken of uploaden goed gaat
# def test_data_post_orders():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     orders = {
#         "id": 100000,
#         "source_id": 33,
#         "order_date": "2019-04-03T11:33:15Z",
#         "request_date": "2019-04-07T11:33:15Z",
#         "reference": "ORD00001",
#         "reference_extra": "Bedreven arm straffen bureau.",
#         "order_status": "Delivered",
#         "notes": "Voedsel vijf vork heel.",
#         "shipping_notes": "Buurman betalen plaats bewolkt.",
#         "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
#         "warehouse_id": 18,
#         "ship_to": "",
#         "bill_to": "",
#         "shipment_id": 1,
#         "total_amount": 9905.13,
#         "total_discount": 150.77,
#         "total_tax": 372.72,
#         "total_surcharge": 77.6,
#         "created_at": "2019-04-03T11:33:15Z",
#         "updated_at": "2019-04-05T07:33:15Z",
#         "items": [
#             {
#                 "item_id": "P007435",
#                 "amount": 23
#             },
#             {
#                 "item_id": "P009557",
#                 "amount": 1
#             },
#             {
#                 "item_id": "P009553",
#                 "amount": 50
#             },
#             {
#                 "item_id": "P010015",
#                 "amount": 16
#             },
#             {
#                 "item_id": "P002084",
#                 "amount": 33
#             },
#             {
#                 "item_id": "P009663",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P010125",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P005768",
#                 "amount": 26
#             },
#             {
#                 "item_id": "P004051",
#                 "amount": 1
#             },
#             {
#                 "item_id": "P005026",
#                 "amount": 29
#             },
#             {
#                 "item_id": "P000726",
#                 "amount": 22
#             },
#             {
#                 "item_id": "P008107",
#                 "amount": 47
#             },
#             {
#                 "item_id": "P001598",
#                 "amount": 32
#             },
#             {
#                 "item_id": "P002855",
#                 "amount": 20
#             },
#             {
#                 "item_id": "P010404",
#                 "amount": 30
#             },
#             {
#                 "item_id": "P010446",
#                 "amount": 6
#             },
#             {
#                 "item_id": "P001517",
#                 "amount": 9
#             },
#             {
#                 "item_id": "P009265",
#                 "amount": 2
#             },
#             {
#                 "item_id": "P001108",
#                 "amount": 20
#             },
#             {
#                 "item_id": "P009110",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P009686",
#                 "amount": 13
#             }
#         ]
#     }
#     response = requests.post(f"{BASE_URL}/orders/", headers=header, json=orders)
#     assert response.status_code == 201
# # IT-data-get-orders - checken of je de verwachte data terug krijgt
# def test_data_get_orders():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/orders/100000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-orders
# def test_data_update_orders():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"status": "Updated Order Status"}

#     response = requests.put(f"{BASE_URL}/orders/100000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-orders
# def test_data_delete_orders():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/orders/100000/", headers=header)
#     assert response.status_code == 204
# # check if order is not found
# def test_data_check_delete_orders():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/orders/100000/", headers=header)
#     assert response.status_code == 404




# # IT-auth-get-shipments - checken of API key goed werkt
# def test_auth_get_shipments():
#     response = requests.get(f"{BASE_URL}/shipments/")
#     assert response.status_code == 401
# # IT-data-post-shipments - checken of uploaden goed gaat
# def test_data_post_shipments():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     shipments = {
#         "id": 100000,
#         "order_id": 1,
#         "source_id": 33,
#         "order_date": "2000-03-09",
#         "request_date": "2000-03-11",
#         "shipment_date": "2000-03-13",
#         "shipment_type": "I",
#         "shipment_status": "Pending",
#         "notes": "Zee vertrouwen klas rots heet lachen oneven begrijpen.",
#         "carrier_code": "DPD",
#         "carrier_description": "Dynamic Parcel Distribution",
#         "service_code": "Fastest",
#         "payment_type": "Manual",
#         "transfer_mode": "Ground",
#         "total_package_count": 31,
#         "total_package_weight": 594.42,
#         "created_at": "2000-03-10T11:11:14Z",
#         "updated_at": "2000-03-11T13:11:14Z",
#         "items": [
#             {
#                 "item_id": "P007435",
#                 "amount": 23
#             },
#             {
#                 "item_id": "P009557",
#                 "amount": 1
#             },
#             {
#                 "item_id": "P009553",
#                 "amount": 50
#             },
#             {
#                 "item_id": "P010015",
#                 "amount": 16
#             },
#             {
#                 "item_id": "P002084",
#                 "amount": 33
#             },
#             {
#                 "item_id": "P009663",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P010125",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P005768",
#                 "amount": 26
#             },
#             {
#                 "item_id": "P004051",
#                 "amount": 1
#             },
#             {
#                 "item_id": "P005026",
#                 "amount": 29
#             },
#             {
#                 "item_id": "P000726",
#                 "amount": 22
#             },
#             {
#                 "item_id": "P008107",
#                 "amount": 47
#             },
#             {
#                 "item_id": "P001598",
#                 "amount": 32
#             },
#             {
#                 "item_id": "P002855",
#                 "amount": 20
#             },
#             {
#                 "item_id": "P010404",
#                 "amount": 30
#             },
#             {
#                 "item_id": "P010446",
#                 "amount": 6
#             },
#             {
#                 "item_id": "P001517",
#                 "amount": 9
#             },
#             {
#                 "item_id": "P009265",
#                 "amount": 2
#             },
#             {
#                 "item_id": "P001108",
#                 "amount": 20
#             },
#             {
#                 "item_id": "P009110",
#                 "amount": 18
#             },
#             {
#                 "item_id": "P009686",
#                 "amount": 13
#             }
#         ]
#     }
#     response = requests.post(f"{BASE_URL}/shipments/", headers=header, json=shipments)
#     assert response.status_code == 201
# # IT-data-get-shipments - checken of je de verwachte data terug krijgt
# def test_data_get_shipments():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/shipments/100000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-shipments
# def test_data_update_shipments():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"tracking_number": "Updated Tracking Number"}

#     response = requests.put(f"{BASE_URL}/shipments/100000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-shipments
# def test_data_delete_shipments():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/shipments/100000/", headers=header)
#     assert response.status_code == 204
# # check if shipment is not found
# def test_data_check_delete_shipment():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/shipments/100000/", headers=header)
#     assert response.status_code == 404


# # IT-auth-get-suppliers - checken of API key goed werkt
# def test_auth_get_suppliers():
#     response = requests.get(f"{BASE_URL}/suppliers/")
#     assert response.status_code == 401
# # IT-data-post-suppliers - checken of uploaden goed gaat
# def test_data_post_suppliers():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     suppliers = {
#         "id": 100000,
#         "code": "SUP0001",
#         "name": "Lee, Parks and Johnson",
#         "address": "5989 Sullivan Drives",
#         "address_extra": "Apt. 996",
#         "city": "Port Anitaburgh",
#         "zip_code": "91688",
#         "province": "Illinois",
#         "country": "Czech Republic",
#         "contact_name": "Toni Barnett",
#         "phonenumber": "363.541.7282x36825",
#         "reference": "LPaJ-SUP0001",
#         "created_at": "1971-10-20 18:06:17",
#         "updated_at": "1985-06-08 00:13:46"
#     }
#     response = requests.post(f"{BASE_URL}/suppliers/", headers=header, json=suppliers)
#     assert response.status_code == 201
# # IT-data-get-suppliers - checken of je de verwachte data terug krijgt
# def test_data_get_suppliers():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/suppliers/100000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-suppliers
# def test_data_update_suppliers():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"name": "Updated Supplier Name"}

#     response = requests.put(f"{BASE_URL}/suppliers/100000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-suppliers
# def test_data_delete_suppliers():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/suppliers/100000/", headers=header)
#     assert response.status_code == 204
# # check if supplier is not found
# def test_data_check_delete_suppliers():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/suppliers/100000/", headers=header)
#     assert response.status_code == 404




# # IT-auth-get-transfers - checken of API key goed werkt
# def test_auth_get_transfers():
#     response = requests.get(f"{BASE_URL}/transfers/")
#     assert response.status_code == 401
# # IT-data-post-transfers - checken of uploaden goed gaat
# def test_data_post_transfers():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     transfers = {
#         "id": 1000000,
#         "reference": "TR00001",
#         "transfer_from": "",
#         "transfer_to": 9229,
#         "transfer_status": "Completed",
#         "created_at": "2000-03-11T13:11:14Z",
#         "updated_at": "2000-03-12T16:11:14Z",
#         "items": [
#             {
#                 "item_id": "P007435",
#                 "amount": 23
#             }
#         ]
#     }
#     response = requests.post(f"{BASE_URL}/transfers/", headers=header, json=transfers)
#     assert response.status_code == 201
# # IT-data-get-transfers - checken of je de verwachte data terug krijgt
# def test_data_get_transfers():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/transfers/1000000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-transfers
# def test_data_update_transfers():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"status": "Updated Transfer Status"}

#     response = requests.put(f"{BASE_URL}/transfers/1000000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-transfers
# def test_data_delete_transfers():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/transfers/1000000/", headers=header)
#     assert response.status_code == 204
# # check if transfer is not found
# def test_data_check_delete_transfer():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/transfers/1000000/", headers=header)
#     assert response.status_code == 404


# # IT-auth-get-warehouses - checken of API key goed werkt
# def test_auth_get_warehouses():
#     response = requests.get(f"{BASE_URL}/warehouses/")
#     assert response.status_code == 401
# # IT-data-post-warehouses - checken of uploaden goed gaat
# def test_data_post_warehouses():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     warehouses = {
#         "id": 100000,
#         "code": "YQZZNL56",
#         "name": "Heemskerk cargo hub",
#         "address": "Karlijndreef 281",
#         "zip": "4002 AS",
#         "city": "Heemskerk",
#         "province": "Friesland",
#         "country": "NL",
#         "contact": {
#             "name": "Fem Keijzer",
#             "phone": "(078) 0013363",
#             "email": "blamore@example.net"
#         },
#         "created_at": "1983-04-13 04:59:55",
#         "updated_at": "2007-02-08 20:11:00"
#     }
#     response = requests.post(f"{BASE_URL}/warehouses/", headers=header, json=warehouses)
#     assert response.status_code == 201
# # IT-data-get-warehouses - checken of je de verwachte data terug krijgt
# def test_data_get_warehouses():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     response = requests.get(f"{BASE_URL}/warehouses/100000/", headers=header)
#     assert response.status_code == 200
#     # Validate expected fields here if necessary
# # IT-data-update-warehouses
# def test_data_update_warehouses():
#     header = {"X-API-Key": "a1b2c3d4e5"}
#     data = {"location": "Updated Warehouse Location"}

#     response = requests.put(f"{BASE_URL}/warehouses/100000/", headers=header, json=data)
#     assert response.status_code == 200
# # IT-data-delete-warehouses
# def test_data_delete_warehouses():
#     header = {"X-API-Key": "a1b2c3d4e5"}

#     response = requests.delete(f"{BASE_URL}/warehouses/100000/", headers=header)
#     assert response.status_code == 204
# # check if warehouse is not found
# def test_data_check_delete_warehouse():
#     header = {"X-API-Key" : "a1b2c3d4e5"}

#     response = requests.get(f"{BASE_URL}/warehouses/100000/", headers=header)
#     assert response.status_code == 404

