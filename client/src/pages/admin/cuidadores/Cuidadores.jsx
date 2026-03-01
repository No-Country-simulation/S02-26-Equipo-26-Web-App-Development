import Header from '../../../core/components/header/Header';
import Sidebar from '../../../core/components/sidebar/Sidebar';
import CreateCaregiverModal from '../../../core/components/CreateCaregiverModal';
import { useState, useEffect } from 'react';
import { caregiverService } from '../../../core/services/caregiverService';
import './Cuidadores.css';

// Configuración de colores por especialidad
const especialidadConfig = {
  "Geriatría": { className: "especialidad-geriatria" },
  "Discapacidad": { className: "especialidad-discapacidad" },
  "Pediatría": { className: "especialidad-pediatria" },
  "Post-operatorio": { className: "especialidad-postoperatorio" },
  "Alzheimer": { className: "especialidad-alzheimer" },
  "Cuidados paliativos": { className: "especialidad-paliativos" },
};

export default function CuidadoresPage({ sidebarCollapsed, toggleSidebar }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [especialidadFilter, setEspecialidadFilter] = useState("todas");
  const [disponibilidadFilter, setDisponibilidadFilter] = useState("cualquiera");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [caregivers, setCaregivers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Cargar cuidadores del backend
  const loadCaregivers = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await caregiverService.getAll();
      // Mapear datos del backend al formato del frontend
      const mappedData = data.map(c => ({
        id: `#C-${c.id}`,
        nombre: c.full_name,
        avatar: "/user-placeholder.png",
        especialidad: c.specialty_name || "Sin especialidad",
        estado: c.is_active ? "activo" : "inactivo",
        email: c.email,
        telefono: c.phone_number || "No disponible",
      }));
      setCaregivers(mappedData);
    } catch (err) {
      console.error('Error cargando cuidadores:', err);
      setError('Error al cargar cuidadores. Intenta recargar la página.');
      // Si falla, mostrar array vacío (no mockup)
      setCaregivers([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCaregivers();
  }, []);

  // Filtrar cuidadores
  const filteredCuidadores = caregivers.filter((cuidador) => {
    const matchesSearch =
      cuidador.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cuidador.especialidad.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesEspecialidad =
      especialidadFilter === "todas" ||
      cuidador.especialidad.toLowerCase() === especialidadFilter.toLowerCase();
    return matchesSearch && matchesEspecialidad;
  });

  // Obtener iniciales del nombre
  const getInitials = (nombre) => {
    return nombre
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  return (
    <>
      {/* Header con Hamburger Menu */}
      <Header 
        sidebarCollapsed={sidebarCollapsed} 
        onToggleSidebar={toggleSidebar} 
      />

      {/* Sidebar */}
      <Sidebar collapsed={sidebarCollapsed} />

      {/* Contenido principal */}
      <div className={`caregivers-page ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        {/* Header */}
        <div className="page-header">
          <div className="header-content">
            <h1 className="page-title">Gestión de Cuidadores</h1>
            <p className="page-subtitle">Administra y supervisa al personal terapéutico.</p>
          </div>
          <button 
            className="btn-primary btn-new-caregiver"
            onClick={() => setIsModalOpen(true)}
          >
            <span className="material-icons">person_add</span>
            Nuevo Cuidador
          </button>
        </div>

        {/* Error message */}
        {error && (
          <div className="error-banner">
            {error}
            <button onClick={loadCaregivers}>Reintentar</button>
          </div>
        )}

        {/* Filters */}
        <div className="card filters-card">
          <div className="filters-grid">
            <div className="filter-group">
              <label className="filter-label">Especialización</label>
              <select 
                className="filter-select" 
                value={especialidadFilter} 
                onChange={(e) => setEspecialidadFilter(e.target.value)}
              >
                <option value="todas">Todas las especialidades</option>
                <option value="geriatría">Geriatría</option>
                <option value="pediatría">Pediatría</option>
                <option value="discapacidad">Discapacidad</option>
                <option value="post-operatorio">Post-operatorio</option>
                <option value="alzheimer">Alzheimer</option>
                <option value="cuidados paliativos">Cuidados paliativos</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label">Disponibilidad</label>
              <select 
                className="filter-select" 
                value={disponibilidadFilter} 
                onChange={(e) => setDisponibilidadFilter(e.target.value)}
              >
                <option value="cualquiera">Cualquier horario</option>
                <option value="mañana">Turno mañana</option>
                <option value="tarde">Turno tarde</option>
                <option value="noche">Turno noche</option>
                <option value="24h">24 horas</option>
              </select>
            </div>

            <div className="filter-actions">
              <button className="btn-icon" title="Filtrar">
                <span className="material-icons">filter_list</span>
              </button>
              <button className="btn-icon" title="Descargar">
                <span className="material-icons">download</span>
              </button>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="card table-card">
          <div className="table-container">
            {isLoading ? (
              <div className="loading-state">Cargando cuidadores...</div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr className="table-header-row">
                    <th className="table-header">Cuidador</th>
                    <th className="table-header">Especialidad</th>
                    <th className="table-header">Estado</th>
                    <th className="table-header">Contacto</th>
                    <th className="table-header">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCuidadores.length === 0 ? (
                    <tr>
                      <td colSpan="5" className="empty-state">
                        No hay cuidadores registrados
                      </td>
                    </tr>
                  ) : (
                    filteredCuidadores.map((cuidador) => {
                      const especialidadStyle = especialidadConfig[cuidador.especialidad] || {
                        className: "especialidad-default",
                      };
                      return (
                        <tr key={cuidador.id} className="table-row">
                          <td className="table-cell">
                            <div className="caregiver-info">
                              <div className="avatar">
                                <img 
                                  src={cuidador.avatar} 
                                  alt={cuidador.nombre} 
                                  className="avatar-img"
                                />
                                <div className="avatar-fallback">
                                  {getInitials(cuidador.nombre)}
                                </div>
                              </div>
                              <div className="caregiver-details">
                                <p className="caregiver-name">{cuidador.nombre}</p>
                                <p className="caregiver-id">ID: {cuidador.id}</p>
                              </div>
                            </div>
                          </td>
                          <td className="table-cell">
                            <span className={`badge ${especialidadStyle.className}`}>
                              {cuidador.especialidad}
                            </span>
                          </td>
                          <td className="table-cell">
                            <span className={`badge ${cuidador.estado === "activo" ? "badge-active" : "badge-inactive"}`}>
                              <span className={`status-dot ${cuidador.estado === "activo" ? "dot-active" : "dot-inactive"}`}></span>
                              {cuidador.estado === "activo" ? "Activo" : "Inactivo"}
                            </span>
                          </td>
                          <td className="table-cell">
                            <div className="contact-info">
                              <div className="contact-item">
                                <span className="material-icons contact-icon">email</span>
                                <span className="contact-text">{cuidador.email}</span>
                              </div>
                              <div className="contact-item">
                                <span className="material-icons contact-icon">phone</span>
                                <span className="contact-text">{cuidador.telefono}</span>
                              </div>
                            </div>
                          </td>
                          <td className="table-cell">
                            <div className="action-buttons">
                              <button className="btn-action" title="Ver">
                                <span className="material-icons">visibility</span>
                              </button>
                              <button className="btn-action" title="Más">
                                <span className="material-icons">more_horiz</span>
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            )}
          </div>

          {/* Pagination */}
          <div className="pagination">
            <div className="pagination-info">
              Mostrando {filteredCuidadores.length > 0 ? `1-${filteredCuidadores.length}` : '0'} de {filteredCuidadores.length} cuidadores
            </div>
            <div className="pagination-buttons">
              <button className="btn-pagination btn-prev" disabled>
                Anterior
              </button>
              <button className="btn-pagination btn-next">
                Siguiente
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal para crear cuidador */}
      <CreateCaregiverModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={loadCaregivers}
      />
    </>
  );
}