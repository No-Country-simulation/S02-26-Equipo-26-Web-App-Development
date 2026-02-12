import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import { useState } from 'react';
import './Pacientes.css';

export default function PacientesPage({ sidebarCollapsed, toggleSidebar }) {
  return (
    <>
      <Header sidebarCollapsed={sidebarCollapsed} onToggleSidebar={toggleSidebar} />
      <Sidebar collapsed={sidebarCollapsed} />
      
      <div className={`empty-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="empty-page-content">
          <h1 className="empty-page-title">🏥 Pacientes</h1>
          <p className="empty-page-subtitle">Bienvenido a la sección de Gestión de Pacientes</p>
          <div className="empty-page-message">
            <p>Esta página está en desarrollo.</p>
            <p>Próximamente podrás:</p>
            <ul>
              <li>Registrar nuevos pacientes</li>
              <li>Ver historial médico</li>
              <li>Gestionar asignaciones de cuidadores</li>
              <li>Seguimiento de tratamientos</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}