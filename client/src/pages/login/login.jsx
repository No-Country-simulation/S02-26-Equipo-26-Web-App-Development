import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  // ✅ Estados corregidos (incluyendo error)
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState('admin');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(''); // ✅ Estado error añadido
  const navigate = useNavigate();

  // Manejador del submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(''); // ✅ Ahora funciona porque error está declarado

    // ✅ 1. Primero define el mapping de roles
    const roleToRoute = {
      admin: '/admin',
      caregiver: '/caregiver',
      patient: '/family'
    };

    // ✅ 2. Luego valida
    if (!roleToRoute[selectedRole]) {
      setError('Rol no válido');
      setIsLoading(false);
      return;
    }

    try {
      console.log('Login ', { email, password, selectedRole });
      
      // Simular llamada a API
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // ✅ 3. Finalmente redirige
      navigate(roleToRoute[selectedRole]);
      
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="brand">
          <img 
            src="/logoV3.png" 
            alt="Valora Logo" 
            className="brand-logo" 
          />
          <p>Gestión Integral de Cuidados</p>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Mensaje de error */}
          {error && <div className="error-message">{error}</div>}

          {/* Campo: Usuario / Email */}
          <div className="form-group">
            <label htmlFor="email">Usuario / Email</label>
            <div className="input-wrapper">
              <span className="material-icons input-icon">person</span>
              <input
                type="text"
                id="email"
                placeholder="nombre@empresa.com"
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="off"
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

          {/* Campo: Rol */}
          <div className="form-group">
            <label htmlFor="role">Ingresar como</label>
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

          {/* Acciones */}
          <div className="actions">
            <a href="#" className="forgot-pass">
              ¿Olvidaste tu contraseña?
            </a>
          </div>

          {/* Botón de login */}
          <button 
            type="submit" 
            className="btn-login" 
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="spinner"></div>
            ) : (
              'Ingresar'
            )}
          </button>
        </form>
      </div>
    </div>
  );
}