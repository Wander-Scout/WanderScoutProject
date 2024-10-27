from django import forms
from .models import Profile
from django.utils.html import strip_tags

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'age', 'phone_number']

    def clean_address(self):
        address = self.cleaned_data.get("address")
        return strip_tags(address)  # Remove any HTML tags

    # If 'phone_number' might contain any characters that need to be stripped of tags, you can do the same:
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        return strip_tags(phone_number)
