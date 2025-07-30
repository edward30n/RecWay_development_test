import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  HomeIcon,
  MapIcon,
  ChartBarIcon,
  CpuChipIcon,
  ClipboardDocumentListIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Segmentos', href: '/segmentos', icon: MapIcon },
  { name: 'Sensores', href: '/sensores', icon: CpuChipIcon },
  { name: 'Muestras', href: '/muestras', icon: ClipboardDocumentListIcon },
  { name: 'Análisis', href: '/analisis', icon: ChartBarIcon },
  { name: 'Configuración', href: '/configuracion', icon: Cog6ToothIcon },
];

const Sidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-content">
        <nav className="sidebar-nav">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `sidebar-link ${isActive ? 'active' : ''}`
              }
            >
              <item.icon />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
        
        {/* Divider */}
        <div className="sidebar-divider"></div>
        
        {/* Status indicator */}
        <div className="sidebar-status">
          <div className="sidebar-status-indicator">
            <div className="sidebar-status-dot"></div>
            <span className="sidebar-status-text">Sistema Activo</span>
          </div>
          <p className="sidebar-status-detail">Todos los sensores operativos</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
