from django import forms
from .models import CustomerReview

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 3}),
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }
