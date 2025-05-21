from django.test import TestCase
from users.forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from users.models import User


class CustomerSignUpFormTests(TestCase):
    def test_valid_customer_form(self):
        form_data = {
            "username": "newcustomer",
            "email": "newcustomer@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "birth": "2000-01-01",
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_customer_form(self):
        form_data = {
            "email": "newcustomer@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "birth": "2000-01-01",
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class CompanySignUpFormTests(TestCase):
    def test_valid_company_form(self):
        form_data = {
            "username": "newcompany",
            "email": "newcompany@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "field": "Plumbing",
        }
        form = CompanySignUpForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())


class UserLoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )

    def test_valid_login_form(self):
        form_data = {"email": "test@example.com", "password": "testpassword123"}
        form = UserLoginForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
