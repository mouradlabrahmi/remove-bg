from django import forms

from rmbg.models import Image


class CreateImageMutationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "picture",
            "name",
        ]
