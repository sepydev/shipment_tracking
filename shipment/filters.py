from django_filters import rest_framework as filters

from shipment.models import Shipment


class ShipmentFilter(filters.FilterSet):
    tracking_number = filters.CharFilter(lookup_expr='iexact')
    carrier = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier']
