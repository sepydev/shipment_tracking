from django.db import models


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50)
    carrier = models.CharField(max_length=50)
    sender_address = models.CharField(max_length=500)
    receiver_address = models.CharField(max_length=500)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.tracking_number} - {self.carrier}'


class Article(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    SKU = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} - {self.SKU}'
