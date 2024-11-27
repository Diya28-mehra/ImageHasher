from rest_framework import serializers  
from .models import ImageData  
import requests

class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = ['id', 'image_url', 'md5_hash', 'phash', 'created_at', 'modified_at']
        read_only_fields = ['md5_hash', 'phash', 'created_at', 'modified_at']

    def validate_image_url(self, value):
        """
        Validate if the provided URL is reachable and returns an image.
        """
        try:
            response = requests.head(value, timeout=5)  # Perform a HEAD request to check URL
            if response.status_code != 200:
                raise serializers.ValidationError("The URL is not reachable or returned an invalid status code.")
            # Check Content-Type to ensure it's an image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                raise serializers.ValidationError("The URL does not point to a valid image.")
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(f"Error accessing the URL: {str(e)}")
        return value
