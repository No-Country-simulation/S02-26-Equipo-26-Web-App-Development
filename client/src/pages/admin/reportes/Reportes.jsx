import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import { useState } from 'react';
import './Reportes.css';

export default function ReportesPage({ sidebarCollapsed, toggleSidebar }) {
  return (
    <>
      <Header sidebarCollapsed={sidebarCollapsed} onToggleSidebar={toggleSidebar} />
      <Sidebar collapsed={sidebarCollapsed} />
      
      <div className={`empty-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="empty-page-content">
          <h1 className="empty-page-title">📊 Reportes</h1>
          <p className="empty-page-subtitle">Bienvenido a la sección de Generación de Reportes</p>
          <div className="empty-page-message">
            <p>Esta página está en desarrollo.</p>
            <p>Próximamente podrás:</p>
            <ul>
              <li>Generar reportes estadísticos</li>
              <li>Exportar datos en múltiples formatos</li>
              <li>Crear dashboards personalizados</li>
              <li>Programar reportes automáticos</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}