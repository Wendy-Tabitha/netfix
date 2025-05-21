from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User, Customer, Company
from django.utils import timezone
import datetime


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertFalse(self.user.is_company)
        self.assertFalse(self.user.is_customer)


class CustomerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="testpassword123",
            is_customer=True,
        )
        self.customer = Customer.objects.create(
            user=self.user,
            birth=timezone.now().date() - datetime.timedelta(days=365 * 25),
        )

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(
            self.customer.__str__(), f"{self.user.id} - {self.user.username}"
        )
        self.assertTrue(self.user.is_customer)


class CompanyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcompany",
            email="company@example.com",
            password="testpassword123",
            is_company=True,
        )
        self.company = Company.objects.create(user=self.user, field="Plumbing")

    def test_company_creation(self):
        self.assertTrue(isinstance(self.company, Company))
        self.assertEqual(self.company.field, "Plumbing")
        self.assertTrue(self.user.is_company)
