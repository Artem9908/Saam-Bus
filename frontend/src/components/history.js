import React, { useEffect, useState } from 'react';
import './history.css';

function History() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    const fetchDocuments = async () => {
      const response = await fetch('http://localhost:8000/documents');
      const data = await response.json();
      setDocuments(data);
    };

    fetchDocuments();
  }, []);

  return (
    <div className="history-container">
      <h1>Document History</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Content</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc) => (
            <tr key={doc.id}>
              <td>{doc.name}</td>
              <td>{doc.date}</td>
              <td>${doc.amount}</td>
              <td>
                <button onClick={() => alert(doc.content)}>View</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default History; 