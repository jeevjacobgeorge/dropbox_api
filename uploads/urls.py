from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('get-phone/', ImageUploadView.as_view(), name='get-image'),  # GET endpoint using query parameters
]
