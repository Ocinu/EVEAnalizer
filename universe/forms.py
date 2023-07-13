from django import forms
from django.db.models import Q
from django_select2 import forms as s2forms

from universe.models import Region


class RegionRouteForm(forms.Form):
    region = forms.ChoiceField(
        choices=[
            (r.eve_id, r.name) for r in Region.objects.filter(~Q(name__regex=r"\d+"))
        ],
        widget=s2forms.Select2Widget(attrs={"class": "col-md form-control"}),
    )
    sec_status = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "col-md form-control"}),
        choices=Region.StatusChoices.choices,
        label="Security status",
    )

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get("region")

        if not region:
            raise forms.ValidationError("You must select exist region")
