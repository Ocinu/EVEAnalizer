from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class PersonCreationForm(UserCreationForm):
    """person registration form"""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class PersonLoginForm(AuthenticationForm):
    """person login form"""

    username = forms.CharField(
        label="Username",
        help_text="person Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        help_text="person password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
