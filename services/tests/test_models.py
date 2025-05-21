from django.test import TestCase
from services.models import Service, ServiceRequest
from users.models import User, Company, Customer
from django.utils import timezone


class ServiceModelTests(TestCase):
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

    def test_service_creation(self):
        self.assertTrue(isinstance(self.service, Service))
        self.assertEqual(self.service.name, "Pipe Repair")  # Changed from title to name
        self.assertEqual(self.service.company, self.company)
        self.assertEqual(self.service.field, "Plumbing")
        self.assertEqual(
            self.service.price_hour, 100.00
        )  # Changed from price to price_hour


class ServiceRequestModelTests(TestCase):
    def setUp(self):
        # Create a company user
        self.company_user = User.objects.create_user(
            username="testcompany",
            email="company@example.com",
            password="testpassword123",
            is_company=True,
        )
        self.company = Company.objects.create(user=self.company_user, field="Plumbing")

        # Create a customer user
        self.customer_user = User.objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="testpassword123",
            is_customer=True,
        )
        self.customer = Customer.objects.create(
            user=self.customer_user, birth=timezone.now().date()
        )

        # Create a service - UPDATED field names
        self.service = Service.objects.create(
            name="Pipe Repair",  # Changed from title to name
            description="Fix leaking pipes",
            company=self.company,
            field="Plumbing",
            price_hour=100.00,  # Changed from price to price_hour
        )

        # Create a service request
        self.service_request = ServiceRequest.objects.create(
            service=self.service,
            user=self.customer_user,
            address="123 Test St",
            message="Need help with plumbing",  # Added message field which is required
            service_time=2.0,  # Added service_time in hours instead of date/time
            status="pending",  # Make sure to use lowercase status value that matches choices
        )

    def test_service_request_creation(self):
        self.assertTrue(isinstance(self.service_request, ServiceRequest))
        self.assertEqual(self.service_request.service, self.service)
        self.assertEqual(self.service_request.user, self.customer_user)
        self.assertEqual(self.service_request.address, "123 Test St")
        self.assertEqual(self.service_request.message, "Need help with plumbing")
        self.assertEqual(self.service_request.service_time, 2.0)
        self.assertEqual(self.service_request.status, "pending")
        # Check that total_cost was calculated correctly
        self.assertEqual(self.service_request.total_cost, 200.00)  # 2 hours * $100/hour
