from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import InventoryItem

# Create your tests here.
class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item=InventoryItem.objects.create(
            name="Perfume",
            description="Denver perfume, black code",
            in_stock= True
        )
    
    def test_api_listview(self):
        response=self.client.get(reverse("items"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InventoryItem.objects.count(),1)
        self.assertContains(response, self.item.name)
    
    def test_api_detailview(self):
        response = self.client.get(reverse("item-detailview", kwargs={"pk": self.item.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(response.data["name"], self.item.name)
        self.assertEqual(response.data["description"], self.item.description)
        self.assertEqual(response.data["in_stock"], self.item.in_stock)
