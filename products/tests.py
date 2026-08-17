from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class ProductAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="test_user",
            password="test_password"
        )

    def test_unauthenticated_product_list(self):

        response = self.client.get(
            "/products/viewset-products/"
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_authenticated_product_list(self):

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/products/viewset-products/"
        )

        self.assertEqual(
            response.status_code,
            200
        )