import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import { useState } from 'react';
import './Configuracion.css';

export default function ConfiguracionPage({ sidebarCollapsed, toggleSidebar }) {
  return (
    <>
      <Header sidebarCollapsed={sidebarCollapsed} onToggleSidebar={toggleSidebar} />
      <Sidebar collapsed={sidebarCollapsed} />
      
      <div className={`empty-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="empty-page-content">
          <h1 className="empty-page-title">⚙️ Configuración</h1>
          <p className="empty-page-subtitle">Bienvenido a la sección de Configuración del Sistema</p>
          <div className="empty-page-message">
            <p>Esta página está en desarrollo.</p>
            <p>Próximamente podrás:</p>
            <ul>
              <li>Configurar parámetros del sistema</li>
              <li>Gestionar usuarios y permisos</li>
              <li>Ajustar preferencias generales</li>
              <li>Administrar integraciones</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}