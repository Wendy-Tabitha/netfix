from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = "date"


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={"placeholder": "Enter Email"}),
    )
    birth = forms.DateField(
        required=False, widget=DateInput(attrs={"placeholder": "Enter Birth Date"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "birth")

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Enter Username"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            birth = self.cleaned_data.get("birth")
            Customer.objects.create(user=user, birth=birth)
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={"placeholder": "Enter Email"}),
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field("field").choices,
        widget=forms.Select(attrs={"placeholder": "Select Service Field"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "field")

    def __init__(self, *args, **kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Enter Username"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            field = self.cleaned_data.get("field")
            Company.objects.create(user=user, field=field)
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Enter Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["autocomplete"] = "off"

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is None:
                    raise forms.ValidationError("Invalid email or password")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data
