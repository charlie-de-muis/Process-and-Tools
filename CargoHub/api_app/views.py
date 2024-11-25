from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (Client, Inventory, ItemGroup, ItemLine, ItemType, Item, Location, Order, 
                     Shipment, Supplier, Transfer, Warehouse)
from .serializers import (ClientSerializer, InventorySerializer, ItemGroupSerializer, ItemTypeSerializer, 
                          ItemSerializer, LocationSerializer, OrderSerializer, ShipmentSerializer, 
                          SupplierSerializer, TransferSerializer, WarehouseSerializer)


class GenericView(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        instances = self.model.objects.all()
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientView(GenericView):
    model = Client
    serializer_class = ClientSerializer


class WarehouseView(GenericView):
    model = Warehouse
    serializer_class = WarehouseSerializer


class LocationView(GenericView):
    model = Location
    serializer_class = LocationSerializer


class ItemTypeView(GenericView):
    model = ItemType
    serializer_class = ItemTypeSerializer


class ItemGroupView(GenericView):
    model = ItemGroup
    serializer_class = ItemGroupSerializer


class ItemView(GenericView):
    model = Item
    serializer_class = ItemSerializer


class InventoryView(GenericView):
    model = Inventory
    serializer_class = InventorySerializer


class OrderView(GenericView):
    model = Order
    serializer_class = OrderSerializer


class SupplierView(GenericView):
    model = Supplier
    serializer_class = SupplierSerializer


class ShipmentView(GenericView):
    model = Shipment
    serializer_class = ShipmentSerializer


class TransferView(GenericView):
    model = Transfer
    serializer_class = TransferSerializer
