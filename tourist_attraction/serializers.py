from rest_framework import serializers
from .models import TouristAttraction

class TouristAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristAttraction
        fields = '__all__'  # Or specify the fields you want to include
