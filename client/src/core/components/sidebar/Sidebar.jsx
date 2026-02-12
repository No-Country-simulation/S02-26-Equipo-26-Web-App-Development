import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

export default function Sidebar({ collapsed }) {
  const location = useLocation();
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  // Menús principales (sin "Configuración")
  const mainMenuItems = [
    { label: "Dashboard", icon: "dashboard", route: "/admin" },
    { label: "Cuidadores", icon: "people", route: "/admin/cuidadores" },
    { label: "Pacientes", icon: "groups", route: "/admin/pacientes" },
    { label: "Pagos", icon: "payments", route: "/admin/pagos" },
    { label: "Documentos", icon: "description", route: "/admin/documentos" },
    { label: "Reportes", icon: "assessment", route: "/admin/reportes" }
  ];

  // Menús al final (Configuración + Cerrar sesión)
  const bottomMenuItems = [
    { label: "Configuración", icon: "settings", route: "/admin/configuracion" },
    { label: "Cerrar sesión", icon: "logout", route: "/logout" }
  ];

  // Manejar redimensionamiento
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth < 768) {
        setCollapsed(true);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, [collapsed]);

  return (
    <div className={`sidebar-container ${collapsed ? 'collapsed' : ''}`}>
      {/* Contenido del sidebar */}
      <div className="sidebar-content">
        {/* Logo */}
        <div className="sidebar-logo">
          <img src="/logoV3.png" alt="Valora" className="logo-img" />
          {!collapsed && <span className="logo-text">Valora</span>}
        </div>

        {/* Menú principal */}
        <nav className="main-menu">
          {mainMenuItems.map((item, index) => (
            <Link
              key={index}
              to={item.route}
              className={`menu-item ${location.pathname === item.route ? 'active' : ''}`}
            >
              <span className="menu-icon">
                <span className="material-icons">{item.icon}</span>
              </span>
              {!collapsed && <span className="menu-label">{item.label}</span>}
            </Link>
          ))}
        </nav>
      </div>

      {/* Menú al final (Configuración + Cerrar sesión) */}
      <div className="sidebar-bottom">
        {bottomMenuItems.map((item, index) => (
          <Link
            key={index}
            to={item.route}
            className={`menu-item ${location.pathname === item.route ? 'active' : ''}`}
          >
            <span className="menu-icon">
              <span className="material-icons">{item.icon}</span>
            </span>
            {!collapsed && <span className="menu-label">{item.label}</span>}
          </Link>
        ))}
      </div>
    </div>
  );
}