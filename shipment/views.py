from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from shipment.filters import ShipmentFilter
from shipment.models import Shipment
from shipment.serializers import ShipmentWeatherSerializer


class ShipmentListView(ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentWeatherSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ShipmentFilter
