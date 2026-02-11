import './Sidebar.css';

export default function Sidebar({ collapsed }) {
  // Definir los ítems del menú con sus iconos
  const menuItems = [
    { label: 'Dashboard', icon: 'dashboard', route: '/admin' },
    { label: 'Cuidadores', icon: 'person', route: '/admin/cuidadores' },
    { label: 'Pacientes', icon: 'people', route: '/admin/pacientes' },
    { label: 'Pagos', icon: 'payments', route: '/admin/pagos' },
    { label: 'Documentos', icon: 'description', route: '/admin/documentos' },
    { label: 'Reportes', icon: 'assessment', route: '/admin/reportes' },
    { label: 'Configuración', icon: 'settings', route: '/admin/configuracion' }
  ];

  return (
    <aside className={`sidebar-container ${collapsed ? 'collapsed' : ''}`}>
      {/* Logo (solo visible cuando el sidebar está expandido) */}
      {!collapsed && (
        <div className="brand" style={{ height: 'auto', padding: '20px 0' }}>
          <img
            src="/logoV3.png"
            alt="Valora"
            style={{ height: '10rem', width: 'auto', margin: '0 auto' }}
            className="logo-dash"
          />
        </div>
      )}

      {/* Navegación */}
      <nav className="navigation">
        <ul>
          {menuItems.map((item, index) => (
            <li key={index}>
              <a 
                href={item.route} 
                className={`nav-link ${index === 0 ? 'active' : ''}`}
              >
                <span className="material-icons nav-icon">{item.icon}</span>
                {!collapsed && (
                  <span className="nav-label">{item.label}</span>
                )}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}