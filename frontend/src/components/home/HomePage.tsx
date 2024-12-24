// src/components/home/HomePage.tsx
import React from 'react';
import { Link } from 'react-router-dom';

export const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-indigo-600 mb-2">AI-Docs Automation</h1>
          <p className="text-gray-600">Streamline your document workflows</p>
        </div>

        {/* Main Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <Link to="/generate" 
                className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Create Document</h2>
            <p className="text-gray-600">Generate professional documents automatically</p>
          </Link>
          
          <Link to="/history" 
                className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Google Docs Integration</h2>
            <p className="text-gray-600">Work with your documents in Google Docs</p>
          </Link>
        </div>

        {/* Additional Navigation */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/about" 
                className="text-center p-4 text-indigo-600 hover:text-indigo-800">
            About Us
          </Link>
          <Link to="/contact" 
                className="text-center p-4 text-indigo-600 hover:text-indigo-800">
            Contact Us
          </Link>
        </div>
      </div>
    </div>
  );
};