import axios, { AxiosError } from 'axios';
import { Document, DocumentFilters, DocumentFormData, ApiResponse, ErrorResponse } from '../../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const generateDocument = async (data: DocumentFormData): Promise<ApiResponse<Document>> => {
  try {
    console.log('Sending data to API:', data);
    
    const response = await axios.post<ApiResponse<Document>>(`${API_URL}/generate-document`, {
      ...data,
      template_type: data.templateType,
      date: data.date.includes('-') 
        ? data.date.split('-').reverse().join('-')
        : data.date
    });

    return response.data; // Return the response data directly

  } catch (error) {
    console.error('API error:', error);
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw new Error(axiosError.response?.data?.message || 'Failed to generate document');
    }
    throw error;
  }
};

export const getDocuments = async (filters: DocumentFilters): Promise<ApiResponse<{
  items: Document[];
  total: number;
  page: number;
  pages: number;
}>> => {
  try {
    const cleanFilters = {
      ...filters,
      name: filters.name?.trim() || '',
      date: filters.date && /^\d{4}-\d{2}-\d{2}$/.test(filters.date) ? filters.date : '',
      page: filters.page || 1,
      limit: filters.limit || 10
    };

    console.log('Sending filters to API:', cleanFilters); // Debug log

    const response = await axios.get(`${API_URL}/documents`, {
      params: cleanFilters
    });
    
    if (!response.data?.data || typeof response.data.data !== 'object') {
      throw new Error('Invalid response format from server');
    }

    console.log('API Response:', response.data); // Debug log

    return {
      status: 'success',
      data: response.data.data
    };
  } catch (error) {
    console.error('Detailed error:', error);
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ErrorResponse>;
      throw new Error(axiosError.response?.data?.message || 'Failed to fetch documents');
    }
    throw error;
  }
};

export const saveToGoogleDrive = async (docId: string): Promise<ApiResponse<Document>> => {
  try {
    const response = await axios.post<ApiResponse<Document>>(
      `${API_URL}/documents/${docId}/save-to-google`
    );
    
    if (response.data.status === 'error') {
      throw new Error(response.data.message || 'Failed to save to Google Drive');
    }
    
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ErrorResponse>;
      const errorMessage = axiosError.response?.data?.message || 'Failed to save to Google Drive';
      throw new Error(errorMessage);
    }
    throw new Error('Failed to save to Google Drive');
  }
}; 