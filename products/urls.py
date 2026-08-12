from django.urls import path
from . import views

urlpatterns = [
    path("", views.products, name="products"),
    path("api/", views.product_list_api, name="product-list-api"),
    path("<int:id>/", views.product_detail, name="product-detail"),
    path("apiview/", views.ProductListAPIView.as_view(), name="product-list-apiview"),
    path("apiview/<int:id>/", views.ProductDetailAPIView.as_view(), name="product-detail-apiview"),
    path("generic/", views.ProductListCreateAPIView.as_view(), name="product-list-create-generic"),
    path("generic/<int:pk>/", views.ProductDetailGenericAPIView.as_view(), name="product-detail-generic"),
]