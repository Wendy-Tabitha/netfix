from django.contrib import admin
from .models import HomePage, AboutPage, ContactPage


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "created_at", "updated_at")
    search_fields = ("title", "subtitle", "description")
    readonly_fields = ("created_at", "updated_at")


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("title", "email", "phone", "created_at", "updated_at")
    search_fields = ("title", "email", "phone", "address")
    readonly_fields = ("created_at", "updated_at")
