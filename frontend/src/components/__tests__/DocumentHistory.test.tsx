import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { DocumentHistory } from '../document/DocumentHistory';
import { getDocuments } from '../../services/api/document';

vi.mock('../../services/api/document', () => ({
  getDocuments: vi.fn().mockResolvedValue({
    status: 'success',
    data: {
      items: [],
      total: 0,
      page: 1,
      pages: 1
    }
  })
}));

describe('DocumentHistory', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch documents on mount', async () => {
    render(<DocumentHistory />);
    
    await waitFor(() => {
      expect(getDocuments).toHaveBeenCalledWith({
        name: '',
        date: '',
        page: 1,
        limit: 10
      });
    });
  });
}); 