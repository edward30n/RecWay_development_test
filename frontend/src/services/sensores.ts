import api from './api';
import type { Sensor, SensorCreate, PaginatedResponse } from '../types';

export const sensoresService = {
  // Obtener todos los sensores
  getAll: async (): Promise<Sensor[]> => {
    const response = await api.get<Sensor[]>('/sensores/');
    return response.data;
  },

  // Obtener sensor por ID
  getById: async (id: number): Promise<Sensor> => {
    const response = await api.get<Sensor>(`/sensores/${id}`);
    return response.data;
  },

  // Crear nuevo sensor
  create: async (sensor: SensorCreate): Promise<Sensor> => {
    const response = await api.post<Sensor>('/sensores/', sensor);
    return response.data;
  },

  // Actualizar sensor
  update: async (id: number, sensor: Partial<SensorCreate>): Promise<Sensor> => {
    const response = await api.put<Sensor>(`/sensores/${id}`, sensor);
    return response.data;
  },

  // Eliminar sensor
  delete: async (id: number): Promise<void> => {
    await api.delete(`/sensores/${id}`);
  },

  // Buscar sensores con paginación
  search: async (params: {
    skip?: number;
    limit?: number;
    search?: string;
  }): Promise<PaginatedResponse<Sensor>> => {
    const response = await api.get<PaginatedResponse<Sensor>>('/sensores/search', {
      params,
    });
    return response.data;
  },
};
