# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ImageUploadSerializer
from .dropbox_helper import upload_to_dropbox, get_image_from_dropbox
import tempfile
from django.conf import settings

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the incoming data
        serializer = ImageUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract the image from the validated data
            image = serializer.validated_data['image']
            
            # Save the image temporarily to a file (using a temporary file)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image.read())  # Write the image content to the temp file
                temp_file.seek(0)  # Reset pointer to the beginning of the file
                
                # Upload the file to Dropbox
                result = upload_to_dropbox(temp_file.name, image.name)
                if result:
                    return Response({"message": result}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Failed to upload to Dropbox."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Handle GET request to retrieve image from Dropbox."""
        filename = kwargs.get('filename')  # Retrieve filename from URL parameter
        
        if not filename:
            return Response({"message": "Filename is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get image URL or content from Dropbox
        result = get_image_from_dropbox(filename)
        
        if result:
            return Response({"image_url": result}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed to retrieve image from Dropbox."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
