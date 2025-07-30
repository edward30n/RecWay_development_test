import api from './api';
import type { Muestra, MuestraCreate, PaginatedResponse } from '../types';

export const muestrasService = {
  // Obtener todas las muestras
  getAll: async (): Promise<Muestra[]> => {
    const response = await api.get<Muestra[]>('/muestras/');
    return response.data;
  },

  // Obtener muestra por ID
  getById: async (id: number): Promise<Muestra> => {
    const response = await api.get<Muestra>(`/muestras/${id}`);
    return response.data;
  },

  // Crear nueva muestra
  create: async (muestra: MuestraCreate): Promise<Muestra> => {
    const response = await api.post<Muestra>('/muestras/', muestra);
    return response.data;
  },

  // Actualizar muestra
  update: async (id: number, muestra: Partial<MuestraCreate>): Promise<Muestra> => {
    const response = await api.put<Muestra>(`/muestras/${id}`, muestra);
    return response.data;
  },

  // Eliminar muestra
  delete: async (id: number): Promise<void> => {
    await api.delete(`/muestras/${id}`);
  },

  // Obtener muestras por segmento
  getBySegmento: async (segmentoId: number): Promise<Muestra[]> => {
    const response = await api.get<Muestra[]>(`/muestras/segmento/${segmentoId}`);
    return response.data;
  },

  // Obtener muestras por sensor
  getBySensor: async (sensorId: number): Promise<Muestra[]> => {
    const response = await api.get<Muestra[]>(`/muestras/sensor/${sensorId}`);
    return response.data;
  },

  // Buscar muestras con filtros
  search: async (params: {
    skip?: number;
    limit?: number;
    sensor_id?: number;
    segmento_id?: number;
    fecha_inicio?: string;
    fecha_fin?: string;
  }): Promise<PaginatedResponse<Muestra>> => {
    const response = await api.get<PaginatedResponse<Muestra>>('/muestras/search', {
      params,
    });
    return response.data;
  },
};
