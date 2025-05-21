def debug_form(form):
    """Helper function to print form errors during tests"""
    if not form.is_valid():
        print("\nForm errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {', '.join(errors)}")
    return form.is_valid()


def debug_response(response):
    """Helper function to print response details during tests"""
    print(f"\nResponse status: {response.status_code}")
    print(f"Response templates: {[t.name for t in response.templates]}")
    print(f"Response context: {response.context.keys()}")
    return response
