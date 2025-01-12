from django.db import models

# Create your models here.

class InventoryItem(models.Model):
    name=models.CharField(max_length=50, unique=True)
    description=models.CharField(max_length=100)
    in_stock=models.BooleanField(default=True)

    def __str__(self):
        return self.name

