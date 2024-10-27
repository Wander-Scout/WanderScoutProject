from django import forms
from .models import CustomerReview
from .models import AdminReply
from django.utils.html import strip_tags

# form class for customer reviews
class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview  # links to CustomerReview model where the reviews are saved
        fields = ['review_text', 'rating']  # only these two fields are shown in the form
        widgets = {
            'review_text': forms.Textarea(attrs={
                'placeholder': 'Write your review here...',  # gives message to tell users what to do
                'rows': 3  # sets a small text box for reviews
            }),
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),  # dropdown for ratings from 1 to 5 stars
        }

# form class for admin replies.
class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = AdminReply  # uses the AdminReply model to save replies from admins
        fields = ['reply_text'] 
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'rows': 3,  # small text area for replies
                'placeholder': 'Write your reply here...'  # gives message to tell admins what to do
            }),
        }
