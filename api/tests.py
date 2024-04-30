from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from common.models import Vendor, PurchaseOrder
import json

User = get_user_model()

class VendorManagementSystemTestCase(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        # Initialize client and authenticate user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def create_vendor(self):
        data = {
            "vendor_code": "test_vendor",
            "name": "Test Vendor",
            "contact_details": "Test Contact",
            "address": "Test Address"
        }
        return Vendor.objects.create(**data)

    def create_purchase_order(self):
        vendor = self.create_vendor()
        data = {
            "po_number": "test_po",
            "expected_delivery_date": "2024-04-30",
            "items": json.dumps({'apple':{'quality':'good'},'asus':{'quality':'good'}}),
            "quantity": 10,
            "status": "pending",
            "vendor": vendor
        }
        return PurchaseOrder.objects.create(**data)
        
    def test_authentication(self):
        # Test login endpoint with correct credentials
        url = '/api/login/'
        data = {'email': 'testuser@gmail.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_vendor(self):
        # Test POST /vendors/ endpoint
        url = '/api/vendors/'
        data = {
            "vendor_code": "test_vendor",
            "name": "Test Vendor",
            "contact_details": "Test Contact",
            "address": "Test Address"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        
    def test_vendor_list(self):
        # Test GET /vendors/ endpoint
        url = '/api/vendors/'
        obj = self.create_vendor()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_vendor_detail(self):
        # Test GET /vendors/{vendor_id}/ endpoint
        obj = self.create_vendor()
        vendor_code = obj.pk
        url = f'/api/vendors/{vendor_code}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))


    def test_update_vendor(self):
        # Test PUT /vendors/{vendor_code}/ endpoint
        obj = self.create_vendor()
        vendor_code = obj.pk 
        url = f'/api/vendors/{vendor_code}/'
        data = {
            "vendor_code":vendor_code,
            "name": "Updated Vendor Name",
            "contact_details": "Updated Contact",
            "address": "Updated Address"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.json().get('name'),data['name'])
        
    def test_delete_vendor(self):
        # Test DELETE /vendors/{vendor_code}/ endpoint
        obj = self.create_vendor()
        vendor_code = obj.pk 
        url = f'/api/vendors/{vendor_code}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_create_purchase_order(self):
        # Test POST /purchase_orders/ endpoint
        url = '/api/purchase_orders/'
        vendor = self.create_vendor()
        data = {
            "po_number": "test_po",
            "expected_delivery_date": "2024-04-30",
            "items": json.dumps({'apple':{'quality':'good'},'asus':{'quality':'good'}}),
            "quantity": 10,
            "status": "pending",
            "vendor": vendor.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))

    def test_purchase_order_list(self):
        # Test GET /purchase_orders/ endpoint
        url = '/api/purchase_orders/'
        obj = self.create_purchase_order()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_purchase_order_detail(self):
        # Test GET /purchase_orders/{po_number}/ endpoint
        obj = self.create_purchase_order()
        po_number = obj.pk
        url = f'/api/purchase_orders/{po_number}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))

    def test_update_purchase_order(self):
        # Test PUT /purchase_orders/{po_number}/ endpoint
        obj = self.create_purchase_order()
        po_number = obj.pk
        url = f'/api/purchase_orders/{po_number}/'
        data = {
            "po_number": po_number,
            "expected_delivery_date": "2024-05-30",
            "items": json.dumps({'apple':{'quality':'good'},'asus':{'quality':'good'}}),
            "quantity": 20,
            "status": "completed",
            "vendor": obj.vendor.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.json().get('quantity'), data['quantity'])

    def test_delete_purchase_order(self):
        # Test DELETE /purchase_orders/{po_number}/ endpoint
        obj = self.create_purchase_order()
        po_number = obj.pk
        url = f'/api/purchase_orders/{po_number}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


