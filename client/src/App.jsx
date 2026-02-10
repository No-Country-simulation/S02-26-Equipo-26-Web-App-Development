// src/app/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/login/Login';
import Register from './pages/register/register';
import AdminDashboard from './pages/admin/AdminDashboard';
import CaregiverDashboard from './pages/caregiver/CaregiverDashboard';
import FamilyDashboard from './pages/family/FamilyDashboard';

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;