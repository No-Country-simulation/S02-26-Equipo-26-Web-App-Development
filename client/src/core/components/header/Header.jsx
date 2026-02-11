import './Header.css';

export default function Header({ sidebarCollapsed, onToggleSidebar }) {
  return (
    <header className="app-header">
      {/* Hamburger Menu (reemplaza el logo) */}
      <button 
        className="sidebar-toggle" 
        onClick={onToggleSidebar}
        aria-label={sidebarCollapsed ? "Expandir sidebar" : "Colapsar sidebar"}
      >
        <span className="material-icons">
          {sidebarCollapsed ? 'menu' : 'close'}
        </span>
      </button>
      
      {/* Acciones del header (notificaciones y perfil) */}
      <div className="header-actions">
        <button className="icon-btn" title="Notificaciones">
          <span className="material-icons">notifications</span>
        </button>
        <div className="user-profile">
          <img 
            src="/user-placeholder.png" 
            alt="User" 
            className="avatar"
          />
        </div>
      </div>
    </header>
  );
}