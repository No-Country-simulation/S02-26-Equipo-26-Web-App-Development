import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
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
import { useState } from 'react';

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
      {/* Rutas sin sidebar */}
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Rutas con sidebar */}
      {requiresSidebar && (
        <>
          <Route 
            path="/admin" 
            element={
              <AdminDashboard 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/cuidadores" 
            element={
              <CuidadoresPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/pacientes" 
            element={
              <PacientesPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/pagos" 
            element={
              <PagosPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/documentos" 
            element={
              <DocumentosPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/reportes" 
            element={
              <ReportesPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/admin/configuracion" 
            element={
              <ConfiguracionPage 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/caregiver" 
            element={
              <CaregiverDashboard 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
          <Route 
            path="/family" 
            element={
              <FamilyDashboard 
                sidebarCollapsed={sidebarCollapsed} 
                toggleSidebar={toggleSidebar} 
              /> 
            } 
          />
        </>
      )}
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}