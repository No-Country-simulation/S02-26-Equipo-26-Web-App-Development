// src/pages/register/Register.jsx
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register } from '../../core/services/authService';
import './Register.css';

// Mapa frontend (value del select) → valor que espera el backend
const ROLE_MAP = {
  admin:     'Admin',
  caregiver: 'Caregiver',
  patient:   'Patient',
};

export default function Register() {
  const [form, setForm] = useState({
    fullName:        '',
    email:           '',
    password:        '',
    confirmPassword: '',
    role:            'patient',
    hourlyRate:      '',     // solo Caregiver
  });
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [isLoading,   setIsLoading]   = useState(false);
  const [error,       setError]       = useState('');

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setForm((prev) => ({ ...prev, [id]: value }));
    setError('');
  };

  const validate = () => {
    if (form.password !== form.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return false;
    }
    if (form.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return false;
    }
    if (!acceptTerms) {
      setError('Debes aceptar los términos y condiciones');
      return false;
    }
    if (form.role === 'caregiver' && !form.hourlyRate) {
      setError('Debes indicar tu tarifa por hora');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    // Separar nombre completo en first_name / last_name
    const [firstName = '', ...rest] = form.fullName.trim().split(' ');
    const lastName = rest.join(' ') || firstName; // fallback si solo hay un nombre

    setIsLoading(true);
    setError('');

    try {
      await register({
        firstName,
        lastName,
        email:           form.email,
        password:        form.password,
        passwordConfirm: form.confirmPassword,
        role:            ROLE_MAP[form.role],
        hourlyRate:      form.role === 'caregiver' ? parseFloat(form.hourlyRate) : null,
      });

      // Registro exitoso → ir al dashboard o login
      navigate('/login', { state: { registered: true } });
    } catch (err) {
      setError(err.message || 'Error al registrar usuario');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="brand">
          <img src="/logoV3.png" alt="Valora Logo" className="brand-logo" />
          <p>Gestión Integral de Cuidados</p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Nombre completo */}
          <div className="form-group">
            <label htmlFor="fullName">Nombre completo</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">person</span>
              <input
                type="text"
                id="fullName"
                placeholder="Juan Pérez"
                className="form-control"
                value={form.fullName}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Email */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">email</span>
              <input
                type="email"
                id="email"
                placeholder="nombre@empresa.com"
                className="form-control"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Contraseña */}
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">lock</span>
              <input
                type="password"
                id="password"
                placeholder="••••••••"
                className="form-control"
                value={form.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Confirmar contraseña */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmar contraseña</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">lock</span>
              <input
                type="password"
                id="confirmPassword"
                placeholder="••••••••"
                className="form-control"
                value={form.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Rol */}
          <div className="form-group">
            <label htmlFor="role">Registrarse como</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">badge</span>
              <select
                id="role"
                className="form-control"
                value={form.role}
                onChange={handleChange}
              >
                <option value="admin">Administrador</option>
                <option value="caregiver">Acompañante / Cuidador</option>
                <option value="patient">Paciente / Familia</option>
              </select>
            </div>
          </div>

          {/* Tarifa por hora (solo Caregiver) */}
          {form.role === 'caregiver' && (
            <div className="form-group">
              <label htmlFor="hourlyRate">Tarifa por hora (USD)</label>
              <div className="input-wrapper">
                <span className="material-icons input-icon">attach_money</span>
                <input
                  type="number"
                  id="hourlyRate"
                  placeholder="15.00"
                  min="1"
                  step="0.01"
                  className="form-control"
                  value={form.hourlyRate}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          )}

          {/* Términos */}
          <div className="form-group terms">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={acceptTerms}
                onChange={(e) => setAcceptTerms(e.target.checked)}
              />
              <span>
                Acepto los{' '}
                <a href="#" className="terms-link">
                  términos y condiciones
                </a>
              </span>
            </label>
          </div>

          {/* Error */}
          {error && <div className="error-message">{error}</div>}

          {/* Botón */}
          <button type="submit" className="btn-register" disabled={isLoading}>
            {isLoading ? <div className="spinner"></div> : 'Crear cuenta'}
          </button>

          <div className="login-link">
            ¿Ya tienes cuenta?{' '}
            <Link to="/login" className="link">
              Iniciar sesión
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}