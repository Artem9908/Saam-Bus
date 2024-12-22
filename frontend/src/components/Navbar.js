import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  return (
    <nav className="bg-indigo-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-white font-bold">Document Generator</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to="/"
                  className={`${
                    location.pathname === '/'
                      ? 'bg-indigo-700 text-white'
                      : 'text-white hover:bg-indigo-500'
                  } px-3 py-2 rounded-md text-sm font-medium`}
                >
                  Generate Document
                </Link>
                <Link
                  to="/history"
                  className={`${
                    location.pathname === '/history'
                      ? 'bg-indigo-700 text-white'
                      : 'text-white hover:bg-indigo-500'
                  } px-3 py-2 rounded-md text-sm font-medium`}
                >
                  History
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 