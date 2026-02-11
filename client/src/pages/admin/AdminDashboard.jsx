import Header from '../../core/components/header/Header';
import Sidebar from '../../core/components/sidebar/Sidebar';
import { useState, useEffect } from 'react';
import "./AdminDashboard.css";

const stats = [
  { label: "Usuarios", value: "1,245", icon: "people", color: "blue" },
  { label: "Ingresos", value: "$12,430", icon: "attach_money", color: "green" },
  { label: "Gastos", value: "$3,210", icon: "trending_down", color: "orange" },
  { label: "Pendientes", value: "18", icon: "schedule", color: "cyan" }
];

const validationRequests = [
  { name: "Juan Pérez", doc: "Contrato", value: "$450", status: "pending" },
  { name: "María López", doc: "Factura", value: "$1,200", status: "approved" }
];

const recentPayments = [
  { name: "Carlos Ruiz", amount: "$250" },
  { name: "Ana Gómez", amount: "$980" }
];

export default function AdminDashboard() {
  // Estado para controlar si el sidebar está colapsado
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Manejador de toggle del sidebar
  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  // Detectar cambios de tamaño de pantalla
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true);
      } else {
        setSidebarCollapsed(false);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Ejecutar al inicio
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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
      <div className={`dashboard-container ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>

        <header className="page-header">
          <h1 className="page-title">Dashboard</h1>
        </header>

        {/* STATS */}
        <div className="stats-grid">
          {stats.map((stat, i) => (
            <div key={i} className={`stat-card ${stat.color}`}>
              <div className="stat-icon">
                <span className="material-icons">{stat.icon}</span>
              </div>
              <div className="stat-info">
                <span className="stat-label">{stat.label}</span>
                <span className="stat-value">{stat.value}</span>
              </div>
              <svg viewBox="0 0 100 25" className="sparkline">
                <path
                  d="M0 20 Q 20 5 40 15 T 80 10 T 100 15"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                />
              </svg>
            </div>
          ))}
        </div>

        {/* MAIN GRID */}
        <div className="dashboard-main-grid">

          {/* LEFT COLUMN */}
          <div className="left-column">

            {/* MÉTRICAS */}
            <section className="dashboard-section">
              <div className="card metrics-card">
                <div className="card-header">
                  <h3>Métricas de Gestión</h3>
                  <button className="btn-link">Métricas 30 días &gt;</button>
                </div>

                <svg width="100%" height="200" viewBox="0 0 500 200">
                  <path
                    d="M0 150 C 100 100 150 180 250 120 S 350 50 500 80"
                    stroke="#3b82f6"
                    strokeWidth="3"
                    fill="none"
                  />
                  <path
                    d="M0 180 C 100 160 150 190 250 150 S 350 120 500 140"
                    stroke="#10b981"
                    strokeWidth="3"
                    fill="none"
                  />
                </svg>
              </div>
            </section>

            {/* VALIDACIONES */}
            <section className="dashboard-section">
              <div className="card table-card">
                <div className="card-header">
                  <h3>Solicitudes de Validación</h3>
                  <select>
                    <option>Cuentas</option>
                  </select>
                </div>

                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Documento</th>
                      <th>Descripción</th>
                      <th>Valor</th>
                      <th>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {validationRequests.map((item, i) => (
                      <tr key={i}>
                        <td>
                          <div className="user-cell">
                            <div className="avatar-xs"></div>
                            {item.name}
                          </div>
                        </td>
                        <td>{item.doc}</td>
                        <td className="font-bold">{item.value}</td>
                        <td>
                          <span className={`badge ${item.status}`}>
                            {item.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            {/* PAGOS */}
            <section className="dashboard-section">
              <div className="card table-card">
                <div className="card-header">
                  <h3>Pagos Recientes</h3>
                </div>

                {recentPayments.map((pay, i) => (
                  <div key={i} className="list-item">
                    <div className="user-cell">
                      <div className="avatar-sm"></div>
                      {pay.name}
                    </div>
                    <span className="amount-tag">{pay.amount}</span>
                  </div>
                ))}
              </div>
            </section>

          </div>

          {/* RIGHT COLUMN */}
          <div className="right-column">

            <section className="dashboard-section">
              <div className="card actions-card">
                <h3>Pagos (Items faltantes)</h3>

                <button className="btn btn-primary full-width">
                  <span className="material-icons">add</span>
                  Registrar Guardia
                </button>

                <button className="btn btn-outline full-width">
                  <span className="material-icons">fact_check</span>
                  Verificar Documentos
                </button>
              </div>
            </section>

            <section className="dashboard-section">
              <div className="card payments-card">
                <div className="payment-item">
                  <div className="user-cell">
                    <div className="avatar-sm">AM</div>
                    Ana Martínez
                  </div>
                  <strong>$245.70</strong>
                </div>
              </div>
            </section>

          </div>
        </div>
      </div>
    </>
  );
}