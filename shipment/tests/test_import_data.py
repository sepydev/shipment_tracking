from django.core.management import call_command
from django.test import TestCase
from io import StringIO
import os

from shipment.models import Shipment, Article


class ImportDataCommandTestCase(TestCase):

    def setUp(self):
        self.csv_file_path = 'test_seed_data.csv'
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write(
                "tracking_number,carrier,sender_address,receiver_address,article_name,article_quantity,article_price,"
                "SKU,status\n")
            csv_file.write(
                'TN12345678,DHL,"Street 1, 10115 Berlin, Germany","Street 10, 75001 Paris, France",Laptop,100,800,'
                'LP123,in-transit\n')
            csv_file.write(
                'TN12345678,DHL,"Street 1, 10115 Berlin, Germany","Street 10, 75001 Paris, France",Mouse,1,25,MO456,'
                'in-transit\n')
            csv_file.write(
                'TN12345679,UPS,"Street 2, 20144 Hamburg, Germany","Street 20, 1000 Brussels, Belgium",Monitor,2,200,'
                'MT789,inbound-scan\n')

    def tearDown(self):
        os.remove(self.csv_file_path)

    def test_import_data_command(self):
        out = StringIO()
        call_command('import_data', self.csv_file_path, stdout=out)
        self.assertIn('Successfully import seed data', out.getvalue())
        self.assertEqual(2, len(Shipment.objects.all()))
        self.assertEqual(3, len(Article.objects.all()))
        shipment_tn12345678 = Shipment.objects.get(tracking_number='TN12345678')
        self.assertEqual("DHL", shipment_tn12345678.carrier)
        self.assertEqual("Street 1, 10115 Berlin, Germany", shipment_tn12345678.sender_address)
        self.assertEqual("Street 10, 75001 Paris, France", shipment_tn12345678.receiver_address)
        self.assertEqual("in-transit", shipment_tn12345678.status)
        article_laptop = shipment_tn12345678.article_set.filter(name='Laptop').first()
        self.assertEqual(100, article_laptop.quantity)
        self.assertEqual(800, article_laptop.price)
        self.assertEqual("LP123", article_laptop.SKU)

