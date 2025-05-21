from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.service_list, name="service_list"),
    path("create/", v.create, name="create_service"),
    path("<int:pk>/", v.service_detail, name="service_detail"),
    path("<int:pk>/edit/", v.edit_service, name="edit_service"),
    path("<int:pk>/delete/", v.delete_service, name="delete_service"),
    path("field/<str:field>/", v.service_field, name="service_field"),
    path("my-requests/", v.my_requests, name="my_requests"),
    path("company-requests/", v.company_requests, name="company_requests"),
    path(
        "request/<int:request_id>/update/<str:new_status>/",
        v.update_request_status,
        name="update_request_status",
    ),
    path("most-requested/", v.most_requested_services, name="most_requested_services"),
    path("create/", v.ServiceCreateView.as_view(), name="service-create"),
    path("<int:pk>/rate/", v.rate_service, name="rate_service"),
]
