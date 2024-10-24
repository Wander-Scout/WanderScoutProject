from django.db import models
from django.contrib.auth.models import User

class CustomerReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(max_length=500)
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)]) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} Stars"
