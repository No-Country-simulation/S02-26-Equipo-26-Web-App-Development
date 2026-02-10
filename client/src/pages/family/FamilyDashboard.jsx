import { Link } from 'react-router-dom';

export default function FamilyDashboard() {
  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      color: 'white',
      fontFamily: 'Inter, sans-serif'
    }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>👨‍👩‍👧‍👦</h1>
      <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>¡Hola, Familia!</h2>
      <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>Has ingresado al panel de pacientes/familiares</p>
      
      <div style={{ 
        background: 'rgba(255, 255, 255, 0.1)',
        padding: '2rem',
        borderRadius: '12px',
        backdropFilter: 'blur(10px)',
        textAlign: 'center'
      }}>
        <p style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>
          🏠 Funcionalidades disponibles próximamente
        </p>
        <Link 
          to="/login" 
          style={{
            display: 'inline-block',
            padding: '12px 24px',
            background: '#fff',
            color: '#00f2fe',
            textDecoration: 'none',
            borderRadius: '8px',
            fontWeight: '600',
            transition: 'all 0.3s'
          }}
          onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
          onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
        >
          ← Volver al Login
        </Link>
      </div>
    </div>
  );
}