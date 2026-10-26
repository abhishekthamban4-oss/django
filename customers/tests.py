from django.test import TestCase
from django.urls import reverse
from .models import Customer


class CustomerCRUDTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            phone="1234567890",
            address="123 Wonderland",
        )

    def test_customer_model_str(self):
        self.assertEqual(str(self.customer), "Alice Smith")

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "alice@example.com")

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer-detail', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "123 Wonderland")

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer-create'), {
            'name': 'Bob Jones',
            'email': 'bob@example.com',
            'phone': '9876543210',
            'address': '456 Elm St',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer-list'))
        self.assertTrue(Customer.objects.filter(email='bob@example.com').exists())

    def test_customer_update_view(self):
        response = self.client.post(reverse('customer-update', args=[self.customer.pk]), {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'phone': '5555555555',
            'address': '789 Oak Ave',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer-list'))
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Alice Johnson')
        self.assertEqual(self.customer.phone, '5555555555')

    def test_customer_delete_view(self):
        response = self.client.post(reverse('customer-delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer-list'))
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())
