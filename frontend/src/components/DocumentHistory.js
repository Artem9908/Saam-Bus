import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { getDocuments } from '../services/api';

function DocumentHistory() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    name: '',
    date: ''
  });

  const fetchDocuments = useCallback(async () => {
    try {
      const data = await getDocuments(filters);
      setDocuments(data);
    } catch (error) {
      toast.error('Error fetching documents: ' + error.message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4">Document History</h2>
          
          {/* Filters */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">Filter by Name</label>
              <input
                type="text"
                name="name"
                value={filters.name}
                onChange={handleFilterChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="Enter name..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Filter by Date</label>
              <input
                type="date"
                name="date"
                value={filters.date}
                onChange={handleFilterChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* Documents Table */}
          {loading ? (
            <div className="text-center py-4">Loading...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {documents.map((doc) => (
                    <tr key={doc.id}>
                      <td className="px-6 py-4 whitespace-nowrap">{doc.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{formatDate(doc.date)}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{formatAmount(doc.amount)}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {doc.doc_url ? (
                          <a
                            href={doc.doc_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-indigo-600 hover:text-indigo-900"
                          >
                            View Document
                          </a>
                        ) : (
                          <span className="text-gray-400">No document link</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {documents.length === 0 && (
                <div className="text-center py-4 text-gray-500">
                  No documents found
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DocumentHistory; 