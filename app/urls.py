from django.urls import path
from .views import ItemListCreateView, ItemDetailView


urlpatterns=[
    path('items', ItemListCreateView.as_view(), name="items"),
    path('items/<int:pk>', ItemDetailView.as_view(), name='item-detailview'),
]