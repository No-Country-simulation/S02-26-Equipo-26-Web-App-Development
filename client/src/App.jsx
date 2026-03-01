// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useState } from 'react';

import { AuthProvider } from './core/context/AuthContext';
import ProtectedRoute from './core/components/ProtectedRoute';

import Login from './pages/login/Login';
import Register from './pages/register/Register';

import AdminDashboard from './pages/admin/AdminDashboard'; 
import CaregiverDashboard from './pages/caregiver/CaregiverDashboard';
import FamilyDashboard from './pages/family/FamilyDashboard';

import CuidadoresPage from './pages/admin/cuidadores/Cuidadores';
import PacientesPage from './pages/admin/pacientes/pacientes';
import PagosPage from './pages/admin/pagos/pagos';
import DocumentosPage from './pages/admin/documentos/documentos';
import ReportesPage from './pages/admin/reportes/Reportes';
import ConfiguracionPage from './pages/admin/Configuracion/configuracion';

function AppContent() {
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  // Verificar si la ruta actual requiere sidebar
  const requiresSidebar = location.pathname.startsWith('/admin') || 
                         location.pathname.startsWith('/caregiver') || 
                         location.pathname.startsWith('/family');

  return (
    <Routes>
      {/* Rutas públicas (sin sidebar) */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Rutas protegidas con sidebar */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={['Admin']}>
            <AdminDashboard 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/cuidadores"
        element={
          <ProtectedRoute roles={['Admin']}>
            <CuidadoresPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/pacientes"
        element={
          <ProtectedRoute roles={['Admin']}>
            <PacientesPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/pagos"
        element={
          <ProtectedRoute roles={['Admin']}>
            <PagosPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/documentos"
        element={
          <ProtectedRoute roles={['Admin']}>
            <DocumentosPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/reportes"
        element={
          <ProtectedRoute roles={['Admin']}>
            <ReportesPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/configuracion"
        element={
          <ProtectedRoute roles={['Admin']}>
            <ConfiguracionPage 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/caregiver"
        element={
          <ProtectedRoute roles={['Caregiver']}>
            <CaregiverDashboard 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />
      <Route
        path="/family"
        element={
          <ProtectedRoute roles={['Patient']}>
            <FamilyDashboard 
              sidebarCollapsed={sidebarCollapsed} 
              toggleSidebar={toggleSidebar} 
            />
          </ProtectedRoute>
        }
      />

      {/* Ruta por defecto */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>  {/* ← ESTO FALTABA - envuelve toda la app */}
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}