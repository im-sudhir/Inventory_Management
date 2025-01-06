from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import InventoryItemSerializer
from .models import InventoryItem
# Create your views here.

class ItemListCreateView(ListCreateAPIView):
    serializer_class=InventoryItemSerializer
    queryset=InventoryItem.objects.all()

class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=InventoryItemSerializer
    queryset=InventoryItem.objects.all()