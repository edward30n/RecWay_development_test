"use client"

import React, { useState } from 'react';
import { 
  MagnifyingGlassIcon, 
  BellIcon, 
  UserCircleIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/button';

const ModernNavbar: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          {/* Logo and Brand */}
          <div className="mr-8 flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-green-500 shadow-lg">
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">RecWay</h1>
              <p className="hidden text-xs text-gray-500 sm:block">Monitoreo Ambiental</p>
            </div>
          </div>

          {/* Navigation Links - Desktop */}
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <a
              href="/"
              className="transition-colors hover:text-blue-600 text-foreground/60 hover:text-foreground/80"
            >
              Dashboard
            </a>
            <a
              href="/sensores"
              className="transition-colors hover:text-blue-600 text-foreground/60 hover:text-foreground/80"
            >
              Sensores
            </a>
            <a
              href="/segmentos"
              className="transition-colors hover:text-blue-600 text-foreground/60 hover:text-foreground/80"
            >
              Segmentos
            </a>
            <a
              href="/muestras"
              className="transition-colors hover:text-blue-600 text-foreground/60 hover:text-foreground/80"
            >
              Muestras
            </a>
            <a
              href="/analisis"
              className="transition-colors hover:text-blue-600 text-foreground/60 hover:text-foreground/80"
            >
              Análisis
            </a>
          </nav>

          {/* Right side - Search and Actions */}
          <div className="flex flex-1 items-center justify-end space-x-4">
            {/* Search Bar - Desktop */}
            <div className="hidden md:flex relative w-full max-w-sm">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
              <input
                type="search"
                placeholder="Buscar sensores, reportes..."
                className="h-9 w-full rounded-md border border-input bg-background pl-9 pr-3 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>

            {/* Action Buttons */}
            <Button variant="ghost" size="icon" className="relative">
              <BellIcon className="h-5 w-5" />
              <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-red-500 text-xs text-white flex items-center justify-center">
                3
              </span>
            </Button>

            <Button variant="ghost" size="icon">
              <UserCircleIcon className="h-5 w-5" />
            </Button>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5" />
              ) : (
                <Bars3Icon className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-white pt-16 md:hidden">
          <div className="container px-4 py-6">
            {/* Mobile Search */}
            <div className="mb-6">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <input
                  type="search"
                  placeholder="Buscar sensores, reportes..."
                  className="h-10 w-full rounded-md border border-input bg-background pl-9 pr-3 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                />
              </div>
            </div>

            {/* Mobile Navigation Links */}
            <nav className="space-y-4">
              {[
                { name: 'Dashboard', href: '/' },
                { name: 'Sensores', href: '/sensores' },
                { name: 'Segmentos', href: '/segmentos' },
                { name: 'Muestras', href: '/muestras' },
                { name: 'Análisis', href: '/analisis' },
                { name: 'Configuración', href: '/configuracion' },
              ].map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="block py-3 text-lg font-medium text-gray-700 hover:text-blue-600"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {item.name}
                </a>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
};

export default ModernNavbar;
