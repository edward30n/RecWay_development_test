import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

// Tipos para el contexto de autenticación
interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Crear el contexto
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider del contexto
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Verificar token al cargar la aplicación
  useEffect(() => {
    const savedToken = localStorage.getItem('recway_token');
    const savedUser = localStorage.getItem('recway_user');
    
    if (savedToken && savedUser) {
      try {
        const parsedUser = JSON.parse(savedUser);
        setToken(savedToken);
        setUser(parsedUser);
      } catch (error) {
        // Si hay error al parsear, limpiar localStorage
        localStorage.removeItem('recway_token');
        localStorage.removeItem('recway_user');
      }
    }
    
    setIsLoading(false);
  }, []);

  // Función de login (simulada)
  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    
    try {
      // Simulación de llamada a API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Credenciales de prueba
      if (email === 'admin@recway.com' && password === 'admin123') {
        const mockUser: User = {
          id: '1',
          email: 'admin@recway.com',
          name: 'Administrador RecWay'
        };
        
        const mockToken = 'recway_token_' + Date.now();
        
        // Guardar en localStorage
        localStorage.setItem('recway_token', mockToken);
        localStorage.setItem('recway_user', JSON.stringify(mockUser));
        
        // Actualizar estado
        setToken(mockToken);
        setUser(mockUser);
        setIsLoading(false);
        
        return true;
      } else {
        setIsLoading(false);
        return false;
      }
    } catch (error) {
      setIsLoading(false);
      return false;
    }
  };

  // Función de logout
  const logout = () => {
    localStorage.removeItem('recway_token');
    localStorage.removeItem('recway_user');
    setToken(null);
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!token && !!user,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook para usar el contexto
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
