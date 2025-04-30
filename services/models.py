from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Company, Customer

# Create your models here.

class Service(models.Model):
    FIELD_CHOICES = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )

    name = models.CharField(max_length=200)
    field = models.CharField(max_length=70, choices=FIELD_CHOICES)
    description = models.TextField()
    price_hour = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.company.user.username}"

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    message = models.TextField()
    address = models.TextField(help_text="Address where the service is required")
    service_time = models.DecimalField(max_digits=5, decimal_places=2, help_text="Hours needed for the service")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request for {self.service.name} by {self.user.username}"
        
    def save(self, *args, **kwargs):
        # Calculate total cost based on service price_hour and service time
        if not self.total_cost:
            self.total_cost = self.service.price_hour * self.service_time
        super().save(*args, **kwargs)
