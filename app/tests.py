from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import InventoryItem

class InventoryItemAPITestCase(APITestCase):

    def setUp(self):
        # Create a test inventory item
        self.item = InventoryItem.objects.create(
            name="Test Item", 
            description="Test Description", 
            in_stock=True
        )
        # Define URLs for list and detail views
        self.list_url = reverse('items')
        self.detail_url = reverse('item-detailview', kwargs={'pk': self.item.id})

    def test_get_items_list(self):
        # Test retrieving a list of items
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_item(self):
        # Test creating a new item
        data = {
            "name": "New Item", 
            "description": "New Description", 
            "in_stock": False
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(response.data['in_stock'])

    def test_create_item_with_duplicate_name(self):
        # Test creating an item with a duplicate name
        data = {
            "name": "Test Item",  # Duplicate name
            "description": "Another Description", 
            "in_stock": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_get_item_detail(self):
        # Test retrieving details of a specific item
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)
        self.assertEqual(response.data['description'], self.item.description)
        self.assertTrue(response.data['in_stock'])

    def test_update_item(self):
        # Test updating an existing item with new data
        data = {
            "name": "Updated Item", 
            "description": "Updated Description", 
            "in_stock": False
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(response.data['in_stock'])

    def test_partial_update_item(self):
        # Test partially updating an item using PATCH
        data = {"in_stock": False}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['in_stock'])

    def test_delete_item(self):
        # Test deleting an existing item
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InventoryItem.objects.filter(id=self.item.id).exists())

    def test_get_non_existent_item(self):
        # Test retrieving a non-existent item
        url = reverse('item-detailview', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
