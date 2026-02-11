import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import { useState, useEffect } from 'react';
import './Documentos.css';

export default function DocumentosPage() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true);
      } else {
        setSidebarCollapsed(false);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <>
      <Header sidebarCollapsed={sidebarCollapsed} onToggleSidebar={toggleSidebar} />
      <Sidebar collapsed={sidebarCollapsed} />
      
      <div className={`empty-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="empty-page-content">
          <h1 className="empty-page-title">📄 Documentos</h1>
          <p className="empty-page-subtitle">Bienvenido a la sección de Gestión de Documentos</p>
          <div className="empty-page-message">
            <p>Esta página está en desarrollo.</p>
            <p>Próximamente podrás:</p>
            <ul>
              <li>Subir y gestionar documentos</li>
              <li>Verificar documentación de cuidadores</li>
              <li>Categorizar archivos por tipo</li>
              <li>Control de versiones</li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}