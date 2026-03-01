// src/pages/login/Login.jsx
import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../core/context/AuthContext';
import './Login.css';   // reutiliza o crea estilos similares a Register.css

export default function Login() {
  const [email,     setEmail]     = useState('');
  const [password,  setPassword]  = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error,     setError]     = useState('');
  const [success,   setSuccess]   = useState('');

  const { login, isAuthenticated } = useAuth();
  const navigate  = useNavigate();
  const location  = useLocation();

  // Si ya está autenticado, redirigir
  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  // Mensaje de éxito tras registrarse
  useEffect(() => {
    if (location.state?.registered) {
      setSuccess('¡Cuenta creada! Ahora puedes iniciar sesión.');
    }
  }, [location.state]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      const user = await login({ email, password });

      // Redirigir según el rol
      const roleRoutes = {
        Admin:     '/admin',
        Caregiver: '/caregiver',
        Patient:   '/family',
      };
      navigate(roleRoutes[user.role] || '/dashboard', { replace: true });
    } catch (err) {
      setError(err.message || 'Credenciales inválidas');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">   {/* reusa estilos de Register */}
      <div className="register-card">
        <div className="brand">
          <img src="/logoV3.png" alt="Valora Logo" className="brand-logo" />
          <p>Gestión Integral de Cuidados</p>
        </div>

        <form onSubmit={handleSubmit}>
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
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError(''); }}
                required
                autoFocus
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
                value={password}
                onChange={(e) => { setPassword(e.target.value); setError(''); }}
                required
              />
            </div>
          </div>

          {/* Mensajes */}
          {success && <div className="success-message">{success}</div>}
          {error   && <div className="error-message">{error}</div>}

          {/* Botón */}
          <button type="submit" className="btn-register" disabled={isLoading}>
            {isLoading ? <div className="spinner"></div> : 'Iniciar sesión'}
          </button>

          <div className="login-link">
            ¿No tienes cuenta?{' '}
            <Link to="/register" className="link">
              Registrarse
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}