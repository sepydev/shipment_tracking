from django.urls import path

from shipment.views import ShipmentListView

urlpatterns = [
    path('list/', ShipmentListView.as_view(), name='shipment-list'),
]
