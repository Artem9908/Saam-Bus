import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { DocumentForm } from './components/document/DocumentForm';
import { DocumentHistory } from './components/document/DocumentHistory';
import { generateDocument } from './services/api/document';
import { DocumentFormData } from './types';
import { toast } from 'react-hot-toast';
import { HomePage } from './components/home/HomePage';
import { AboutPage } from './components/about/AboutPage';
import { ContactForm } from './components/contact/ContactForm';

export const AppRoutes: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = async (data: DocumentFormData) => {
    try {
      const response = await generateDocument(data);
      if (response.status === 'success') {
        navigate('/history');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Error generating document';
      toast.error(message);
      console.error('Error submitting form:', error);
    }
  };

  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/generate" element={<DocumentForm onSubmit={handleSubmit} />} />
      <Route path="/history" element={<DocumentHistory />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/contact" element={<ContactForm />} />
    </Routes>
  );
};