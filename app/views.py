from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializers import InventoryItemSerializer
from .models import InventoryItem
# Create your views here.

class ItemListCreateView(ListCreateAPIView):
    serializer_class=InventoryItemSerializer
    queryset=InventoryItem.objects.all()