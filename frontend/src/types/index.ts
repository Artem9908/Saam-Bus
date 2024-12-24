// Move all types here from services/api/types.ts
export interface DocumentFilters {
    name?: string;
    date?: string;
    page: number;
    limit: number;
    sortBy?: 'name' | 'date';
    sortOrder?: 'asc' | 'desc';
  }
  
  export interface Document {
    id: number;
    name: string;
    date: string;
    amount: number;
    template_type: string;
    content: string;
    doc_url?: string;
    doc_id?: string;
    google_doc_id?: string;
    created_at: string;
    updated_at?: string;
  }
  
  export interface DocumentFormData {
    name: string;
    date: string;
    amount: number;
    templateType: 'receipt' | 'invoice' | 'contract';
  }
  
  export interface ApiResponse<T> {
    status: 'success' | 'error';
    data: T;
    message?: string;
  }
  
  export interface ErrorResponse {
    status: 'error';
    message: string;
    type?: string;
  }