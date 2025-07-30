import React from 'react';
import { 
  MagnifyingGlassIcon, 
  BellIcon, 
  UserCircleIcon,
  Bars3Icon
} from '@heroicons/react/24/outline';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        {/* Left side - Logo and Brand */}
        <div className="navbar-brand">
          {/* Mobile menu button */}
          <button className="navbar-btn md:hidden">
            <Bars3Icon />
          </button>
          
          {/* Logo and Brand */}
          <div className="navbar-logo">R</div>
          <div>
            <h1 className="navbar-title">RecWay</h1>
            <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Environmental Monitoring</p>
          </div>
        </div>

        {/* Center - Search Bar */}
        <div className="navbar-search">
          <MagnifyingGlassIcon className="navbar-search-icon" />
          <input
            type="text"
            placeholder="Buscar sensores, segmentos..."
          />
        </div>

        {/* Right side - Actions and User */}
        <div className="navbar-actions">
          {/* Search button for mobile */}
          <button className="navbar-btn md:hidden">
            <MagnifyingGlassIcon />
          </button>

          {/* Notifications */}
          <button className="navbar-btn" style={{ position: 'relative' }}>
            <BellIcon />
            <span className="notification-badge"></span>
          </button>

          {/* User Menu */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div className="navbar-logo" style={{ width: '32px', height: '32px' }}>
              <UserCircleIcon style={{ width: '20px', height: '20px' }} />
            </div>
            <div style={{ textAlign: 'left', fontSize: '0.875rem' }}>
              <p style={{ fontWeight: '500', color: '#1f2937' }}>Admin User</p>
              <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Online</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
