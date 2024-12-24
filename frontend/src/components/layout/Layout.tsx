import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const isActive = (path: string) => 
    location.pathname === path ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-50';

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link to="/" className="text-xl font-bold text-indigo-600">
                  AI-Docs
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-4">
                <Link
                  to="/"
                  className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium ${isActive('/')}`}
                >
                  Home
                </Link>
                <Link
                  to="/generate"
                  className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium ${isActive('/generate')}`}
                >
                  Generate
                </Link>
                <Link
                  to="/history"
                  className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium ${isActive('/history')}`}
                >
                  History
                </Link>
                <Link
                  to="/about"
                  className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium ${isActive('/about')}`}
                >
                  About
                </Link>
                <Link
                  to="/contact"
                  className={`inline-flex items-center px-3 py-2 rounded-md text-sm font-medium ${isActive('/contact')}`}
                >
                  Contact
                </Link>
              </div>
            </div>

            <div className="sm:hidden flex items-center">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
              >
                <span className="sr-only">Open main menu</span>
                <svg
                  className="h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={isMobileMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {isMobileMenuOpen && (
          <div className="sm:hidden">
            <div className="pt-2 pb-3 space-y-1">
              <Link
                to="/"
                className={`block px-3 py-2 text-base font-medium ${isActive('/')}`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/generate"
                className={`block px-3 py-2 text-base font-medium ${isActive('/generate')}`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Generate
              </Link>
              <Link
                to="/history"
                className={`block px-3 py-2 text-base font-medium ${isActive('/history')}`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                History
              </Link>
              <Link
                to="/about"
                className={`block px-3 py-2 text-base font-medium ${isActive('/about')}`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                About
              </Link>
              <Link
                to="/contact"
                className={`block px-3 py-2 text-base font-medium ${isActive('/contact')}`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Contact
              </Link>
            </div>
          </div>
        )}
      </nav>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 sm:px-0">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}; 