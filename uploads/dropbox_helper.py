# dropbox_helper.py
import requests
import dropbox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dropbox API URL for refreshing the access token
TOKEN_URL = 'https://api.dropbox.com/oauth2/token'

def get_new_access_token(refresh_token):
    """Use the refresh token to get a new access token."""
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': APP_KEY,
        'client_secret': APP_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        return access_token
    else:
        print(f"Error refreshing token: {response.text}")
        return None

def upload_to_dropbox(file_path, filename):
    """Upload a file to Dropbox."""
    access_token = get_new_access_token(REFRESH_TOKEN)
    if access_token is None:
        return None

    dbx = dropbox.Dropbox(access_token)
    
    try:
        # Open the file and upload to Dropbox (in the 'images' folder)
        with open(file_path, 'rb') as file:
            dbx.files_upload(file.read(), f'/images/{filename}', mute=True)
        
        return f"File '{filename}' uploaded successfully to Dropbox"
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def get_image_from_dropbox(filename):
    """Fetch the image from Dropbox by filename."""
    access_token = get_new_access_token(REFRESH_TOKEN)
    if access_token is None:
        return None

    dbx = dropbox.Dropbox(access_token)
    
    try:
        # Get the shared link of the file
        file_path = f'/images/{filename}'
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
        
        # Extract the public URL
        image_url = shared_link_metadata.url.replace('dl=0', 'raw=1')  # Change 'dl=0' to 'raw=1' to get the image directly
        
        return image_url
    
    except dropbox.exceptions.ApiError as e:
        print(f"Error retrieving image: {e}")
        return None
