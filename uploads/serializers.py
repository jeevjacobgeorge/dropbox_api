from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)  # Accept a name as a string
    phone_number = serializers.CharField(max_length=15)  # Accept phone number (consider regex for validation)
    images = serializers.ListField(
        child=serializers.ImageField(),  # Handle multiple image files
        allow_empty=False  # Prevent an empty list
    )
