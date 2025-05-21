def test_company_signup_view_get(self):
    response = self.client.get(reverse("register_company"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "users/register_company.html")


def test_customer_signup_view_get(self):
    response = self.client.get(reverse("register_customer"))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "users/register_customer.html")


def test_login_successful(self):
    data = {"email": "test@example.com", "password": "testpassword123"}
    response = self.client.post(reverse("login_user"), data)

    # If your view is redirecting on successful login:
    self.assertEqual(response.status_code, 302)
