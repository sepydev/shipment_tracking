from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shipment.models import Shipment


class ShipmentListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('shipment-list')
        Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Street 1, 10115 Berlin, Germany',
            receiver_address='Street 10, 75001 Paris, France',
            status='in-transit'
        )
        Shipment.objects.create(
            tracking_number='TN12345679',
            carrier='UPS',
            sender_address='Street 2, 20144 Hamburg, Germany',
            receiver_address='Street 20, 1000 Brussels, Belgium',
            status='inbound-scan'
        )

    def test_filtering(self):
        response = self.client.get(self.url, {'tracking_number': 'TN12345678', 'carrier': 'DHL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_pagination(self):
        response = self.client.get(self.url, {'offset': 2, 'limit': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_invalid_filter(self):
        response = self.client.get(self.url, {'tracking_number': 'Invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 0)

    def test_no_results(self):
        response = self.client.get(self.url, {'tracking_number': 'NonExistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 0)
