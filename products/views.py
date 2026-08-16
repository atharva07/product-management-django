import json
from django.http import JsonResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
) 
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .permissions import ProductRBACPermission, IsOwnerOrAdmin
from .pagination import ProductPagination

# Create your views here
# This is a method using manual API creation
@csrf_exempt
def products(request):
    if request.method == "GET":
        products = Product.objects.all()
        data = []

        for product in products:
            data.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "quantity": product.quantity
            })

        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        # we use json.loads to convert JSON into Python dictionary
        data = json.loads(request.body)

        product = Product.objects.create(
            name = data["name"],
            description = data["description"],
            price= data["price"],
            quantity = data["quantity"],
        )

        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "quantity": product.quantity,
        }, status = 201)

@csrf_exempt
def product_detail(request, id):
    # This will return the response in positive test case, in negative test case this will return 404 Not Found Error
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "quantity": product.quantity,
        })

    elif request.method == "PUT":
        data = json.loads(request.body)

        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.quantity = data["quantity"]

        product.save()

        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "quantity": product.quantity,
        })

    elif request.method == "DELETE":
        product.delete()

        return JsonResponse({
            "message": "Product Deleted Successfully"
        })

# This is a method using api_view
@api_view(["GET", "POST"])
def product_list_api(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

@api_view(["PUT", "PATCH", "DELETE"])
def product_update_delete_api(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product Not Found"},
            status = 404
        )

    if request.method == "PUT":
        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == "PATCH":
        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )

    elif request.method == "DELETE":
        product.delete()

        return Response(
            {"message": "Product deleted successfully"},
            status=204
        )

# This method is using Generic View
# This is a method using ListAPIView
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetailAPIView(APIView):
    def get_product(self, id):
        return get_object_or_404(Product, id=id)

    def get(self, request, id):
        product = self.get_product(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_product(id)
        # Here we are serializing the data coming from the request and the existing product instance
        serializer = ProductSerializer(
            product,
            # Here we are deserializing the data coming from the request to update the existing product instance
            data=request.data
        )

        # Here also the data will be converted to Python dictionary using deserializer and the validated
        if serializer.is_valid():
            serializer.save()
            # Here we are returning the serialized data of the updated product instance
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        product = self.get_product(id)
        product.delete()
        return Response(
            {
                "message": "Product deleted Successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )

# This method is using Generic View - GET, POST
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# GET, PUT, PATCH, DELETE
class ProductDetailGenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# This is the concept of Viewset
# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # This is Authentication part, Every Request requires an Authenticated user
#     #permission_classes = [IsAdminReadOnly, IsOwnerOrAdmin]
#     permission_classes = [ProductRBACPermission]

#     def get_queryset(self):
#         # If the user is staff, which means he is an admin, then return all the products
#         if self.request.user.is_staff:
#             return Product.objects.all()

#         # Else return only the products which are owner by the user who is making the request
#         return Product.objects.filter(
#             owner = self.request.user
#         )

#     def perform_create(self, serializer):
#         # Here we are setting the owner of the product to the user who is making the request
#         serializer.save(owner=self.request.user)

#     # detail = True -> Action for ONE object
#     @action(detail=True, methods=["post"])
#     def mark_out_of_stock(self, request, pk=None):
#         product = self.get_object()
#         product.quantity = 0
#         product.save()

#         return Response({
#             "message": "Product marked as out of Stock",
#             "product_id": product.id
#         })

#     # detail = False -> Action for a COLLECTION
#     @action(detail=False, methods=["get"])
#     def low_stock(self, request):
#         products = Product.objects.filter(quantity__lt=5)

#         serializer = ProductSerializer(
#             products,
#             many=True
#         )
#         return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [
        DjangoModelPermissions, 
        IsOwnerOrAdmin
    ]

    def get_queryset(self):
        if self.request.user.groups.filter(
            name="Admin"
        ).exists():
            return Product.objects.all()

        return Product.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # These are custom actions, which are not part of the standard CRUD operations
    @action(detail=True, methods=["POST"])
    def mark_out_of_stock(self, request, pk=None):
        product = self.get_object()
        product.quantity = 0
        product.save()

        return Response({
            "message": "Product marked as out of Stock",
            "product_id": product.id
        })

    @action(detail=False, methods=["GET"])
    def low_stock(self, request):
        products = Product.objects.filter(quantity__lt=5)

        serializer = ProductSerializer(
            products, 
            many=True
        )

        return Response(serializer.data)