import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ConfigProvider } from './contexts/ConfigContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import TaskForm from './pages/TaskForm';
import Users from './pages/Users';
import Clients from './pages/Clients';
import Reports from './pages/Reports';
import SystemConfig from './pages/SystemConfig';
import './App.css';

const queryClient = new QueryClient();

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="loading">Cargando...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

function AdminRoute({ children }) {
  const { user } = useAuth();
  
  if (user?.role !== 'admin') {
    return <Navigate to="/dashboard" />;
  }
  
  return children;
}

function AppContent() {
  const { user } = useAuth();
  
  return (
    <Router>
      {user && <Navbar />}
      <div className="container-fluid">
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
          
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/tasks" element={
            <ProtectedRoute>
              <Tasks />
            </ProtectedRoute>
          } />
          
          <Route path="/tasks/new" element={
            <ProtectedRoute>
              <TaskForm />
            </ProtectedRoute>
          } />
          
          <Route path="/tasks/:id/edit" element={
            <ProtectedRoute>
              <TaskForm />
            </ProtectedRoute>
          } />
          
          <Route path="/users" element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          } />
          
          <Route path="/clients" element={
            <ProtectedRoute>
              <AdminRoute>
                <Clients />
              </AdminRoute>
            </ProtectedRoute>
          } />
          
          <Route path="/reports" element={
            <ProtectedRoute>
              <Reports />
            </ProtectedRoute>
          } />
          
          <Route path="/system-config" element={
            <ProtectedRoute>
              <AdminRoute>
                <SystemConfig />
              </AdminRoute>
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </Router>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider>
        <AuthProvider>
          <AppContent />
          <Toaster position="top-right" />
        </AuthProvider>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;
