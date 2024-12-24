import React, { useState } from 'react';
import { DocumentFormData } from '../../types';
import { toast } from 'react-hot-toast';

interface DocumentFormProps {
  onSubmit: (data: DocumentFormData) => void;
  isLoading?: boolean;
}

export const DocumentForm: React.FC<DocumentFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<DocumentFormData>({
    name: '',
    date: '',
    amount: 0,
    templateType: 'receipt'
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof DocumentFormData, string>>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof DocumentFormData, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.date) {
      newErrors.date = 'Date is required';
    } else if (!/^\d{4}-\d{2}-\d{2}$/.test(formData.date)) {
      newErrors.date = 'Invalid date format. Use YYYY-MM-DD';
    }

    if (formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm() || isLoading) {
      return;
    }

    try {
      const dateParts = formData.date.split('-');
      const apiFormattedDate = dateParts.length === 3 
        ? `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`
        : formData.date;

      const submitData = {
        ...formData,
        date: apiFormattedDate
      };

      await onSubmit(submitData);
      toast.success('Document generated successfully');
      
      // Reset form after successful submission
      setFormData({
        name: '',
        date: '',
        amount: 0,
        templateType: 'receipt'
      });
    } catch (error) {
      console.error('Form submission error:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to submit form');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    if (name === 'amount') {
      setFormData(prev => ({
        ...prev,
        [name]: parseFloat(value) || 0
      }));
      return;
    }

    // For date, keep the input value as is until form submission
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="bg-white shadow-sm rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Generate New Document</h2>
          <p className="mt-1 text-sm text-gray-600">
            Fill in the details below to generate a new document.
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6 max-w-3xl">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Document Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.name}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                Date
              </label>
              <input
                type="date"
                id="date"
                name="date"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.date}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
                Amount
              </label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-500 sm:text-sm">$</span>
                </div>
                <input
                  type="number"
                  id="amount"
                  name="amount"
                  required
                  min="0.01"
                  step="0.01"
                  className="pl-7 block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  value={formData.amount || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div>
              <label htmlFor="templateType" className="block text-sm font-medium text-gray-700">
                Template Type
              </label>
              <select
                id="templateType"
                name="templateType"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                value={formData.templateType}
                onChange={handleChange}
              >
                <option value="receipt">Receipt</option>
                <option value="invoice">Invoice</option>
                <option value="contract">Contract</option>
              </select>
            </div>
          </div>

          <div className="pt-5">
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400"
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </>
                ) : (
                  'Generate Document'
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DocumentForm; 