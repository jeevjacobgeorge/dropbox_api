

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

Certainly! Here's a `README.md` file for React developers, explaining how to integrate the frontend with the Django API, including the creation of forms and how to interact with the API.

---

# React Frontend Integration with Image Upload API

This document guides React developers on how to create forms and interact with the Django API for image upload and retrieval of image URLs associated with a phone number. You will learn how to send requests to the API, handle file uploads, and display images dynamically on the frontend.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting up React Project](#setting-up-react-project)
3. [Creating the Upload Form](#creating-the-upload-form)
4. [Uploading Images](#uploading-images)
5. [Fetching Image URLs](#fetching-image-urls)
6. [Handling API Responses](#handling-api-responses)
7. [Error Handling](#error-handling)
8. [Styling the UI](#styling-the-ui)

---

## Prerequisites

Before proceeding, ensure you have the following:

- **Node.js** (>= 14.x)
- **npm** or **yarn** for package management
- A running Django API (as per the instructions in the [Backend README](#backend-readme))

Ensure that your React application can communicate with the Django API. You may want to set the API URL in a `.env` file to avoid hardcoding URLs.

---

## Setting up React Project

1. **Create a new React app** (if not already created):

   ```bash
   npx create-react-app image-upload
   cd image-upload
   ```

2. **Install Axios** to make HTTP requests:

   ```bash
   npm install axios
   ```

3. **Create a `.env` file** for the API base URL:

   ```plaintext
   REACT_APP_API_URL=http://localhost:8000/api
   ```

---

## Creating the Upload Form

In the React app, create a form to upload images and provide a field for entering the `phone_number`. The form will send the selected images to the Django API.

1. **Create `UploadForm.js`** in `src/components/`:

   ```jsx
   import React, { useState } from 'react';
   import axios from 'axios';

   const UploadForm = () => {
     const [phoneNumber, setPhoneNumber] = useState('');
     const [images, setImages] = useState([]);
     const [isUploading, setIsUploading] = useState(false);
     const [uploadResults, setUploadResults] = useState([]);

     const handlePhoneNumberChange = (e) => {
       setPhoneNumber(e.target.value);
     };

     const handleImageChange = (e) => {
       setImages(e.target.files);
     };

     const handleSubmit = async (e) => {
       e.preventDefault();
       setIsUploading(true);

       const formData = new FormData();
       formData.append('phone_number', phoneNumber);
       Array.from(images).forEach((image) => {
         formData.append('images', image);
       });

       try {
         const response = await axios.post(`${process.env.REACT_APP_API_URL}/upload/`, formData, {
           headers: {
             'Content-Type': 'multipart/form-data',
           },
         });

         setUploadResults(response.data.results);
       } catch (error) {
         console.error('Error uploading images:', error);
       } finally {
         setIsUploading(false);
       }
     };

     return (
       <div>
         <h2>Upload Images</h2>
         <form onSubmit={handleSubmit}>
           <div>
             <label>Phone Number:</label>
             <input
               type="text"
               value={phoneNumber}
               onChange={handlePhoneNumberChange}
               required
             />
           </div>
           <div>
             <label>Upload Images:</label>
             <input
               type="file"
               multiple
               onChange={handleImageChange}
               required
             />
           </div>
           <button type="submit" disabled={isUploading}>
             {isUploading ? 'Uploading...' : 'Upload'}
           </button>
         </form>

         {uploadResults.length > 0 && (
           <div>
             <h3>Upload Results:</h3>
             <ul>
               {uploadResults.map((result, index) => (
                 <li key={index}>
                   <strong>{result.filename}</strong>: {result.message}
                   <br />
                   {result.image_url && (
                     <a href={result.image_url} target="_blank" rel="noopener noreferrer">
                       View Image
                     </a>
                   )}
                 </li>
               ))}
             </ul>
           </div>
         )}
       </div>
     );
   };

   export default UploadForm;
   ```

   ### Explanation:
   - `phoneNumber`: Holds the phone number entered by the user.
   - `images`: Holds the selected image files.
   - `handlePhoneNumberChange`: Handles the change in the phone number input.
   - `handleImageChange`: Handles the selection of files.
   - `handleSubmit`: Creates a `FormData` object to send the phone number and images as a `multipart/form-data` request to the API.

---

## Uploading Images

The `handleSubmit` function in the `UploadForm.js` handles sending the images to the backend API using **Axios**.

- We use **FormData** to package the phone number and images as a multipart form.
- When the form is submitted, a `POST` request is sent to the Django API (`/api/upload/`).
- The images are uploaded and, if successful, the image URLs are returned and displayed.

---

## Fetching Image URLs

Create another component to retrieve and display image URLs for a given phone number.

1. **Create `ImageList.js`** in `src/components/`:

   ```jsx
   import React, { useState } from 'react';
   import axios from 'axios';

   const ImageList = () => {
     const [phoneNumber, setPhoneNumber] = useState('');
     const [imageUrls, setImageUrls] = useState([]);
     const [loading, setLoading] = useState(false);
     const [error, setError] = useState('');

     const handlePhoneNumberChange = (e) => {
       setPhoneNumber(e.target.value);
     };

     const fetchImages = async () => {
       setLoading(true);
       setError('');
       try {
         const response = await axios.get(`${process.env.REACT_APP_API_URL}/get-phone/`, {
           params: { phone_number: phoneNumber },
         });

         setImageUrls(response.data.image_urls);
       } catch (error) {
         setError('Failed to retrieve images.');
       } finally {
         setLoading(false);
       }
     };

     return (
       <div>
         <h2>View Uploaded Images</h2>
         <input
           type="text"
           placeholder="Enter phone number"
           value={phoneNumber}
           onChange={handlePhoneNumberChange}
         />
         <button onClick={fetchImages} disabled={loading}>
           {loading ? 'Loading...' : 'Fetch Images'}
         </button>

         {error && <p style={{ color: 'red' }}>{error}</p>}

         {imageUrls.length > 0 && (
           <div>
             <h3>Images:</h3>
             <ul>
               {Object.keys(imageUrls).map((filename) => (
                 <li key={filename}>
                   <strong>{filename}</strong>: 
                   <a href={imageUrls[filename]} target="_blank" rel="noopener noreferrer">
                     View Image
                   </a>
                 </li>
               ))}
             </ul>
           </div>
         )}
       </div>
     );
   };

   export default ImageList;
   ```

### Explanation:
- `fetchImages`: Sends a GET request to `/api/get-phone/` to fetch image URLs for a given phone number.
- The URLs are displayed with a "View Image" link for each file.

---

## Handling API Responses

Both the upload and image-fetching requests will return different responses:

### Upload:
- On success, the response contains the `filename`, `message`, and `image_url` for each uploaded file.
- On error, an appropriate error message will be shown.

### Fetching Images:
- On success, the image URLs are displayed as links to the images.
- On error, an error message is shown indicating that the images couldn't be retrieved.

---

## Error Handling

To handle errors gracefully, ensure that your frontend displays appropriate messages in case of failure. For instance, you can show error messages for invalid inputs or failed requests:

```jsx
try {
  const response = await axios.post(url, data);
} catch (error) {
  setError("There was an error with your request.");
}
```

---

## Styling the UI

You can style the components using plain CSS or frameworks like **Material-UI** or **Bootstrap**. Here's an example of some basic styles you can apply to the form:

```css
form {
  max-width: 500px;
  margin: auto;
}

input[type="text"], input[type="file"] {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
}

button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
```

---

## Conclusion

You now have a React frontend that integrates with the Django API for uploading images and fetching URLs. You can
