import asyncio
from dataclasses import asdict

from rest_framework import serializers

from shipment.models import Shipment, Article
from shipment_traking.settings import container
from weather_info.weather_abstract import WeatherApiABC

weather_Api = container[WeatherApiABC]


class WeatherInfoSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    wind_speed = serializers.FloatField()
    wind_direction = serializers.CharField()
    pressure = serializers.FloatField()
    humidity = serializers.FloatField()
    description = serializers.CharField()


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'


class ShipmentWeatherSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True, source='article_set')
    weather_info = WeatherInfoSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = ['tracking_number', 'carrier', 'status', 'sender_address', 'receiver_address', 'weather_info',
                  'articles']

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        weather_info = asyncio.run(
            weather_Api.get_weather(self.get_city_from_address(data['receiver_address'])))
        data["weather_info"] = asdict(weather_info)
        return data

    def get_city_from_address(self, address):
        city_name = address.split(',')[-2].split(' ')
        city_name = [word for word in city_name if word]
        return ' '.join(city_name[1:])
