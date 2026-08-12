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
        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
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
