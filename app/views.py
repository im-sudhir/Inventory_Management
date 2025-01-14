from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import InventoryItemSerializer
from .models import InventoryItem
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class NameFilter(filters.FilterSet):
    name=filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model=InventoryItem
        fields=['name','in_stock']

class ItemListCreateView(ListCreateAPIView):
    serializer_class=InventoryItemSerializer
    queryset=InventoryItem.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class=NameFilter
    permission_classes=[IsAuthenticated]

class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=InventoryItemSerializer
    queryset=InventoryItem.objects.all()
    permission_classes=[IsAuthenticated]