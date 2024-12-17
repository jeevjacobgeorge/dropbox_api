from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255,blank=True)  # Store the name of the image
    phone_number = models.CharField(max_length=15,blank=False)  # Store phone number as a string, adjust length if necessary
    file_name = models.CharField(max_length=255)  # Store the file name
    image_url = models.URLField()  # Store the URL of the image in Dropbox

    # Optionally, you could store timestamps or other metadata like file size, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.file_name}"
