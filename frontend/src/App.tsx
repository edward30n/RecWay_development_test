import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import HomePage from './pages/HomePage';
// Importar los módulos de autenticación adaptados para React Router
import LoginPage from './pages/auth/LoginPage';
import SignupPage from './pages/auth/SignupPage';
import ForgotPasswordPage from './pages/auth/ForgotPasswordPage';

// Crear cliente de React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Rutas de autenticación (sin layout) */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          
          {/* Ruta para homepage sin layout */}
          <Route path="/home" element={<HomePage />} />
          
          {/* Rutas con layout para dashboard */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="sensores" element={<div className="p-6">Sensores - En desarrollo</div>} />
            <Route path="segmentos" element={<div className="p-6">Segmentos - En desarrollo</div>} />
            <Route path="muestras" element={<div className="p-6">Muestras - En desarrollo</div>} />
            <Route path="analisis" element={<div className="p-6">Análisis - En desarrollo</div>} />
            <Route path="configuracion" element={<div className="p-6">Configuración - En desarrollo</div>} />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
