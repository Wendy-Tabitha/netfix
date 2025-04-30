from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.service_list, name='service_list'),
    path('create/', v.create, name='create_service'),
    path('<int:pk>/', v.service_detail, name='service_detail'),
    path('<int:pk>/edit/', v.edit_service, name='edit_service'),
    path('<int:pk>/delete/', v.delete_service, name='delete_service'),
    path('field/<slug:field>/', v.service_field, name='service_field'),
    path('my-requests/', v.my_requests, name='my_requests'),
]
