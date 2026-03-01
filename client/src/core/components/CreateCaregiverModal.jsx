// client/src/core/components/CreateCaregiverModal.jsx
import { useState, useEffect } from 'react';
import { caregiverService } from '../services/caregiverService';
import './CreateCaregiverModal.css';

export default function CreateCaregiverModal({ isOpen, onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    password: '',
    hourly_rate: '',
    specialty_id: '',
    bank_account: '',
  });
  const [specialties, setSpecialties] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isLoadingSpecialties, setIsLoadingSpecialties] = useState(true);

  useEffect(() => {
    if (isOpen) {
      loadSpecialties();
    }
  }, [isOpen]);

  const loadSpecialties = async () => {
    try {
      setIsLoadingSpecialties(true);
      const data = await caregiverService.getSpecialties();
      setSpecialties(data);
    } catch (err) {
      console.error('Error cargando especialidades:', err);
    } finally {
      setIsLoadingSpecialties(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const validateForm = () => {
    if (!formData.first_name || !formData.last_name) {
      setError('Nombre y apellido son obligatorios');
      return false;
    }
    if (!formData.email.includes('@')) {
      setError('Email inválido');
      return false;
    }
    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return false;
    }
    if (!formData.hourly_rate || parseFloat(formData.hourly_rate) <= 0) {
      setError('Tarifa por hora inválida');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsLoading(true);
    setError('');

    try {
      await caregiverService.create({
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        phone_number: formData.phone_number,
        password: formData.password,
        hourly_rate: parseFloat(formData.hourly_rate),
        specialty_id: formData.specialty_id ? parseInt(formData.specialty_id) : null,
        bank_account: formData.bank_account,
      });

      // Limpiar formulario
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        password: '',
        hourly_rate: '',
        specialty_id: '',
        bank_account: '',
      });

      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message || 'Error al crear cuidador');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Nuevo Cuidador</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">Nombre *</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                placeholder="Juan"
              />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Apellido *</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                placeholder="Pérez"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="cuidador@test.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña temporal *</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Mínimo 6 caracteres"
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone_number">Teléfono</label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              placeholder="+54 9 11 5555-1234"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="specialty_id">Especialidad</label>
              <select
                id="specialty_id"
                name="specialty_id"
                value={formData.specialty_id}
                onChange={handleChange}
                disabled={isLoadingSpecialties}
              >
                <option value="">Seleccionar...</option>
                {specialties.map(spec => (
                  <option key={spec.id} value={spec.id}>{spec.name}</option>
                ))}
              </select>
              {isLoadingSpecialties && <span className="loading-text">Cargando...</span>}
            </div>
            <div className="form-group">
              <label htmlFor="hourly_rate">Tarifa/hora (USD) *</label>
              <input
                type="number"
                id="hourly_rate"
                name="hourly_rate"
                value={formData.hourly_rate}
                onChange={handleChange}
                required
                min="1"
                step="0.01"
                placeholder="15.00"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="bank_account">Cuenta bancaria</label>
            <input
              type="text"
              id="bank_account"
              name="bank_account"
              value={formData.bank_account}
              onChange={handleChange}
              placeholder="CBU o número de cuenta"
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary" disabled={isLoading}>
              {isLoading ? 'Creando...' : 'Crear Cuidador'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}