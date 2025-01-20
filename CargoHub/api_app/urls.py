from django.urls import path, include
from .views import (ClientView, InventoryView, ItemGroupView, ItemTypeView, ItemView, LocationView, 
                    OrderView, ShipmentView, SupplierView, TransferView, WarehouseView)
from .views import baseurl_view

from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Cargohub API",
        default_version='v1',
        description="Cargohub API description",
    ),
    public=True,
)

urlpatterns = [
    path('', baseurl_view, name='baseurl'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('clients/', ClientView.as_view(), name='client-list'),
    path('clients/<int:client_id>/', ClientView.as_view(), name='client-detail'),   
    path('inventories/', InventoryView.as_view(), name='inventories-list'),
    path('inventories/<int:client_id>/', InventoryView.as_view(), name='inventory-detail'),
    path('inventories/item/<int:item_id>/', InventoryView.get_inventories_for_item, name='get_inventories_for_item'),
    path('inventories/item/<int:item_id>/totals/', InventoryView.get_inventory_totals_for_item, name='get_inventory_totals_for_item'),
    path('item_groups/', ItemGroupView.as_view(), name='item-groups-list'),
    path('item_groups/<int:client_id>/', ItemGroupView.as_view(), name='item_groups-detail'),
    path('item_types/', ItemTypeView.as_view(), name='item-types-list'),
    path('item_types/<int:client_id>/', ItemTypeView.as_view(), name='item_types-detail'),
    path('items/', ItemView.as_view(), name='items-list'),
    path('items/<str:client_id>/', ItemView.as_view(), name='items-detail'),
    path('items/item_line/<int:item_line_id>/', ItemView.get_items_for_item_line, name='get_items_for_item_line'),
    path('items/item_group/<int:item_group_id>/', ItemView.get_items_for_item_group, name='get_items_for_item_group'),
    path('items/item_type/<int:item_type_id>/', ItemView.get_items_for_item_type, name='get_items_for_item_type'),
    path('items/supplier/<int:supplier_id>/', ItemView.get_items_for_supplier, name='get_items_for_supplier'),
    path('locations/', LocationView.as_view(), name='locations-list'),
    path('locations/<int:client_id>/', LocationView.as_view(), name='location-detail'),
    path('locations/warehouse/<int:warehouse_id>/', LocationView.get_locations_in_warehouse, name='get_locations_in_warehouse'),
    path('orders/', OrderView.as_view(), name='orders-list'),
    path('orders/<int:client_id>/', OrderView.as_view(), name='orders-detail'),
    path('orders/<int:order_id>/items/', OrderView.get_items_in_order, name='get_items_in_order'),
    path('orders/shipment/<int:shipment_id>/', OrderView.get_orders_in_shipment, name='get_orders_in_shipment'),
    path('orders/client/<int:client_id>/', OrderView.get_orders_for_client, name='get_orders_for_client'),
    path('shipments/', ShipmentView.as_view(), name='shipments-list'),
    path('shipments/<int:client_id>/', ShipmentView.as_view(), name='shipment-detail'),
    path('shipments/<int:shipment_id>/items/', ShipmentView.get_items_in_shipment, name='get_items_in_shipment'),
    path('suppliers/', SupplierView.as_view(), name='suppliers-list'),
    path('suppliers/<int:client_id>/', SupplierView.as_view(), name='supplier-detail'),
    path('transfers/', TransferView.as_view(), name='transfers-list'),
    path('transfers/<int:client_id>/', TransferView.as_view(), name='transfer-detail'),
    path('transfers/<int:transfer_id>/items/', TransferView.get_items_in_transfer, name='get_items_in_transfer'),
    path('warehouses/', WarehouseView.as_view(), name='warehouses-list'),
    path('warehouses/<int:client_id>/', WarehouseView.as_view(), name='warehouse-detail'),
]
