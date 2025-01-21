import logging
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import InventoryItem

# Configure logger for the test module
logger = logging.getLogger('inventory_tests')

class InventoryItemAPITestCase(APITestCase):

    def setUp(self):
        logger.info("Setting up test environment")
        
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        logger.debug("Test user created: %s", self.user.username)
        
        # Generate JWT access token for the user
        self.token = str(AccessToken.for_user(self.user))
        logger.debug("JWT token generated for user: %s", self.token)
        
        # Include the token in the client's Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create a test inventory item
        self.item = InventoryItem.objects.create(
            name="Test Item", 
            description="Test Description", 
            in_stock=True
        )
        logger.debug("Test inventory item created: %s", self.item.name)
        
        # Define URLs for list and detail views
        self.list_url = reverse('items')
        self.detail_url = reverse('item-detailview', kwargs={'pk': self.item.id})

    def test_get_items_list(self):
        logger.info("Testing GET items list")
        response = self.client.get(self.list_url)
        logger.debug("Response status: %s, data: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_item(self):
        logger.info("Testing POST create item")
        data = {
            "name": "New Item", 
            "description": "New Description", 
            "in_stock": False
        }
        response = self.client.post(self.list_url, data)
        logger.debug("Response status: %s, data: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(response.data['in_stock'])

    def test_create_item_with_duplicate_name(self):
        logger.info("Testing POST create item with duplicate name")
        data = {
            "name": "Test Item",  # Duplicate name
            "description": "Another Description", 
            "in_stock": True
        }
        response = self.client.post(self.list_url, data)
        logger.debug("Response status: %s, errors: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_get_item_detail(self):
        logger.info("Testing GET item detail")
        response = self.client.get(self.detail_url)
        logger.debug("Response status: %s, data: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)
        self.assertEqual(response.data['description'], self.item.description)
        self.assertTrue(response.data['in_stock'])

    def test_update_item(self):
        logger.info("Testing PUT update item")
        data = {
            "name": "Updated Item", 
            "description": "Updated Description", 
            "in_stock": False
        }
        response = self.client.put(self.detail_url, data)
        logger.debug("Response status: %s, data: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(response.data['in_stock'])

    def test_partial_update_item(self):
        logger.info("Testing PATCH partial update item")
        data = {"in_stock": False}
        response = self.client.patch(self.detail_url, data)
        logger.debug("Response status: %s, data: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['in_stock'])

    def test_delete_item(self):
        logger.info("Testing DELETE item")
        response = self.client.delete(self.detail_url)
        logger.debug("Response status: %s", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InventoryItem.objects.filter(id=self.item.id).exists())

    def test_get_non_existent_item(self):
        logger.info("Testing GET non-existent item")
        url = reverse('item-detailview', kwargs={'pk': 999})
        response = self.client.get(url)
        logger.debug("Response status: %s, errors: %s", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        logger.info("Testing unauthenticated access")
        self.client.credentials()  # Remove token
        response = self.client.get(self.list_url)
        logger.debug("Response status: %s", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
