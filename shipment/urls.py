from django.urls import path

from shipment.views import ShipmentListView

urlpatterns = [
    path('mymodel/', ShipmentListView.as_view(), name='shipment-list'),
]
