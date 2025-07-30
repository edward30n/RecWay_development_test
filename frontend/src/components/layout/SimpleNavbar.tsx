import React from 'react';
import { Search, Bell, User } from 'lucide-react';

const SimpleNavbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white shadow-sm">
      <div className="flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-green-500">
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">RecWay</h1>
            <p className="text-xs text-gray-500">Monitoreo Ambiental</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center space-x-6">
          <a href="/" className="text-blue-600 font-medium">Dashboard</a>
          <a href="/sensores" className="text-gray-600 hover:text-blue-600">Sensores</a>
          <a href="/segmentos" className="text-gray-600 hover:text-blue-600">Segmentos</a>
          <a href="/muestras" className="text-gray-600 hover:text-blue-600">Muestras</a>
          <a href="/analisis" className="text-gray-600 hover:text-blue-600">Análisis</a>
        </nav>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="hidden md:flex relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <input
              type="search"
              placeholder="Buscar..."
              className="h-9 w-64 rounded-md border border-gray-300 bg-white pl-9 pr-3 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Notifications */}
          <button className="relative p-2 text-gray-600 hover:text-blue-600">
            <Bell className="h-5 w-5" />
            <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 text-xs text-white flex items-center justify-center">
              3
            </span>
          </button>

          {/* User */}
          <button className="p-2 text-gray-600 hover:text-blue-600">
            <User className="h-5 w-5" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default SimpleNavbar;
