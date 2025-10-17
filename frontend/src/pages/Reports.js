import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { dashboardService, taskService, userService } from '../services/api';
import { 
  Download, 
  Calendar, 
  Users, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  TrendingUp
} from 'lucide-react';
import ActionButton from '../components/ActionButton';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { format, subDays, startOfMonth, endOfMonth } from 'date-fns';
import { es } from 'date-fns/locale';

function Reports() {
  const { user } = useAuth();
  const [dateRange, setDateRange] = useState({
    start: format(startOfMonth(new Date()), 'yyyy-MM-dd'),
    end: format(endOfMonth(new Date()), 'yyyy-MM-dd'),
  });

  const { data: stats } = useQuery(
    ['dashboard-stats', user?.company_id],
    () => dashboardService.getStats(user?.company_id),
    {
      enabled: !!user,
    }
  );

  const { data: companyStats } = useQuery(
    'company-stats',
    () => dashboardService.getCompanyStats(),
    {
      enabled: user?.role === 'admin',
    }
  );

  const { data: tasks } = useQuery(
    ['tasks-report', dateRange],
    () => taskService.getAll({
      start_date: dateRange.start,
      end_date: dateRange.end,
    }),
    {
      enabled: !!user,
    }
  );

  const { data: users } = useQuery(
    'users',
    () => userService.getAll(),
    {
      enabled: !!user,
    }
  );

  const handleDateRangeChange = (field, value) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const exportToCSV = (data, filename) => {
    if (!data || data.length === 0) {
      alert('No hay datos para exportar');
      return;
    }

    const headers = Object.keys(data[0]).join(',');
    const rows = data.map(item => 
      Object.values(item).map(value => 
        typeof value === 'string' && value.includes(',') ? `"${value}"` : value
      ).join(',')
    );
    
    const csvContent = [headers, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const pieData = stats ? [
    { name: 'Pendientes', value: stats.pending_tasks, color: '#f39c12' },
    { name: 'En Progreso', value: stats.in_progress_tasks, color: '#3498db' },
    { name: 'Completadas', value: stats.completed_tasks, color: '#27ae60' },
  ] : [];

  const userTaskData = users?.map(userItem => {
    const userTasks = tasks?.filter(task => task.assigned_to === userItem.id) || [];
    return {
      name: userItem.full_name,
      total: userTasks.length,
      completadas: userTasks.filter(task => task.status === 'completada').length,
      pendientes: userTasks.filter(task => task.status === 'pendiente').length,
    };
  }) || [];

  const monthlyData = [
    { month: 'Ene', completadas: 12, pendientes: 8 },
    { month: 'Feb', completadas: 15, pendientes: 6 },
    { month: 'Mar', completadas: 18, pendientes: 4 },
    { month: 'Abr', completadas: 22, pendientes: 3 },
    { month: 'May', completadas: 20, pendientes: 5 },
    { month: 'Jun', completadas: 25, pendientes: 2 },
  ];

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Reportes</h1>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => handleDateRangeChange('start', e.target.value)}
            className="form-control"
            style={{ width: 'auto' }}
          />
          <span>a</span>
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => handleDateRangeChange('end', e.target.value)}
            className="form-control"
            style={{ width: 'auto' }}
          />
        </div>
      </div>

      {/* Resumen Ejecutivo */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">Resumen Ejecutivo</h3>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
            <CheckCircle size={32} color="#27ae60" />
            <h3 style={{ margin: '8px 0', color: '#27ae60' }}>{stats?.completed_tasks || 0}</h3>
            <p style={{ margin: 0, color: '#666' }}>Tareas Completadas</p>
          </div>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
            <Clock size={32} color="#f39c12" />
            <h3 style={{ margin: '8px 0', color: '#f39c12' }}>{stats?.pending_tasks || 0}</h3>
            <p style={{ margin: 0, color: '#666' }}>Tareas Pendientes</p>
          </div>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
            <TrendingUp size={32} color="#3498db" />
            <h3 style={{ margin: '8px 0', color: '#3498db' }}>{stats?.in_progress_tasks || 0}</h3>
            <p style={{ margin: 0, color: '#666' }}>En Progreso</p>
          </div>
          <div style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
            <AlertCircle size={32} color="#e74c3c" />
            <h3 style={{ margin: '8px 0', color: '#e74c3c' }}>{stats?.overdue_tasks || 0}</h3>
            <p style={{ margin: 0, color: '#666' }}>Tareas Vencidas</p>
          </div>
        </div>
      </div>

      {/* Gráficos */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Distribución de Tareas</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#3498db"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Tareas por Usuario</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={userTaskData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total" fill="#3498db" name="Total" />
              <Bar dataKey="completadas" fill="#27ae60" name="Completadas" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Tendencia Mensual</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="completadas" stroke="#27ae60" name="Completadas" />
              <Line type="monotone" dataKey="pendientes" stroke="#f39c12" name="Pendientes" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {user?.role === 'admin' && companyStats && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Tareas por Empresa</h3>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={companyStats.map(stat => ({
                name: stat.client?.name || 'N/A',
                total: stat.task_stats.total_tasks,
                completadas: stat.task_stats.completed_tasks,
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="total" fill="#3498db" name="Total" />
                <Bar dataKey="completadas" fill="#27ae60" name="Completadas" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Exportar Datos */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Exportar Datos</h3>
        </div>
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <ActionButton
            variant="primary"
            size="medium"
            onClick={() => exportToCSV(tasks || [], `tareas_${dateRange.start}_${dateRange.end}.csv`)}
            icon={Download}
          >
            Exportar Tareas
          </ActionButton>
          <ActionButton
            variant="secondary"
            size="medium"
            onClick={() => exportToCSV(users || [], 'usuarios.csv')}
            icon={Download}
          >
            Exportar Usuarios
          </ActionButton>
          {user?.role === 'admin' && (
            <ActionButton
              variant="secondary"
              size="medium"
              onClick={() => exportToCSV(companyStats || [], 'empresas.csv')}
              icon={Download}
            >
              Exportar Empresas
            </ActionButton>
          )}
        </div>
      </div>
    </div>
  );
}

export default Reports;
