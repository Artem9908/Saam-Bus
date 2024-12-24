import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DocumentForm } from '../document/DocumentForm';
import { generateDocument } from '../../services/api/document';

vi.mock('../../services/api/document', () => ({
  generateDocument: vi.fn()
}));

describe('DocumentForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
    vi.mocked(generateDocument).mockResolvedValue({
      status: 'success',
      data: {
        id: 1,
        name: 'Test Document',
        date: '2024-01-01',
        amount: 100,
        content: 'Test content'
      },
      message: 'Document generated successfully'
    });
  });

  it('renders all form fields', () => {
    render(<DocumentForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/template type/i)).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    render(<DocumentForm onSubmit={mockOnSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/name/i), {
      target: { value: 'Test Document' }
    });
    fireEvent.change(screen.getByLabelText(/date/i), {
      target: { value: '2024-01-01' }
    });
    fireEvent.change(screen.getByLabelText(/amount/i), {
      target: { value: '100' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /generate document/i }));
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        name: 'Test Document',
        date: '2024-01-01',
        amount: 100,
        templateType: 'receipt'
      });
    });
  });

  it('validates required fields', () => {
    render(<DocumentForm onSubmit={mockOnSubmit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /generate document/i }));
    
    expect(screen.getByLabelText(/name/i)).toBeInvalid();
    expect(screen.getByLabelText(/date/i)).toBeInvalid();
    expect(screen.getByLabelText(/amount/i)).toBeInvalid();
  });
  
  it('validates amount minimum value', () => {
    render(<DocumentForm onSubmit={mockOnSubmit} />);
    
    const amountInput = screen.getByLabelText(/amount/i);
    fireEvent.change(amountInput, { target: { value: '-1' } });
    
    expect(amountInput).toBeInvalid();
  });
});