from django import forms
from myapi.models import Journey


class JourneyForm(forms.ModelForm):

    class Meta:
        model = Journey
        fields = "__all__"