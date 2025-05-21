"""netfix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from . import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("services/", include("services.urls")),
    path("register/", include("users.urls")),
    path("customer/<slug:name>", v.customer_profile, name="customer_profile"),
    path("company/<slug:name>", v.company_profile, name="company_profile"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
]

# Error handlers
handler404 = "netfix.views.handler404"
handler500 = "netfix.views.handler500"

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
