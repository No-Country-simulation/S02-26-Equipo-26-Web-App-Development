import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';

export default function Register() {
  // Estados del formulario
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState('patient');
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  // Validación de contraseñas
  const validatePasswords = () => {
    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return false;
    }
    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return false;
    }
    return true;
  };

  // Manejador del submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validar contraseñas
    if (!validatePasswords()) {
      return;
    }

    // Validar términos y condiciones
    if (!acceptTerms) {
      setError('Debes aceptar los términos y condiciones');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Aquí irá tu lógica de registro
      // Ejemplo: await authService.register(name, email, password, selectedRole);
      
      console.log('Register data:', { name, email, password, selectedRole });
      
      // Simular carga (eliminar en producción)
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Redirigir al login después de registrarse
      navigate('/login');
      
    } catch (err) {
      console.error('Register error:', err);
      setError(err.message || 'Error al registrar usuario');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <div className="brand">
          <img 
            src="/logoV3.png" 
            alt="Valora Logo" 
            className="brand-logo" 
          />
          <p>Gestión Integral de Cuidados</p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Campo: Nombre completo */}
          <div className="form-group">
            <label htmlFor="name">Nombre completo</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">person</span>
              <input
                type="text"
                id="name"
                placeholder="Juan Pérez"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Campo: Email */}
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">email</span>
              <input
                type="email"
                id="email"
                placeholder="nombre@empresa.com"
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Campo: Contraseña */}
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">lock</span>
              <input
                type="password"
                id="password"
                placeholder="••••••••"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Campo: Confirmar contraseña */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirmar contraseña</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">lock</span>
              <input
                type="password"
                id="confirmPassword"
                placeholder="••••••••"
                className="form-control"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Campo: Rol */}
          <div className="form-group">
            <label htmlFor="role">Registrarse como</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">badge</span>
              <select
                id="role"
                className="form-control"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                <option value="admin">Administrador</option>
                <option value="caregiver">Acompañante / Cuidador</option>
                <option value="patient">Paciente / Familia</option>
              </select>
            </div>
          </div>

          {/* Términos y condiciones */}
          <div className="form-group terms">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={acceptTerms}
                onChange={(e) => setAcceptTerms(e.target.checked)}
              />
              <span>Acepto los <a href="#" className="terms-link">términos y condiciones</a></span>
            </label>
          </div>

          {/* Mensaje de error */}
          {error && <div className="error-message">{error}</div>}

          {/* Botón de registro */}
          <button 
            type="submit" 
            className="btn-register" 
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="spinner"></div>
            ) : (
              'Crear cuenta'
            )}
          </button>

          {/* Enlace a login */}
          <div className="login-link">
            ¿Ya tienes cuenta? <Link to="/login" className="link">Iniciar sesión</Link>
          </div>
        </form>
      </div>
    </div>
  );
}