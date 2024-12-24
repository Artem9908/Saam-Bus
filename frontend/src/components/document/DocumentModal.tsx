import React, { useState } from 'react';
import { saveToGoogleDrive } from '../../services/api/document';
import { toast } from 'react-toastify';
import { Document } from '../../types';

interface Props {
  document: Document;
  onClose: () => void;
  onUpdate?: (updatedDoc: Document) => void;
}

const DocumentModal: React.FC<Props> = ({ document, onClose, onUpdate }) => {
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveToGoogle = async () => {
    if (!document.doc_id) return;
    
    try {
      setIsSaving(true);
      const response = await saveToGoogleDrive(document.doc_id);
      if (onUpdate && response.data) {
        onUpdate(response.data);
      }
      toast.success('Document saved to Google Drive');
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to save to Google Drive');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg max-w-2xl w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Document Details</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            ✕
          </button>
        </div>
        
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold">Name</h3>
            <p>{document.name}</p>
          </div>
          
          <div>
            <h3 className="font-semibold">Date</h3>
            <p>{new Date(document.date).toLocaleDateString()}</p>
          </div>
          
          <div>
            <h3 className="font-semibold">Amount</h3>
            <p>{new Intl.NumberFormat('en-US', {
              style: 'currency',
              currency: 'USD'
            }).format(document.amount)}</p>
          </div>
          
          <div>
            <h3 className="font-semibold">Content</h3>
            <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded">
              {document.content}
            </pre>
          </div>
        </div>
        
        <div className="mt-6 flex justify-end space-x-2">
          {!document.google_doc_id && (
            <button
              onClick={handleSaveToGoogle}
              disabled={isSaving}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
            >
              {isSaving ? 'Saving...' : 'Save to Google Drive'}
            </button>
          )}
          {document.doc_url && (
            <a
              href={document.doc_url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Open in Google Drive
            </a>
          )}
          <button
            onClick={onClose}
            className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default DocumentModal; 