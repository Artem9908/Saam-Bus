const API_URL = process.env.REACT_APP_API_URL;

export const generateDocument = async (formData) => {
  const response = await fetch(`${API_URL}/generate-document`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    throw new Error('Failed to generate document');
  }

  return response.json();
};

export const getDocuments = async (filters = {}) => {
  const queryParams = new URLSearchParams();
  if (filters.name) queryParams.append('name', filters.name);
  if (filters.date) queryParams.append('date', filters.date);

  const response = await fetch(`${API_URL}/documents?${queryParams}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch documents');
  }

  return response.json();
}; 