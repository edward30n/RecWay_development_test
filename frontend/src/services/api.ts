import axios from 'axios';

// Configuración base de axios
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Servicios genéricos para CRUD
export const apiService = {
  // GET - Obtener todos los elementos
  getAll: (endpoint: string) => api.get(`/api/v1/${endpoint}`),
  
  // GET - Obtener elemento por ID
  getById: (endpoint: string, id: number) => api.get(`/api/v1/${endpoint}/${id}`),
  
  // POST - Crear nuevo elemento
  create: (endpoint: string, data: any) => api.post(`/api/v1/${endpoint}`, data),
  
  // PUT - Actualizar elemento
  update: (endpoint: string, id: number, data: any) => api.put(`/api/v1/${endpoint}/${id}`, data),
  
  // DELETE - Eliminar elemento
  delete: (endpoint: string, id: number) => api.delete(`/api/v1/${endpoint}/${id}`),
  
  // GET - Buscar con parámetros
  search: (endpoint: string, params: any) => api.get(`/api/v1/${endpoint}`, { params }),
};

export default api;
