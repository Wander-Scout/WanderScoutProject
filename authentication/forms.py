from django import forms
from .models import Profile
from django.utils.html import strip_tags

# form for the profile model with custom cleaning for certain fields
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'age', 'phone_number'] # fields included in the form

    # custom clean method for the 'address' field
    def clean_address(self):
        address = self.cleaned_data.get("address") # get the 'address' field data after validation
        return strip_tags(address)  # Remove any HTML tags

    # If 'phone_number' might contain any characters that need to be stripped of tags, you can do the same:
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number") # get the 'phone_number' field data after validation
        return strip_tags(phone_number) # use strip_tags to remove any HTML tags
