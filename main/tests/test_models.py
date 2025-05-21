from django.test import TestCase
from django.core.exceptions import ValidationError
from main.models import HomePage, AboutPage, ContactPage
from django.utils import timezone


class HomePageModelTests(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.create(
            title="Welcome to NetFix",
            subtitle="Your Home Service Solution",
            description="We provide excellent home services",
        )

    def test_homepage_creation(self):
        self.assertTrue(isinstance(self.homepage, HomePage))
        self.assertEqual(self.homepage.__str__(), "Welcome to NetFix")
        self.assertEqual(self.homepage.title, "Welcome to NetFix")
        self.assertEqual(self.homepage.subtitle, "Your Home Service Solution")

    def test_homepage_timestamps(self):
        self.assertIsNotNone(self.homepage.created_at)
        self.assertIsNotNone(self.homepage.updated_at)


class AboutPageModelTests(TestCase):
    def setUp(self):
        self.aboutpage = AboutPage.objects.create(
            title="About NetFix", content="We are a leading home service provider"
        )

    def test_aboutpage_creation(self):
        self.assertTrue(isinstance(self.aboutpage, AboutPage))
        self.assertEqual(self.aboutpage.__str__(), "About NetFix")
        self.assertEqual(self.aboutpage.title, "About NetFix")
        self.assertEqual(
            self.aboutpage.content, "We are a leading home service provider"
        )

    def test_aboutpage_timestamps(self):
        self.assertIsNotNone(self.aboutpage.created_at)
        self.assertIsNotNone(self.aboutpage.updated_at)


class ContactPageModelTests(TestCase):
    def setUp(self):
        self.contactpage = ContactPage.objects.create(
            title="Contact Us",
            email="contact@netfix.com",
            phone="+1234567890",
            address="123 Service Street, City",
        )

    def test_contactpage_creation(self):
        self.assertTrue(isinstance(self.contactpage, ContactPage))
        self.assertEqual(self.contactpage.__str__(), "Contact Us")
        self.assertEqual(self.contactpage.email, "contact@netfix.com")
        self.assertEqual(self.contactpage.phone, "+1234567890")
