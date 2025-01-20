from django.shortcuts import render
from django.conf import settings
# Create your views here.
# test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (ClientSerializer, InventorySerializer, ItemGroupSerializer, ItemTypeSerializer, 
                          ItemSerializer, LocationSerializer, OrderSerializer, ShipmentSerializer, 
                          SupplierSerializer, TransferSerializer, WarehouseSerializer)
from rest_framework.exceptions import NotFound, ValidationError
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import path

from api.models.clients import Clients
from api.models.inventories import Inventories
from api.models.item_groups import Item_Groups
from api.models.item_lines import Item_Lines
from api.models.item_types import Item_Types
from api.models.items import Items
from api.models.locations import Locations
from api.models.orders import Orders
from api.models.shipments import Shipments
from api.models.suppliers import Suppliers
from api.models.transfers import Transfers
from api.models.warehouses import Warehouses

def baseurl_view(request):
    return HttpResponse("Welcome to the Cargohub API! :)", status=200)

class GenericView(APIView):
    model_class = None  # Will be set dynamically in child views
    model_instance = None  # Instance of the model used for DB operations
    serializer_class = None  # Used for serialization
    # api fix?
    def get_api_key(self, request):
        """
        Retrieve the API key from request headers.
        """
        return request.headers.get("APIKEYADMIN")
    

    def validate_api_key(self, request):
        """
        Validate the API key. 
        """
        api_key = self.get_api_key(request)
        print(f"Extracted API Key: {api_key}")
        print(f"Expected API Key: {settings.APIKEYADMIN}")
        if api_key != settings.APIKEYADMIN:
            return False
        return True

    def handle_unauthorized(self):
        """
        Return a standard response for unauthorized access.
        """
        return JsonResponse(
            {"error": "Unauthorized: Invalid or missing API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def get(self, request, *args, **kwargs):
        if not self.validate_api_key(request):
            return self.handle_unauthorized()

        model_instance = self.model_instance()

        if 'request_id' in kwargs:
            request_id = kwargs.get('request_id')
            model_method = model_instance.get(request_id)  # Call the specific model's method
            if model_method is None:
                return JsonResponse({"error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(model_method, status=status.HTTP_200_OK)

        # For the general case (e.g., fetch all clients)
        model_multiple = model_instance.gets()  # Fetch all
        if not model_multiple:
            return JsonResponse({"message": "No list found"}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse(model_multiple, safe=False, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not self.validate_api_key(request):
            return self.handle_unauthorized()

        model_instance = self.model_instance()  # Create an instance of the model
        request_data = request.data
        model_instance.add(request_data)  # Call the add method on the model instance
        return JsonResponse(request_data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        if not self.validate_api_key(request):
            return self.handle_unauthorized()

        request_id = kwargs.get('request_id')
        if not request_id:
            return JsonResponse({"error": "request_id is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        model_instance = self.model_instance()  # Create an instance of the model
        request_data = request.data
        model_instance.update(request_id, request_data)  # Update data
        return JsonResponse(request_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if not self.validate_api_key(request):
            return self.handle_unauthorized()

        request_id = kwargs.get('request_id')
        if not request_id:
            return JsonResponse({"error": "request_id is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        model_instance = self.model_instance()  # Create an instance of the model
        model_instance.remove(request_id)  # Call the remove method to delete
        return JsonResponse({"message": "ID deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
    
class ClientView(GenericView):
    model_class = Clients  
    model_instance = Clients 
    serializer_class = ClientSerializer 


class WarehouseView(GenericView):
    model = Warehouses
    model_instance = Warehouses  
    serializer_class = WarehouseSerializer  


class LocationView(GenericView):
    model = Locations
    model_instance = Locations
    serializer_class = LocationSerializer

    def get_locations_in_warehouse(self, request, warehouse_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM locations WHERE warehouse_id = ?"
            cursor.execute(query, (warehouse_id,))
            locations = cursor.fetchall()
            
            if not locations:
                return JsonResponse({"message": f"No locations found for warehouse_id {warehouse_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"locations": locations}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()



class ItemTypeView(GenericView):
    model = Item_Types
    model_instance = Item_Types
    serializer_class = ItemTypeSerializer


class ItemGroupView(GenericView):
    model = Item_Groups
    model_instance = Item_Groups
    serializer_class = ItemGroupSerializer


class ItemView(GenericView):
    model = Items
    model_instance = Items
    serializer_class = ItemSerializer

    def get_items_for_item_line(self, request, item_line_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM items WHERE item_line = ?"
            cursor.execute(query, (item_line_id,))
            items = cursor.fetchall()
            
            if not items:
                return JsonResponse({"message": f"No items found for item_line_id {item_line_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"items": items}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()

    def get_items_for_item_group(self, request, item_group_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM items WHERE item_group = ?"
            cursor.execute(query, (item_group_id,))
            items = cursor.fetchall()
            
            if not items:
                return JsonResponse({"message": f"No items found for item_group_id {item_group_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"items": items}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()

    def get_items_for_item_type(self, request, item_type_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM items WHERE item_type = ?"
            cursor.execute(query, (item_type_id,))
            items = cursor.fetchall()
            
            if not items:
                return JsonResponse({"message": f"No items found for item_type_id {item_type_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"items": items}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()

    def get_items_for_supplier(self, request, supplier_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM items WHERE supplier_id = ?"
            cursor.execute(query, (supplier_id,))
            items = cursor.fetchall()
            
            if not items:
                return JsonResponse({"message": f"No items found for supplier_id {supplier_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"items": items}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()



class InventoryView(GenericView):
    model = Inventories
    model_instance = Inventories
    serializer_class = InventorySerializer

    def get_inventories_for_item(self, request, item_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM inventories WHERE item_id = ?"
            cursor.execute(query, (item_id,))
            inventories = cursor.fetchall()

            if not inventories:
                return JsonResponse({"message": f"No inventories found for item ID {item_id}"}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"inventories": inventories}, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()
            conn.close()

    def get_inventory_totals_for_item(self, request, item_id):
        result = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0
        }

        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            cursor = conn.cursor()
            query = """
                SELECT total_expected, total_ordered, total_allocated, total_available
                FROM inventories
                WHERE item_id = ?
            """
            cursor.execute(query, (item_id,))
            inventories = cursor.fetchall()

            if not inventories:
                return JsonResponse({"message": f"No inventories found for item ID {item_id}"}, status=status.HTTP_404_NOT_FOUND)

            for inventory in inventories:
                result["total_expected"] += inventory[0]
                result["total_ordered"] += inventory[1]
                result["total_allocated"] += inventory[2]
                result["total_available"] += inventory[3]

            return JsonResponse(result, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()
            conn.close()



class OrderView(GenericView):
    model = Orders
    model_instance = Orders
    serializer_class = OrderSerializer

    def get_items_in_order(self, request, order_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT items FROM orders WHERE id = ?"
            cursor.execute(query, (order_id,))
            order = cursor.fetchone()
            
            if order is None:
                return JsonResponse({"message": f"No order found with id {order_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"items": order[0]}, status=status.HTTP_200_OK)  
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()

    def get_orders_in_shipment(self, request, shipment_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = "SELECT id FROM orders WHERE shipment_id = ?"
            cursor.execute(query, (shipment_id,))
            orders = cursor.fetchall()
            
            if not orders:
                return JsonResponse({"message": f"No orders found for shipment_id {shipment_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            order_ids = [order[0] for order in orders]
            return JsonResponse({"order_ids": order_ids}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()

    def get_orders_for_client(self, request, client_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM orders WHERE ship_to = ? OR bill_to = ?
            """
            cursor.execute(query, (client_id, client_id))
            orders = cursor.fetchall()
            
            if not orders:
                return JsonResponse({"message": f"No orders found for client_id {client_id}"}, status=status.HTTP_404_NOT_FOUND)
            
            return JsonResponse({"orders": orders}, safe=False, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            conn.close()



class SupplierView(GenericView):
    model = Suppliers
    model_instance = Suppliers
    serializer_class = SupplierSerializer


class ShipmentView(GenericView):
    model = Shipments
    model_instance = Shipments
    serializer_class = ShipmentSerializer

    def get_items_in_shipment(self, request, shipment_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            cursor = conn.cursor()
            query = "SELECT items FROM shipments WHERE id = ?"
            cursor.execute(query, (shipment_id,))
            shipment = cursor.fetchone()

            if shipment is None:
                return JsonResponse({"message": f"No shipment found with id {shipment_id}"}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"items": shipment[0]}, safe=False, status=status.HTTP_200_OK)  

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()
            conn.close()



class TransferView(GenericView):
    model = Transfers
    model_instance = Transfers
    serializer_class = TransferSerializer

    def get_items_in_transfer(self, request, transfer_id):
        conn = self.model.db.connection(self.model.dbfile)
        if conn is None:
            return JsonResponse({"error": "DB connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            cursor = conn.cursor()
            query = "SELECT items FROM transfers WHERE id = ?"
            cursor.execute(query, (transfer_id,))
            result = cursor.fetchone()

            if result is None:
                return JsonResponse({"message": f"Transfer with id {transfer_id} not found"}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"items": result[0]}, safe=False, status=status.HTTP_200_OK)  

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            cursor.close()
            conn.close()


