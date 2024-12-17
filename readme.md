

# Image Upload API Documentation

## Overview

This API allows users to upload images to Dropbox and fetch image URLs associated with a specific phone number. The API integrates with Dropbox to store and manage the uploaded files, returning raw image URLs that can be used for displaying the images on websites or mobile apps.

The API provides the following endpoints:
1. **POST** `/api/upload/` – Upload one or more images to Dropbox.
2. **GET** `/api/get-phone/?phone_number=<phone_number>` – Retrieve all image URLs associated with a phone number from Dropbox.

## Features

- Upload images to Dropbox, categorized by phone number.
- Automatically generate shared image URLs from Dropbox.
- Store and retrieve phone numbers, file names, and URLs in a database (via Django's admin).
- Image files are stored in Dropbox in a folder named after the phone number.
- Image URLs are returned as raw image URLs (suitable for direct embedding in HTML).

---

## Table of Contents

1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
   - [POST /api/upload/](#post-apipost-upload)
   - [GET /api/get-phone/](#get-apiget-phone)
3. [Models](#models)
4. [Admin Panel](#admin-panel)
5. [Environment Variables](#environment-variables)
6. [Running the Project](#running-the-project)
7. [License](#license)

---

## Installation

### Prerequisites

Make sure you have the following installed on your local environment:
- Python 3.8 or higher
- pip (Python package installer)
- A working Dropbox account with an API app created (for getting the `APP_KEY` and `APP_SECRET`).

### Steps to Install

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install dependencies**:

   Create a virtual environment and install the required dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**:
   
   In the project root, create a `.env` file with the following environment variables:

   ```plaintext
   DROPBOX_APP_KEY=<your_dropbox_app_key>
   DROPBOX_APP_SECRET=<your_dropbox_app_secret>
   DROPBOX_REFRESH_TOKEN=<your_dropbox_refresh_token>
   ```

   The `DROPBOX_REFRESH_TOKEN` is a long-lived token that you can generate by following Dropbox's OAuth flow.

4. **Run database migrations**:

   After setting up the database, run the migrations to create the necessary tables.

   ```bash
   python manage.py migrate
   ```

---

## API Endpoints

### POST /api/upload/

#### Request

- **Endpoint**: `/api/upload/`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Request body**: A JSON object containing the `phone_number` and an array of image files.

  Example request body:

  ```json
  {
    "phone_number": "1234567890",
    "images": [
      <image_file_1>,
      <image_file_2>
    ]
  }
  ```

#### Response

- **200 OK**: On successful upload, returns a list of results with filenames and their respective Dropbox URLs.

  Example response:

  ```json
  {
    "phone_number": "1234567890",
    "results": [
      {
        "filename": "2024-12-17_12:30:45_image1.jpg",
        "message": "File '2024-12-17_12:30:45_image1.jpg' uploaded successfully to Dropbox",
        "image_url": "https://www.dropbox.com/s/abcdefg/2024-12-17_12:30:45_image1.jpg?raw=1"
      },
      {
        "filename": "2024-12-17_12:31:00_image2.jpg",
        "message": "File '2024-12-17_12:31:00_image2.jpg' uploaded successfully to Dropbox",
        "image_url": "https://www.dropbox.com/s/hijklmn/2024-12-17_12:31:00_image2.jpg?raw=1"
      }
    ]
  }
  ```

- **400 BAD REQUEST**: If the input data is invalid (missing `phone_number` or `images`).

  Example response:

  ```json
  {
    "message": "Phone number and images are required."
  }
  ```

- **500 INTERNAL SERVER ERROR**: If there's an error while uploading to Dropbox or processing the request.

  Example response:

  ```json
  {
    "message": "Failed to upload all images."
  }
  ```

### GET /api/get-phone/

#### Request

- **Endpoint**: `/api/get-phone/`
- **Method**: GET
- **Query Parameters**:
  - `phone_number` (string): The phone number to fetch associated images for.

  Example request URL:

  ```
  GET /api/get-phone/?phone_number=1234567890
  ```

#### Response

- **200 OK**: On successful retrieval of images, returns a list of image URLs with filenames.

  Example response:

  ```json
  {
    "phone_number": "1234567890",
    "image_urls": {
      "image1.jpg": "https://www.dropbox.com/s/abcdefg/image1.jpg?raw=1",
      "image2.jpg": "https://www.dropbox.com/s/hijklmn/image2.jpg?raw=1"
    }
  }
  ```

- **400 BAD REQUEST**: If `phone_number` is not provided.

  Example response:

  ```json
  {
    "message": "Phone number is required."
  }
  ```

- **404 NOT FOUND**: If no images are found for the provided phone number.

  Example response:

  ```json
  {
    "message": "No images found for the provided phone number."
  }
  ```

---

## Models

### `Image`

This model stores information about images uploaded to Dropbox.

- **Fields**:
  - `phone_number` (string): The phone number associated with the image.
  - `file_name` (string): The name of the uploaded file.
  - `image_url` (string): The Dropbox URL for accessing the image.
  - `uploaded_at` (datetime): The timestamp when the image was uploaded.

```python
class Image(models.Model):
    phone_number = models.CharField(max_length=15)
    file_name = models.CharField(max_length=255)
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name
```

---

## Admin Panel

To manage images in the Django admin interface:

1. Go to `http://localhost:8000/admin/`
2. Log in with your superuser account.
3. You will see the `Image` model under your app name.
4. You can view, edit, and delete uploaded images.

To enable the Django admin interface, make sure you have the following in `admin.py`:

```python
from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'file_name', 'image_url', 'uploaded_at')
    search_fields = ('phone_number', 'file_name')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)

admin.site.register(Image, ImageAdmin)
```

---

## Environment Variables

To configure the Dropbox API and the Django application, ensure the following environment variables are set:

- **`DROPBOX_APP_KEY`**: Your Dropbox app key (provided by Dropbox when you create the app).
- **`DROPBOX_APP_SECRET`**: Your Dropbox app secret (provided by Dropbox when you create the app).
- **`DROPBOX_REFRESH_TOKEN`**: A long-lived Dropbox refresh token used for generating access tokens.

---

## Running the Project

1. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the API**:

   - **Upload images**: Use `POST /api/upload/` to upload images.
   - **Retrieve image URLs**: Use `GET /api/get-phone/?phone_number=<phone_number>` to fetch image URLs associated with a phone number.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
