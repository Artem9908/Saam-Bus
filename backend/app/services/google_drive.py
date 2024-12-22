import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import StringIO
from ..config import TESTING

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveService:
    def __init__(self):
        self.credentials = None
        self.service = None
        # Only authenticate if not in testing or development mode
        if not TESTING and not os.getenv('DEVELOPMENT_MODE') == 'true':
            self._authenticate()

    def _authenticate(self):
        try:
            # Load credentials from file if exists
            if os.path.exists('token.json'):
                self.credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

            # If no valid credentials, authenticate
            if not self.credentials or not self.credentials.valid:
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.credentials = flow.run_local_server(port=0)
                    
                    # Save credentials
                    with open('token.json', 'w') as token:
                        token.write(self.credentials.to_json())
                else:
                    raise Exception("No credentials.json file found")

            self.service = build('drive', 'v3', credentials=self.credentials)
        except Exception as e:
            print(f"Authentication failed: {e}")
            # Don't raise exception in constructor

    def upload_document(self, content: str, filename: str) -> str:
        # Return mock link in testing or development mode
        if TESTING or os.getenv('DEVELOPMENT_MODE') == 'true':
            return f"http://mock-drive-link.com/{filename}"

        try:
            if not self.service:
                return None

            # Create file metadata
            file_metadata = {'name': filename}

            # Create file content
            file_content = StringIO(content)
            media = MediaIoBaseUpload(
                file_content,
                mimetype='text/plain',
                resumable=True
            )

            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            return file.get('webViewLink')

        except Exception as e:
            print(f"Error uploading to Google Drive: {str(e)}")
            return None