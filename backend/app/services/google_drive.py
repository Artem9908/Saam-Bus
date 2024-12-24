from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import logging
from ..config import GOOGLE_CREDENTIALS_PATH, GOOGLE_DRIVE_FOLDER_ID, TESTING, SKIP_GOOGLE_AUTH
from ..exceptions import GoogleAPIError
import os
from unittest.mock import Mock

logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self):
        if TESTING or SKIP_GOOGLE_AUTH:
            self.service = Mock()
            mock_file = {'id': 'mock-id', 'webViewLink': 'https://drive.google.com/mock-id'}
            create_mock = Mock()
            create_mock.execute.return_value = mock_file
            self.service.files.return_value.create.return_value = create_mock
        else:
            try:
                if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
                    raise FileNotFoundError(f"Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}")

                self.credentials = service_account.Credentials.from_service_account_file(
                    GOOGLE_CREDENTIALS_PATH,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
                self.service = build('drive', 'v3', credentials=self.credentials)
                logger.info("Successfully initialized Google Drive service")
            except Exception as e:
                logger.error(f"Failed to initialize Google Drive service: {e}")
                raise GoogleAPIError(f"Failed to initialize Google Drive service: {str(e)}")

    async def upload_document(self, content: str, filename: str, mime_type: str = None) -> dict:
        """
        Upload a document to Google Drive
        Args:
            content: Document content
            filename: Name of the file
            mime_type: MIME type of the file (optional)
        Returns:
            dict with doc_id and doc_url
        """
        try:
            file_metadata = {'name': filename}
            if GOOGLE_DRIVE_FOLDER_ID:
                file_metadata['parents'] = [GOOGLE_DRIVE_FOLDER_ID]

            # Determine MIME type
            if not mime_type:
                mime_type = 'application/vnd.google-apps.document'
                if filename.endswith('.txt'):
                    mime_type = 'text/plain'
                elif filename.endswith('.pdf'):
                    mime_type = 'application/pdf'
            
            media = MediaIoBaseUpload(
                BytesIO(content.encode()),
                mimetype=mime_type,
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink',
                supportsAllDrives=True
            ).execute()

            # Set file permissions to anyone with link can view
            self.service.permissions().create(
                fileId=file.get('id'),
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()

            return {
                'doc_id': file.get('id'),
                'doc_url': file.get('webViewLink')
            }
        except Exception as e:
            logger.error(f"Error uploading to Google Drive: {e}")
            raise GoogleAPIError(f"Failed to upload document: {str(e)}")

    async def delete_document(self, doc_id: str) -> None:
        """Delete a document from Google Drive"""
        try:
            self.service.files().delete(fileId=doc_id).execute()
        except Exception as e:
            logger.error(f"Error deleting from Google Drive: {e}")
            raise GoogleAPIError(f"Failed to delete document: {str(e)}")