import api from './api';
import type { Segmento, SegmentoCreate, Geometria, PaginatedResponse } from '../types';

export const segmentosService = {
  // Obtener todos los segmentos
  getAll: async (): Promise<Segmento[]> => {
    const response = await api.get<Segmento[]>('/segmentos/');
    return response.data;
  },

  // Obtener segmento por ID
  getById: async (id: number): Promise<Segmento> => {
    const response = await api.get<Segmento>(`/segmentos/${id}`);
    return response.data;
  },

  // Crear nuevo segmento
  create: async (segmento: SegmentoCreate): Promise<Segmento> => {
    const response = await api.post<Segmento>('/segmentos/', segmento);
    return response.data;
  },

  // Actualizar segmento
  update: async (id: number, segmento: Partial<SegmentoCreate>): Promise<Segmento> => {
    const response = await api.put<Segmento>(`/segmentos/${id}`, segmento);
    return response.data;
  },

  // Eliminar segmento
  delete: async (id: number): Promise<void> => {
    await api.delete(`/segmentos/${id}`);
  },

  // Obtener geometría de un segmento
  getGeometria: async (segmentoId: number): Promise<Geometria[]> => {
    const response = await api.get<Geometria[]>(`/segmentos/${segmentoId}/geometria`);
    return response.data;
  },

  // Buscar segmentos con paginación
  search: async (params: {
    skip?: number;
    limit?: number;
    search?: string;
  }): Promise<PaginatedResponse<Segmento>> => {
    const response = await api.get<PaginatedResponse<Segmento>>('/segmentos/search', {
      params,
    });
    return response.data;
  },
};
