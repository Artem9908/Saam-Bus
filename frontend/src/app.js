import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import DocumentForm from './components/DocumentForm';
import DocumentHistory from './components/DocumentHistory';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex space-x-7">
                <div className="flex items-center space-x-4">
                  <Link to="/" className="text-gray-800 hover:text-gray-600 px-3 py-2 rounded-md">
                    Generate Document
                  </Link>
                  <Link to="/history" className="text-gray-800 hover:text-gray-600 px-3 py-2 rounded-md">
                    History
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<DocumentForm />} />
            <Route path="/history" element={<DocumentHistory />} />
          </Routes>
        </div>
      </div>
      <ToastContainer position="bottom-right" />
    </Router>
  );
}

export default App;