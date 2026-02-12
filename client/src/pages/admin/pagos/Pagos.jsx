import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import { useState } from 'react';
import './Pagos.css';

export default function PagosPage({ sidebarCollapsed, toggleSidebar }) {
  return (
    <>
      <Header sidebarCollapsed={sidebarCollapsed} onToggleSidebar={toggleSidebar} />
      <Sidebar collapsed={sidebarCollapsed} />
      
      <div className={`empty-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="empty-page-content">
          <h1 className="empty-page-title">💳 Pagos</h1>
          <p className="empty-page-subtitle">Bienvenido a la sección de Gestión de Pagos</p>
          <div className="empty-page-message">
            <p>Esta página está en desarrollo.</p>
            <p>Próximamente podrás:</p>
            <ul>
              <li>Registrar pagos de cuidadores</li>
              <li>Ver historial de transacciones</li>
              <li>Generar reportes financieros</li>
              <li>Gestionar facturación</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}