from .models import Service


def available_service_fields(request):
    # Get all fields that have at least one service
    fields = Service.objects.values_list("field", flat=True).distinct()
    return {"available_fields": fields}
