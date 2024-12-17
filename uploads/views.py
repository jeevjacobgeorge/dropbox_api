from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ImageUploadSerializer
from .dropbox_helper import upload_to_dropbox, get_images_from_dropbox
import tempfile
import os
from datetime import datetime
from .models import Image





class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the incoming data
        serializer = ImageUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract the name, phone_number, and images from the validated data
            phone_number = serializer.validated_data['phone_number']
            images = serializer.validated_data['images']
            name = serializer.validated_data['name']
            upload_results = []  # To store the result for each image
            saved_images = []  # List to store the created image records
            
            # Process each image in the list
            for image in images:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    try:
                        # Write the image content to the temp file
                        temp_file.write(image.read())
                        temp_file.seek(0)  # Reset pointer to the beginning of the file
                        
                        # Get the current date and time, formatted as YYYYMMDD_HHMMSS
                        current_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                        
                        # Create a unique filename using the current date/time and the original file name
                        unique_filename = f'{current_time}_{image.name}'
                        path = f'{phone_number}/{unique_filename}'
                        # Upload the file to Dropbox
                        result = upload_to_dropbox(temp_file.name, path)
                        if result:
                            # Save the image details in the database
                            image_url = result.get("image_url")  # Extract the URL from the result
                            image_record = Image.objects.create(
                                name=name,
                                phone_number=phone_number,
                                file_name=unique_filename,
                                image_url=image_url
                            )
                            saved_images.append(image_record)
                            
                            upload_results.append({"filename": unique_filename, "message": result})
                        else:
                            upload_results.append({"filename": unique_filename, "message": "Failed to upload."})
                    finally:
                        # Clean up temporary file after uploading
                        os.remove(temp_file.name)
            
            # Return a summary of the results
            if all(res['message'] == "Failed to upload." for res in upload_results):
                return Response({"message": "Failed to upload all images."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Return the results along with the name and phone number
            return Response({
                "phone_number": phone_number,
                "results": upload_results
            }, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Handle GET request to retrieve image URLs from Dropbox."""
        # Get phone_number and name from query parameters
        phone_number = request.query_params.get('phone_number')
        
        if not phone_number:
            return Response({"message": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch image URLs using the helper function
        image_urls = get_images_from_dropbox(phone_number)

        if image_urls is None:
            return Response({"message": "Failed to retrieve images from Dropbox."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If no images are found, return a 404 response
        if not image_urls:
            return Response({"message": "No images found for the provided phone number."}, status=status.HTTP_404_NOT_FOUND)

        # Return the image URLs
        return Response({
            "phone_number": phone_number,
            "image_urls": image_urls
        }, status=status.HTTP_200_OK)
