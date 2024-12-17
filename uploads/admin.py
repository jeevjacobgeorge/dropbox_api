from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin list view
    list_display = ('name','phone_number',  'image_url','file_name', 'uploaded_at')
    
    # Add search functionality for the phone number and file name
    search_fields = ('name','phone_number', 'file_name')
    
    # Add filters for the uploaded_at field to filter images by date
    list_filter = ('uploaded_at',)
    
    # Enable ordering by the uploaded_at field
    ordering = ('-uploaded_at',)
    
    # Optional: Allow editing of fields directly in the list view (inline editing)
   

    # You can also set the default fields in the form for adding/editing
    fields = ('phone_number', 'file_name', 'image_url', 'uploaded_at')

# Register the model and the custom admin class
admin.site.register(Image, ImageAdmin)
