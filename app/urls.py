from django.urls import path
from .views import ItemListCreateView, ItemDetailView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name="items"),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detailview'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
