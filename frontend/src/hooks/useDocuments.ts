import { useState, useCallback } from 'react';
import { toast } from 'react-hot-toast';
import { Document, DocumentFilters } from '../types';
import { getDocuments } from '../services/api/document';

interface DocumentsState {
  items: Document[];
  total: number;
  page: number;
  pages: number;
}

export const useDocuments = () => {
  const [documents, setDocuments] = useState<DocumentsState>({
    items: [],
    total: 0,
    page: 1,
    pages: 1
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = useCallback(async (filters?: Partial<DocumentFilters>) => {
    try {
      setLoading(true);
      setError(null);
      
      const requestFilters: DocumentFilters = {
        name: filters?.name ?? '',
        date: filters?.date ?? '',
        page: filters?.page ?? 1,
        limit: filters?.limit ?? 10,
        sortBy: filters?.sortBy,
        sortOrder: filters?.sortOrder
      };

      console.log('Fetching documents with filters:', requestFilters);
      const response = await getDocuments(requestFilters);
      
      if (response.status === 'success' && response.data) {
        setDocuments({
          items: response.data.items || [],
          total: response.data.total || 0,
          page: response.data.page || 1,
          pages: response.data.pages || 1
        });
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (err) {
      console.error('Document fetch error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch documents';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return { 
    documents: documents.items,
    total: documents.total,
    page: documents.page,
    pages: documents.pages,
    loading,
    error,
    fetchDocuments
  };
}; 