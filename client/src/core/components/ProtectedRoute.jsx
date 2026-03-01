// src/core/components/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * Protege rutas privadas.
 * 
 * Uso:
 *   <Route path="/admin" element={<ProtectedRoute roles={['Admin']}><AdminPage /></ProtectedRoute>} />
 * 
 * Si `roles` está vacío o no se pasa, cualquier usuario autenticado puede acceder.
 */
export default function ProtectedRoute({ children, roles = [] }) {
  const { user, loading } = useAuth();

  // Mientras verifica el token, no renderizar nada (evita flash de login)
  if (loading) return null;

  // No autenticado → redirigir al login
  if (!user) return <Navigate to="/login" replace />;

  // Rol no permitido → redirigir al inicio
  if (roles.length > 0 && !roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}