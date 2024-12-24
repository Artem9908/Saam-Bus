from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import logging
from ..exceptions import GoogleAPIError
from ..config import SKIP_GOOGLE_AUTH, TESTING
from unittest.mock import Mock

logger = logging.getLogger(__name__)

class GoogleDocsService:
    def __init__(self):
        if TESTING or SKIP_GOOGLE_AUTH:
            # Mocks for testing that can raise errors
            self.docs_service = Mock()
            self.drive_service = Mock()
            
            # Default success response
            mock_doc = {'documentId': 'mock-doc-id'}
            create_mock = Mock()
            create_mock.execute.return_value = mock_doc
            
            # Configure the mock to allow error injection
            self.docs_service.documents.return_value.create.return_value = create_mock
            self.docs_service.documents.return_value.create.side_effect = None  # Can be overridden in tests
        else:
            try:
                cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
                if not cred_path or not os.path.exists(cred_path):
                    raise GoogleAPIError("Google credentials file not found")

                creds = service_account.Credentials.from_service_account_file(cred_path)
                self.docs_service = build('docs', 'v1', credentials=creds)
                self.drive_service = build('drive', 'v3', credentials=creds)
            except Exception as e:
                raise GoogleAPIError(f"Failed to initialize Google services: {str(e)}")

    async def create_document(self, title: str, content: str) -> dict:
        if not self.docs_service:
            raise GoogleAPIError("Docs service not initialized")

        try:
            doc = self.docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            if not doc_id:
                raise GoogleAPIError("Failed to get document ID from response")

            # Do batch update
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }]}
            ).execute()

            # Set permissions, etc.
            self.drive_service.permissions().create(
                fileId=doc_id,
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()

            return {'doc_id': doc_id, 'doc_url': f"https://docs.google.com/document/d/{doc_id}/edit"}

        except Exception as exc:
            logger.error(f"Error creating document: {exc}")
            raise GoogleAPIError(f"Failed to create Google document: {str(exc)}") 