import React from 'react';
import { Outlet } from 'react-router-dom';
import RecWayNavigation from './RecWayNavigation';
import './RecWayNavigation.css';

const Layout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* RecWay Navigation */}
      <RecWayNavigation 
        logoText="RecWay"
        onAccountClick={() => window.location.href = '/login'}
      />
      
      {/* Main Content - Sin sidebar por ahora */}
      <main className="p-6 pt-20">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
