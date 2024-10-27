from django.db import models
from django.contrib.auth.models import User

# model for customer reviews
class CustomerReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # links to the user who wrote the review
    review_text = models.TextField(blank=True, null=True)  # the actual review content which can be empty
    rating = models.IntegerField()  # the rating (1-5), required
    created_at = models.DateTimeField(auto_now_add=True)  # automatically adds the timestamp when the review is created.

    def __str__(self):
        return f"{self.user.username} - {self.rating} Stars"  # shows up in the admin panel

# this model handles the admin's replies to reviews
class AdminReply(models.Model):
    review = models.ForeignKey(
        CustomerReview, on_delete=models.CASCADE, related_name='replies'
    )  # connects this reply to a specific review, using 'replies' as the related name for easy access
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}
    )  # only allows staff users (admins) to be linked to the reply
    reply_text = models.TextField()  # the text of the admin's reply
    created_at = models.DateTimeField(auto_now_add=True)  # adds the timestamp when the reply is created
