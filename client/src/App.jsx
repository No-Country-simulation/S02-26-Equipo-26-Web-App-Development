import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/login/Login';
import Register from './pages/register/Register';

import AdminDashboard from './pages/admin/AdminDashboard';
import CaregiverDashboard from './pages/caregiver/CaregiverDashboard';
import FamilyDashboard from './pages/family/FamilyDashboard';

import CuidadoresPage from './pages/admin/cuidadores/Cuidadores';
import PacientesPage from './pages/admin/pacientes/pacientes';
import PagosPage from './pages/admin/pagos/pagos';
import DocumentosPage from './pages/admin/documentos/documentos';
import ReportesPage from './pages/admin/reportes/Reportes';
import ConfiguracionPage from './pages/admin/Configuracion/configuracion';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/caregiver" element={<CaregiverDashboard />} />
        <Route path="/family" element={<FamilyDashboard />} />

        <Route path="/admin/cuidadores" element={<CuidadoresPage />} />
        <Route path="/admin/pacientes" element={<PacientesPage />} />
        <Route path="/admin/pagos" element={<PagosPage />} />
        <Route path="/admin/documentos" element={<DocumentosPage />} />
        <Route path="/admin/reportes" element={<ReportesPage />} />
        <Route path="/admin/configuracion" element={<ConfiguracionPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;