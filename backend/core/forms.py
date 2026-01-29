from django import forms
from .models import SafetyWalk, Observation
from django.contrib.auth.forms import AuthenticationForm

class SafetyWalkForm(forms.ModelForm):
    class Meta:
        model = SafetyWalk
        fields = ["date", "shift", "area"]  # number i performed_by ustawiamy w kodzie


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ["ppe", "work", "environment", "reaction", "comment"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(attrs={
            "placeholder": "Wpisz login",
            "autocomplete": "username",
        })
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Wpisz hasło",
            "autocomplete": "current-password",
        })
    )
    error_messages = {
        "invalid_login": "Błędny login lub hasło.",
        "inactive": "To konto jest nieaktywne.",
    }