from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
from ..config import SKIP_GOOGLE_AUTH

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

class GoogleDocsService:
    def __init__(self):
        self.docs_service = None
        self.drive_service = None
        
        if not SKIP_GOOGLE_AUTH:
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    'credentials.json', scopes=SCOPES
                )
                self.docs_service = build('docs', 'v1', credentials=credentials)
                self.drive_service = build('drive', 'v3', credentials=credentials)
            except Exception as e:
                print(f"Failed to initialize Google services: {e}")

    def create_document(self, title: str, content: str):
        if SKIP_GOOGLE_AUTH:
            return "mock-doc-id-123"
            
        try:
            if not self.docs_service:
                return None
                
            document = self.docs_service.documents().create(
                body={"title": title}
            ).execute()

            self.docs_service.documents().batchUpdate(
                documentId=document.get('documentId'),
                body={
                    'requests': [{
                        'insertText': {
                            'location': {
                                'index': 1
                            },
                            'text': content
                        }
                    }]
                }
            ).execute()

            return document.get('documentId')
        except Exception as e:
            print(f"Error creating document: {e}")
            return None 