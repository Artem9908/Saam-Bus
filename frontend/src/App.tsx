import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { AppRoutes } from './routes';
import { Toaster } from 'react-hot-toast';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <AppRoutes />
        <Toaster position="top-right" />
      </Layout>
    </Router>
  );
};

export default App;