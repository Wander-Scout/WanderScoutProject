from django import forms
from .models import CustomerReview
from .models import AdminReply

class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 3}),
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = AdminReply
        fields = ['reply_text']
        widgets = {
            'reply_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your reply here...'}),
        }
