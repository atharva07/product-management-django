from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(
    "viewset-products",
    views.ProductViewSet,
    basename="product"
)

urlpatterns = [
    path("", views.products, name="products"),
    path("api/", views.product_list_api, name="product-list-api"),
    path("<int:id>/", views.product_detail, name="product-detail"),
    path("apiview/", views.ProductListAPIView.as_view(), name="product-list-apiview"),
    path("apiview/<int:id>/", views.ProductDetailAPIView.as_view(), name="product-detail-apiview"),
    path("generic/", views.ProductListCreateAPIView.as_view(), name="product-list-create-generic"),
    path("generic/<int:pk>/", views.ProductDetailGenericAPIView.as_view(), name="product-detail-generic"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]

urlpatterns += router.urls