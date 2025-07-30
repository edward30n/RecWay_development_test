import React, { useState } from 'react';
import { PlusIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useSensores } from '../../hooks/useSensores';

const Sensores: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const { data: sensores, isLoading, error } = useSensores();

  const filteredSensores = sensores?.filter(sensor =>
    sensor.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sensor.descripcion?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-recway-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border-red-200">
        <p className="text-red-800">Error al cargar los sensores</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Sensores</h1>
          <p className="mt-1 text-sm text-gray-500">
            Gestión de sensores del sistema RecWay
          </p>
        </div>
        <button className="btn-primary flex items-center">
          <PlusIcon className="h-5 w-5 mr-2" />
          Nuevo Sensor
        </button>
      </div>

      {/* Search Bar */}
      <div className="card">
        <div className="relative">
          <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar sensores..."
            className="input-field pl-10 w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Sensors Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="table-header">ID</th>
                <th className="table-header">Nombre</th>
                <th className="table-header">Tipo</th>
                <th className="table-header">Ubicación</th>
                <th className="table-header">Estado</th>
                <th className="table-header">Última Actualización</th>
                <th className="table-header">Acciones</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredSensores?.map((sensor) => (
                <tr key={sensor.id_sensor} className="hover:bg-gray-50">
                  <td className="table-cell font-mono text-sm">
                    {sensor.id_sensor}
                  </td>
                  <td className="table-cell">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {sensor.nombre}
                      </div>
                      {sensor.descripcion && (
                        <div className="text-sm text-gray-500">
                          {sensor.descripcion}
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="table-cell">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {sensor.tipo_sensor || 'No especificado'}
                    </span>
                  </td>
                  <td className="table-cell">
                    <div className="text-sm text-gray-900">
                      {sensor.ubicacion || 'No especificada'}
                    </div>
                    {sensor.latitud && sensor.longitud && (
                      <div className="text-xs text-gray-500">
                        {sensor.latitud.toFixed(6)}, {sensor.longitud.toFixed(6)}
                      </div>
                    )}
                  </td>
                  <td className="table-cell">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        sensor.estado === 'activo'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {sensor.estado || 'Desconocido'}
                    </span>
                  </td>
                  <td className="table-cell text-sm text-gray-500">
                    {sensor.fecha_instalacion || 'No disponible'}
                  </td>
                  <td className="table-cell">
                    <div className="flex space-x-2">
                      <button className="text-recway-600 hover:text-recway-900 text-sm">
                        Ver
                      </button>
                      <button className="text-gray-600 hover:text-gray-900 text-sm">
                        Editar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Empty State */}
        {(!filteredSensores || filteredSensores.length === 0) && (
          <div className="text-center py-12">
            <div className="w-24 h-24 mx-auto mb-4 text-gray-400">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">
              No se encontraron sensores
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              {searchTerm ? 'Intenta con otros términos de búsqueda' : 'Comienza agregando tu primer sensor'}
            </p>
            <button className="btn-primary">
              <PlusIcon className="h-5 w-5 mr-2" />
              Agregar Sensor
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sensores;
