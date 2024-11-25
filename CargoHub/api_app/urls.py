from django.urls import path
from .views import (ClientView, InventoryView, ItemGroupView, ItemTypeView, ItemView, LocationView, 
                    OrderView, ShipmentView, SupplierView, TransferView, WarehouseView)

urlpatterns = [
    path('clients/', ClientView.as_view(), name='clients'),
    path('inventories/', InventoryView.as_view(), name='inventories'),
    path('item_groups/', ItemGroupView.as_view(), name='item-groups'),
    path('item_types/', ItemTypeView.as_view(), name='item-types'),
    path('items/', ItemView.as_view(), name='items'),
    path('locations/', LocationView.as_view(), name='locations'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('shipments/', ShipmentView.as_view(), name='shipments'),
    path('suppliers/', SupplierView.as_view(), name='suppliers'),
    path('transfers/', TransferView.as_view(), name='transfers'),
    path('warehouses/', WarehouseView.as_view(), name='warehouses'),
]
