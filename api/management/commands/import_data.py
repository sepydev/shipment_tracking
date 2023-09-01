from django.core.management.base import BaseCommand
from api.models import Shipment, Article
import csv


def get_or_create_shipment(row):
    shipment, created = Shipment.objects.get_or_create(
        tracking_number=row['tracking_number'],
        carrier=row['carrier'],
        sender_address=row['sender_address'],
        receiver_address=row['receiver_address'],
        status=row['status']
    )
    return shipment


def create_article(shipment, row):
    Article.objects.create(
        shipment=shipment,
        name=row['article_name'],
        quantity=row['article_quantity'],
        price=row['article_price'],
        SKU=row['SKU']
    )


class Command(BaseCommand):
    help = 'import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['file']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                shipment = get_or_create_shipment(row)
                create_article(shipment, row)

        print(self.style.SUCCESS('Successfully loaded seed data'))
