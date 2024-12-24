import React, { useState, useEffect, useCallback } from 'react';
import { DocumentFilters } from '../../types';
import { useDocuments } from '../../hooks/useDocuments';

export const DocumentHistory: React.FC = () => {
  const [filters, setFilters] = useState<DocumentFilters>({
    name: '',
    date: '',
    page: 1,
    limit: 10,
    sortBy: 'date',
    sortOrder: 'desc'
  });

  const { documents, loading, error, fetchDocuments, total } = useDocuments();

  useEffect(() => {
    void fetchDocuments(filters);
  }, [fetchDocuments, filters]);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const date = e.target.value;
    if (date && !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      return;
    }
    handleFilterChange({ date });
  };

  const handleFilterChange = useCallback((newFilters: Partial<DocumentFilters>) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters,
      page: 1
    }));
  }, []);

  const handleSort = (column: 'name' | 'date') => {
    setFilters(prev => ({
      ...prev,
      sortBy: column,
      sortOrder: prev.sortBy === column && prev.sortOrder === 'asc' ? 'desc' : 'asc',
      page: 1
    }));
  };

  const getSortIcon = (column: 'name' | 'date') => {
    if (filters.sortBy !== column) return '↕️';
    return filters.sortOrder === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="bg-white shadow-sm rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Document History</h2>
          <p className="mt-1 text-sm text-gray-600">
            View and manage your generated documents.
          </p>
        </div>

        <div className="mb-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700">
                Search by name
              </label>
              <input
                type="text"
                placeholder="Search documents..."
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={filters.name}
                onChange={(e) => handleFilterChange({ name: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                Filter by date
              </label>
              <input
                type="date"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={filters.date}
                onChange={handleDateChange}
                max={new Date().toISOString().split('T')[0]}
              />
            </div>
          </div>
        </div>

        {loading && <div>Loading...</div>}
        {error && <div className="text-red-500">{error}</div>}
        
        {!loading && (!documents || documents.length === 0) && (
          <div className="text-gray-500">No documents found</div>
        )}
        
        {!loading && documents && documents.length > 0 && (
          <div className="mt-8 flex flex-col">
            <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th 
                          scope="col" 
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                          onClick={() => handleSort('name')}
                        >
                          Name {getSortIcon('name')}
                        </th>
                        <th 
                          scope="col" 
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                          onClick={() => handleSort('date')}
                        >
                          Date {getSortIcon('date')}
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Amount
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {documents?.map((doc) => (
                        <tr key={doc.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {new Date(doc.date).toLocaleDateString('en-GB', {
                              day: '2-digit',
                              month: '2-digit',
                              year: 'numeric'
                            }).split('/').join('-')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${doc.amount.toFixed(2)}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {doc.doc_url ? (
                              <a
                                href={doc.doc_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-indigo-600 hover:text-indigo-900"
                                aria-label="View document"
                              >
                                View document
                              </a>
                            ) : (
                              <span className="text-gray-400">No document available</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <div className="mt-4">
                    <p className="text-gray-600">
                      Showing {documents.length} of {total} documents
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}; 