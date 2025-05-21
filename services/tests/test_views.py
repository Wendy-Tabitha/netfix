from django.test import TestCase
from django.urls import reverse
from services.models import Service, ServiceRequest
from users.models import User, Company, Customer
from django.utils import timezone


class ServiceListViewTests(TestCase):
    def setUp(self):
        # Create a company user
        self.company_user = User.objects.create_user(
            username="testcompany",
            email="company@example.com",
            password="testpassword123",
            is_company=True,
        )
        self.company = Company.objects.create(user=self.company_user, field="Plumbing")

        # Create services - UPDATED field names
        self.service1 = Service.objects.create(
            name="Pipe Repair",  # Changed from title to name
            description="Fix leaking pipes",
            company=self.company,
            field="Plumbing",
            price_hour=100.00,  # Changed from price to price_hour
        )

        self.service2 = Service.objects.create(
            name="Drain Cleaning",  # Changed from title to name
            description="Unclog drains",
            company=self.company,
            field="Plumbing",
            price_hour=75.00,  # Changed from price to price_hour
        )

    def test_service_list_view(self):
        response = self.client.get(reverse("service_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pipe Repair")
        self.assertContains(response, "Drain Cleaning")
        self.assertEqual(len(response.context["services"]), 2)


class ServiceDetailViewTests(TestCase):
    def setUp(self):
        # Create a company user
        self.company_user = User.objects.create_user(
            username="testcompany",
            email="company@example.com",
            password="testpassword123",
            is_company=True,
        )
        self.company = Company.objects.create(user=self.company_user, field="Plumbing")

        # Create a service - UPDATED field names
        self.service = Service.objects.create(
            name="Pipe Repair",  # Changed from title to name
            description="Fix leaking pipes",
            company=self.company,
            field="Plumbing",
            price_hour=100.00,  # Changed from price to price_hour
        )

    def test_service_detail_view(self):
        # Option 1: Log in as a user before accessing the view
        self.client.login(username="testcompany", password="testpassword123")

        response = self.client.get(reverse("service_detail", args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pipe Repair")
        self.assertContains(response, "Fix leaking pipes")
        self.assertContains(response, "100.00")

    # Alternative approach if login doesn't work or if redirect is expected behavior
    def test_service_detail_view_redirect(self):
        # Option 2: Expect and follow the redirect
        response = self.client.get(reverse("service_detail", args=[self.service.id]))
        self.assertEqual(response.status_code, 302)  # Expect redirect

        # Check that it redirects to the registration page
        self.assertIn("register", response.url)  # Changed from 'login' to 'register'

        # Check that the next parameter is included in the redirect URL
        self.assertIn(f"next=/services/{self.service.id}/", response.url)

        # Optionally, follow the redirect and check the final page
        redirect_response = self.client.get(response.url)
        self.assertEqual(redirect_response.status_code, 200)

    # Additional test to verify that authenticated users can access the page
    def test_service_detail_view_authenticated(self):
        # Log in as a user
        self.client.login(username="testcompany", password="testpassword123")

        # Access the service detail page
        response = self.client.get(reverse("service_detail", args=[self.service.id]))

        # Verify successful access
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pipe Repair")
        self.assertContains(response, "Fix leaking pipes")
        self.assertContains(response, "100.00")
