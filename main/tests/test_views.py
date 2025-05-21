from django.test import TestCase
from django.urls import reverse
from main.models import HomePage, AboutPage, ContactPage


class HomeViewTests(TestCase):
    def setUp(self):
        self.homepage = HomePage.objects.create(
            title="Welcome to NetFix",
            subtitle="Your Home Service Solution",
            description="We provide excellent home services",
        )

    def test_home_view(self):
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NetFix")
        self.assertTemplateUsed(response, "main/home.html")
