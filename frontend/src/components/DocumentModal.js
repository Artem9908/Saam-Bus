import React from 'react';
import PropTypes from 'prop-types';
import './DocumentModal.css';

function DocumentModal({ document, onClose }) {
  if (!document) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Document Details</h2>
        <div className="document-info">
          <p><strong>Name:</strong> {document.name}</p>
          <p><strong>Date:</strong> {document.date}</p>
          <p><strong>Amount:</strong> ${document.amount}</p>
        </div>
        <div className="document-content">
          <pre>{document.content}</pre>
        </div>
        {document.drive_link && (
          <a 
            href={document.drive_link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="drive-link"
          >
            View in Google Drive
          </a>
        )}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

DocumentModal.propTypes = {
  document: PropTypes.shape({
    name: PropTypes.string,
    date: PropTypes.string,
    amount: PropTypes.number,
    content: PropTypes.string,
    drive_link: PropTypes.string
  }),
  onClose: PropTypes.func.isRequired
};

export default DocumentModal; 