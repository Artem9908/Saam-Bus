// src/components/about/AboutPage.tsx
import React from 'react';

export const AboutPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">About AI-Docs Automation</h1>
      
      <div className="prose prose-indigo">
        <p className="text-lg text-gray-700 mb-6">
          AI-Docs Automation is a powerful document generation and management system
          that helps businesses streamline their document workflows.
        </p>
        
        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Our Features</h2>
        <ul className="list-disc pl-6 space-y-2 text-gray-700">
          <li>Automated document generation</li>
          <li>Google Drive integration</li>
          <li>Custom templates</li>
          <li>Document history tracking</li>
        </ul>
      </div>
    </div>
  );
};