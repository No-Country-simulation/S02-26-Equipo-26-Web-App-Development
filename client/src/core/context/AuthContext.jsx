// src/core/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { login as loginService, logout as logoutService, getMe, getSavedUser } from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user,    setUser]    = useState(getSavedUser); // carga rápida desde localStorage
  const [loading, setLoading] = useState(true);         // cargando perfil desde servidor

  // Al montar: verificar que el token sigue siendo válido
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setLoading(false);
      return;
    }

    getMe()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async ({ email, password }) => {
    const userData = await loginService({ email, password });
    setUser(userData);
    return userData;
  }, []);

  const logout = useCallback(async () => {
    await logoutService();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook para consumir el contexto
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de <AuthProvider>');
  return ctx;
};