from rest_framework import serializers
from .models import CustomerReview

class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = '__all__'   # Add other fields if necessary
