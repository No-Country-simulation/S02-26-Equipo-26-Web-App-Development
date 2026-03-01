// src/core/services/authService.js

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// ─── Helpers de tokens ────────────────────────────────────────────────────────

export const getAccessToken  = () => localStorage.getItem('access_token');
export const getRefreshToken = () => localStorage.getItem('refresh_token');

const saveTokens = ({ access, refresh }) => {
  localStorage.setItem('access_token',  access);
  localStorage.setItem('refresh_token', refresh);
};

const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};

const saveUser = (user) =>
  localStorage.setItem('user', JSON.stringify(user));

export const getSavedUser = () => {
  const raw = localStorage.getItem('user');
  return raw ? JSON.parse(raw) : null;
};

// ─── Fetch autenticado (adjunta el JWT y refresca si expira) ──────────────────

export const authFetch = async (url, options = {}) => {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const token = getAccessToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  let response = await fetch(url, { ...options, headers });

  // Si el access token expiró, intentamos refrescarlo una sola vez
  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${getAccessToken()}`;
      response = await fetch(url, { ...options, headers });
    } else {
      clearTokens();
      window.location.href = '/login';
    }
  }

  return response;
};

// ─── Refrescar access token ───────────────────────────────────────────────────

const refreshAccessToken = async () => {
  const refresh = getRefreshToken();
  if (!refresh) return false;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });

    if (!res.ok) return false;

    const data = await res.json();
    localStorage.setItem('access_token', data.access);
    return true;
  } catch {
    return false;
  }
};

// ─── REGISTRO ─────────────────────────────────────────────────────────────────

/**
 * Registra un nuevo usuario.
 *
 * @param {Object} params
 * @param {string} params.firstName
 * @param {string} params.lastName
 * @param {string} params.email
 * @param {string} params.password
 * @param {string} params.passwordConfirm
 * @param {string} params.role  — 'Admin' | 'Caregiver' | 'Patient'
 * @param {number|null} [params.hourlyRate]  — requerido si role === 'Caregiver'
 * @param {string} [params.medicalHistory]   — opcional si role === 'Patient'
 */
export const register = async ({
  firstName,
  lastName,
  email,
  password,
  passwordConfirm,
  role,
  hourlyRate = null,
  medicalHistory = '',
}) => {
  // El backend espera los nombres de campo en snake_case
  const payload = {
    first_name:       firstName,
    last_name:        lastName,
    email,
    password,
    password_confirm: passwordConfirm,
    role,                       // 'Admin' | 'Caregiver' | 'Patient'
    ...(role === 'Caregiver' && { hourly_rate: hourlyRate }),
    ...(role === 'Patient'   && { medical_history: medicalHistory }),
  };

  const res = await fetch(`${API_BASE_URL}/auth/register/`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(payload),
  });

  const data = await res.json();

  if (!res.ok) {
    // El serializer devuelve los errores en data.errors
    throw new Error(formatErrors(data.errors) || data.message || 'Error al registrar');
  }

  // Guardar tokens y datos del usuario
  saveTokens(data.data.tokens);
  saveUser(data.data.user);

  return data.data.user;
};

// ─── LOGIN ────────────────────────────────────────────────────────────────────

/**
 * Autentica un usuario con contraseña.
 */
export const login = async ({ email, password }) => {
  const res = await fetch(`${API_BASE_URL}/auth/login/`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.message || 'Credenciales inválidas');
  }

  saveTokens(data.data.tokens);
  saveUser(data.data.user);

  return data.data.user;
};

// ─── PERFIL ACTUAL ────────────────────────────────────────────────────────────

/**
 * Obtiene el perfil del usuario autenticado desde el servidor.
 */
export const getMe = async () => {
  const res = await authFetch(`${API_BASE_URL}/auth/me/`);
  const data = await res.json();

  if (!res.ok) throw new Error(data.message || 'No se pudo obtener el perfil');

  saveUser(data.data);
  return data.data;
};

// ─── LOGOUT ───────────────────────────────────────────────────────────────────

export const logout = async () => {
  const refresh = getRefreshToken();

  if (refresh) {
    // Intentamos invalidar el token en el servidor (falla en silencio)
    try {
      await authFetch(`${API_BASE_URL}/auth/logout/`, {
        method: 'POST',
        body:   JSON.stringify({ refresh }),
      });
    } catch { /* fallo silencioso */ }
  }

  clearTokens();
};

// ─── Utilidad: formatear errores del serializer ───────────────────────────────

const formatErrors = (errors) => {
  if (!errors || typeof errors !== 'object') return null;

  return Object.entries(errors)
    .map(([field, messages]) => {
      const msg = Array.isArray(messages) ? messages.join(', ') : messages;
      return `${field}: ${msg}`;
    })
    .join(' | ');
};