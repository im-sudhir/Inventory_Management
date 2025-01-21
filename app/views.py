import logging
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import InventoryItemSerializer
from .models import InventoryItem
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated

# Configure logger for the app
logger = logging.getLogger('inventory')

# Filter for InventoryItem
class NameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = InventoryItem
        fields = ['name', 'in_stock']

# List and Create View
class ItemListCreateView(ListCreateAPIView):
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NameFilter
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user} is retrieving the item list with filters: {request.query_params}")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info(f"User {request.user} is creating a new inventory item with data: {request.data}")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            logger.info(f"Item created successfully: {response.data}")
        else:
            logger.warning(f"Failed to create item: {response.data}")
        return response

# Retrieve, Update, Destroy View
class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user} is retrieving details for item ID: {item_id}")
        response = super().get(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Item details retrieved successfully for ID: {item_id}")
        else:
            logger.warning(f"Item with ID {item_id} not found")
        return response

    def put(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user} is updating item ID: {item_id} with data: {request.data}")
        response = super().put(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Item ID {item_id} updated successfully: {response.data}")
        else:
            logger.error(f"Failed to update item ID {item_id}: {response.data}")
        return response

    def patch(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user} is partially updating item ID: {item_id} with data: {request.data}")
        response = super().patch(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Item ID {item_id} partially updated successfully: {response.data}")
        else:
            logger.error(f"Failed to partially update item ID {item_id}: {response.data}")
        return response

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        logger.info(f"User {request.user} is deleting item ID: {item_id}")
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            logger.info(f"Item ID {item_id} deleted successfully")
        else:
            logger.error(f"Failed to delete item ID {item_id}: {response.data}")
        return response
