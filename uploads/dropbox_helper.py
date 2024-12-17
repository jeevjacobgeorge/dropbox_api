import requests
import dropbox
from dotenv import load_dotenv, set_key
import os
from urllib.parse import quote_plus
# Load environment variables from .env file
load_dotenv()

# Dropbox API URL for refreshing the access token
TOKEN_URL = 'https://api.dropbox.com/oauth2/token'

def update_refresh_token_in_env(new_refresh_token):
    """Update the REFRESH_TOKEN in the .env file."""
    env_file = '.env'  # Path to your .env file

    # Update the REFRESH_TOKEN in the .env file
    set_key(env_file, 'DROPBOX_REFRESH_TOKEN', new_refresh_token)
    
    # Reload environment variables to reflect the change
    load_dotenv()

def get_new_access_token(refresh_token):
    """Use the refresh token to get a new access token."""
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv("APP_KEY"),
        'client_secret': os.getenv("APP_SECRET"),
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        
        # If a new refresh token is returned, update it in the .env file
        if 'refresh_token' in tokens:
            new_refresh_token = tokens['refresh_token']
            print(f"Refresh token has been updated: {new_refresh_token}")
            update_refresh_token_in_env(new_refresh_token)  # Save the new refresh token
            
        return access_token
    else:
        print(f"Error refreshing token: {response.text}")
        return None

def upload_to_dropbox(file_path, filename):
    """Upload a file to Dropbox and return the shared URL."""
    access_token = get_new_access_token(os.getenv("REFRESH_TOKEN"))
    if access_token is None:
        return None

    dbx = dropbox.Dropbox(access_token)
    
    try:
        with open(file_path, 'rb') as file:
            # Upload the file to Dropbox
            upload_response = dbx.files_upload(file.read(), f'/images/{filename}', mute=True)
        
        # Fetch the shared URL of the uploaded file
        image_url = get_image_from_dropbox(filename)
        
        return {"message": f"File '{filename}' uploaded successfully to Dropbox", "image_url": image_url}
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def get_image_from_dropbox(filename):
    """Fetch the image from Dropbox by filename."""
    access_token = get_new_access_token(os.getenv("REFRESH_TOKEN"))
    if access_token is None:
        return None

    dbx = dropbox.Dropbox(access_token)
    
    try:
        # Check if there's already a shared link for this file
        file_path = f'/images/{filename}'
        result = dbx.sharing_list_shared_links(path=file_path)
        
        # If the link exists, use it
        if result.links:
            image_url = result.links[0].url.replace('dl=0', 'raw=1')  # Convert to raw URL
        
        else:
            # If no shared link exists, create one
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
            image_url = shared_link_metadata.url.replace('dl=0', 'raw=1')  # Convert to raw URL
        
        return image_url
    
    except dropbox.exceptions.ApiError as e:
        print(f"Error retrieving image: {e}")
        return None

def get_images_from_dropbox(phone_number):
    """Fetch image URLs from Dropbox based on phone_number."""
    encoded_phone_number = quote_plus(phone_number)
    
    access_token = get_new_access_token(os.getenv("REFRESH_TOKEN"))
    if access_token is None:
        return {"message": "Failed to get access token."}

    dbx = dropbox.Dropbox(access_token)

    folder_path = f"/images/{encoded_phone_number}"
    
    try:
        # List files in the folder
        result = dbx.files_list_folder(f'{folder_path}')
        
        # Store the URLs for the images with the file name as the key
        file_urls = {}
        
        # Loop through files in the folder
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                # Use sharing_list_shared_links to get an existing shared link
                shared_links_result = dbx.sharing_list_shared_links(path=entry.path_display)
                
                # If a shared link exists, use it
                if shared_links_result.links:
                    image_url = shared_links_result.links[0].url.replace('dl=0', 'raw=1')  # Change 'dl=0' to 'raw=1' to get the raw image
                else:
                    # If no shared link exists, create a new shared link
                    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(entry.path_display)
                    image_url = shared_link_metadata.url.replace('dl=0', 'raw=1')
                
                # Use the file name as the key
                file_urls[entry.name] = image_url

        # Return the URLs of the images
        if file_urls:
            return {"message": "Images retrieved successfully", "file_urls": file_urls}
        else:
            return {"message": "No images found in the folder."}
    
    except dropbox.exceptions.ApiError as e:
        print(f"Error fetching files from Dropbox: {e}")
        return {"message": f"Error fetching files from Dropbox: {e}"}
