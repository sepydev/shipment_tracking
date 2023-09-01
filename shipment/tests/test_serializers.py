from dataclasses import asdict
from unittest.mock import patch

from django.test import TestCase

from shipment.models import Shipment
from shipment.serializers import ShipmentWeatherSerializer
from weather_info.weather_info import WeatherInfo


class ShipmentWeatherSerializerTest(TestCase):

    def setUp(self):
        self.shipment = Shipment.objects.create(
            carrier='DHL',
            status='In transit',
            sender_address="Street 1, 10115 Berlin, Germany",
            receiver_address="Street 10, 75001 Paris, France"
        )
        self.shipment.article_set.create(
            name='iPhone 12',
            quantity=1,
            price=1000.0,
        )
        self.shipment.refresh_from_db()

    @patch('shipment.serializers.weather_Api.get_weather')
    def test_to_representation(self, mock_get_weather):
        weather_data = WeatherInfo(**{
            'city': 'Paris',
            'temperature': 20.5,
            'wind_speed': 10.2,
            'wind_direction': 'N',
            'pressure': 1013.2,
            'humidity': 50.0,
            'description': 'Cloudy'
        })
        mock_get_weather.return_value = weather_data
        serializer = ShipmentWeatherSerializer(instance=self.shipment)

        self.assertTrue('articles' in serializer.data)

        self.assertTrue('weather_info' in serializer.data)
        self.assertEqual(serializer.data['weather_info'], asdict(weather_data))

    def test_get_city_from_address(self):
        serializer = ShipmentWeatherSerializer()

        address = "Street 10, 75001 Paris, France"
        city = serializer.get_city_from_address(address)
        self.assertEqual(city, "Paris")

        address = "123 Main St, 10002 Los Angeles, USA"
        city = serializer.get_city_from_address(address)
        self.assertEqual(city, "Los Angeles")
