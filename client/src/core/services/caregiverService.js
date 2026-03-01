// client/src/core/services/caregiverService.js
import { authFetch } from './authService';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const caregiverService = {
  // Listar todos los cuidadores (para el dashboard)
  async getAll() {
    const response = await authFetch(`${API_BASE_URL}/caregivers/`);
    if (!response.ok) throw new Error('Error al cargar cuidadores');
    return response.json();
  },

  // Obtener especialidades disponibles
  async getSpecialties() {
    const response = await authFetch(`${API_BASE_URL}/caregivers/specialties/`);
    if (!response.ok) throw new Error('Error al cargar especialidades');
    return response.json();
  },

  // Crear nuevo cuidador (solo Admin)
  async create(caregiverData) {
    const response = await authFetch(`${API_BASE_URL}/caregivers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caregiverData),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || error.error || 'Error al crear cuidador');
    }
    
    return response.json();
  },

  // Ver detalle de un cuidador
  async getById(userId) {
    const response = await authFetch(`${API_BASE_URL}/caregivers/${userId}/`);
    if (!response.ok) throw new Error('Error al cargar cuidador');
    return response.json();
  },

  // Actualizar cuidador
  async update(userId, data) {
    const response = await authFetch(`${API_BASE_URL}/caregivers/${userId}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Error al actualizar cuidador');
    return response.json();
  },
};