from django import forms
from django.forms import inlineformset_factory
from .models import SafetyWalk, Observation

class SafetyWalkForm(forms.ModelForm):
    class Meta:
        model = SafetyWalk
        fields = ["date", "shift", "area"]  # number i performed_by ustawiamy w kodzie


ObservationFormSet = inlineformset_factory(
    parent_model=SafetyWalk,
    model=Observation,
    fields=["ppe", "work", "environment", "reaction", "comment"],
    extra=1,
    can_delete=True,
)
