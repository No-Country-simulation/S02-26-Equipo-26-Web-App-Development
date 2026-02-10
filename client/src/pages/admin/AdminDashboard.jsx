import { useState } from 'react';
import './AdminDashboard.css';

export default function AdminDashboard() {
  // Datos de ejemplo
  const stats = [
    { label: 'Ingresos', value: '$24,570', icon: 'trending_up', color: 'blue' },
    { label: 'Gastos', value: '$8,112', icon: 'trending_down', color: 'cyan' },
    { label: 'Pacientes', value: '124', icon: 'people', color: 'orange' },
    { label: 'Guardias', value: '352', icon: 'assignment', color: 'green' }
  ];

  const validationRequests = [
    { name: 'Juan Pérez', doc: 'DNI 38.456.789', value: '$245.70', status: 'pending' },
    { name: 'María García', doc: 'DNI 29.123.456', value: '$180.00', status: 'approved' },
    { name: 'Carlos López', doc: 'DNI 42.789.123', value: '$320.50', status: 'pending' },
    { name: 'Ana Martínez', doc: 'DNI 35.678.901', value: '$150.00', status: 'approved' }
  ];

  const recentPayments = [
    { name: 'Ana Martínez', amount: '$245.70' },
    { name: 'Juan Pérez', amount: '$180.00' },
    { name: 'Carlos López', amount: '$320.50' },
    { name: 'María García', amount: '$150.00' }
  ];

  return (
    <div className="dashboard-container" style={{ minHeight: '100vh' }}>
      {/* Header */}
      <header className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <div className="date-filter"></div>
      </header>

      {/* Estadísticas */}
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className={`stat-card ${stat.color}`}>
            <div className="stat-icon">
              <span className="material-icons">{stat.icon}</span>
            </div>
            <div className="stat-info">
              <span className="stat-label">{stat.label}</span>
              <span className="stat-value">{stat.value}</span>
            </div>
            <div className="stat-chart-mini">
              <svg viewBox="0 0 100 25" className="sparkline">
                <path
                  d="M0 20 Q 20 5 40 15 T 80 10 T 100 15"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                />
              </svg>
            </div>
          </div>
        ))}
      </div>

      {/* Grid principal */}
      <div className="dashboard-main-grid">
        {/* Columna izquierda */}
        <div className="left-column">
          {/* Métricas de Gestión */}
          <div className="card metrics-card">
            <div className="card-header">
              <h3>Métricas de Gestión</h3>
              <button className="btn-link">Métricas 30 días →</button>
            </div>
            <div className="chart-box">
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
                <circle cx="250" cy="120" r="4" fill="#3b82f6" />
                <circle cx="250" cy="150" r="4" fill="#10b981" />
              </svg>
              <div className="chart-legend">
                <span><span className="dot blue"></span> Ingresos</span>
                <span><span className="dot green"></span> Gastos</span>
              </div>
            </div>
          </div>

          {/* Solicitudes de Validación */}
          <div className="card table-card">
            <div className="card-header">
              <h3>Solicitudes de Validación</h3>
              <div className="filters">
                <select>
                  <option>Cuentas</option>
                </select>
              </div>
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
                {validationRequests.map((item, index) => (
                  <tr key={index}>
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
                        {item.status === 'pending' ? 'Pendiente' : 'Aprobado'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagos Recientes */}
          <div className="card table-card">
            <div className="card-header">
              <h3>Pagos Recientes</h3>
            </div>
            <div className="list-items">
              {recentPayments.map((pay, index) => (
                <div key={index} className="list-item">
                  <div className="user-cell">
                    <img src="/user-placeholder.png" className="avatar-sm" alt={pay.name} />
                    <span>{pay.name}</span>
                  </div>
                  <span className="amount-tag">{pay.amount}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Columna derecha */}
        <div className="right-column">
          {/* Acciones */}
          <div className="card actions-card">
            <h3>Pagos (Items faltantes)</h3>
            <div className="action-buttons">
              <button className="btn btn-primary full-width">
                <span className="material-icons">add</span> Registrar Guardia
              </button>
              <button className="btn btn-outline full-width">
                <span className="material-icons">fact_check</span> Verificar Documentos
              </button>
            </div>
          </div>

          {/* Pagos Recientes (Resumen) */}
          <div className="card payments-card">
            <div className="card-header">
              <h3>Pagos Recientes</h3>
            </div>
            <div className="payment-list">
              <div className="payment-item">
                <div className="pay-info">
                  <div className="avatar-sm">AM</div>
                  <div>
                    <div className="pay-name">Ana Martínez</div>
                    <div className="pay-sub">Transferencia</div>
                  </div>
                </div>
                <div className="pay-amount">$245.70</div>
              </div>
              <div className="payment-item">
                <div className="pay-info">
                  <div className="avatar-sm">JP</div>
                  <div>
                    <div className="pay-name">Jose Perez</div>
                    <div className="pay-sub">Recibo</div>
                  </div>
                </div>
                <div className="pay-amount">$8,112.00</div>
              </div>
              <div className="bank-item">
                <span className="material-icons bank-icon">account_balance</span>
                <span>Banco Nación</span>
                <span className="bank-amount green">$465.70</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}