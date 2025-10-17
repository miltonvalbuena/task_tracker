import React from 'react';
import { useQuery } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { dashboardService, userService, taskService } from '../services/api';
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  Users, 
  Building2,
  Activity,
  Target,
  BarChart3,
  PieChart as PieChartIcon,
  BarChart
} from 'lucide-react';
import { CountBadge } from '../components/Badge';
import { PieChart, Pie, Cell, BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const { user } = useAuth();
  
  const { data: stats, isLoading } = useQuery(
    ['dashboard-stats', user?.role],
    () => dashboardService.getStats(user?.role === 'admin' ? null : user?.client_id),
    {
      enabled: !!user,
      refetchInterval: 30000
    }
  );

  const { data: companyStats } = useQuery(
    ['company-stats'],
    () => dashboardService.getClientStats(),
    {
      enabled: user?.role === 'admin'
    }
  );

  const { data: users } = useQuery(
    ['users'],
    () => userService.getAll(),
    {
      enabled: user?.role === 'admin'
    }
  );

  const { data: tasks } = useQuery(
    ['tasks'],
    () => taskService.getAll(),
    {
      enabled: user?.role === 'admin'
    }
  );

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '50vh',
        background: '#f7f9fc'
      }}>
        <div className="loading">Cargando dashboard...</div>
      </div>
    );
  }

  // Mostrar mensaje si no hay datos
  if (!stats) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '50vh',
        background: '#f7f9fc'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div className="error">No se pudieron cargar los datos del dashboard</div>
          <p style={{ marginTop: '10px', color: '#666' }}>
            Verifica tu conexión o contacta al administrador
          </p>
        </div>
      </div>
    );
  }

  const pieData = stats ? [
    { name: 'Pendientes', value: stats.pending_tasks, color: '#f39c12' },
    { name: 'En Progreso', value: stats.in_progress_tasks, color: '#3498db' },
    { name: 'Completadas', value: stats.completed_tasks, color: '#27ae60' },
    { name: 'Vencidas', value: stats.overdue_tasks, color: '#e74c3c' },
  ] : [];

  // Agrupar usuarios por nombre para evitar duplicados
  const userTaskData = users?.reduce((acc, userItem) => {
    const userTasks = tasks?.filter(task => task.assigned_to === userItem.id) || [];
    const existingUser = acc.find(u => u.name === userItem.full_name);
    
    if (existingUser) {
      existingUser.total += userTasks.length;
      existingUser.completadas += userTasks.filter(task => task.status === 'completada').length;
    } else {
      acc.push({
        name: userItem.full_name,
        total: userTasks.length,
        completadas: userTasks.filter(task => task.status === 'completada').length
      });
    }
    return acc;
  }, []) || [];

  const companyTaskData = companyStats?.map(company => ({
    name: company.client?.name || 'N/A',
    total: company.task_stats.total_tasks,
    completadas: company.task_stats.completed_tasks,
    pendientes: company.task_stats.pending_tasks,
    en_progreso: company.task_stats.in_progress_tasks,
    vencidas: company.task_stats.overdue_tasks,
  })) || [];

  return (
    <div style={{ 
      padding: '20px', 
      background: '#f7f9fc',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'white',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        border: '1px solid #f0f0f0',
        overflow: 'hidden',
        marginBottom: '30px'
      }}>
        <div style={{
          background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
          color: 'white',
          padding: '20px 24px',
          borderBottom: '1px solid #f0f0f0'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <BarChart3 size={24} />
                Dashboard Ko-Actuar
              </h1>
              <p style={{ margin: '8px 0 0', opacity: 0.9, fontSize: '14px' }}>
                Sistema de gestión de actividades para Administradoras de Riesgos Laborales
              </p>
            </div>
            <div style={{ 
              background: 'rgba(255,255,255,0.1)', 
              padding: '16px', 
              borderRadius: '8px',
              textAlign: 'center',
              backdropFilter: 'blur(10px)'
            }}>
              <div style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '4px' }}>
                {stats?.total_tasks || 0}
              </div>
              <div style={{ fontSize: '12px', opacity: 0.9 }}>
                Total de Actividades
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Estadísticas Principales */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
        gap: '20px', 
        marginBottom: '30px'
      }}>
        {/* Actividades Pendientes */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          transition: 'all 0.3s ease',
          cursor: 'default'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.12)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center'
          }}>
            <div>
              <div style={{ 
                fontSize: '14px', 
                color: '#f39c12', 
                fontWeight: '600',
                marginBottom: '8px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Actividades Pendientes
              </div>
              <div style={{ 
                fontSize: '32px', 
                fontWeight: 'bold', 
                color: '#2c3e50',
                marginBottom: '4px'
              }}>
                {stats?.pending_tasks || 0}
              </div>
              <div style={{ 
                fontSize: '12px', 
                color: '#7f8c8d',
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.pending_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)',
              boxShadow: '0 4px 12px rgba(243, 156, 18, 0.3)'
            }}>
              <Clock size={24} color="white" />
            </div>
          </div>
        </div>

        {/* En Ejecución */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          transition: 'all 0.3s ease',
          cursor: 'default'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.12)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center'
          }}>
            <div>
              <div style={{ 
                fontSize: '14px', 
                color: '#3498db', 
                fontWeight: '600',
                marginBottom: '8px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                En Ejecución
              </div>
              <div style={{ 
                fontSize: '32px', 
                fontWeight: 'bold', 
                color: '#2c3e50',
                marginBottom: '4px'
              }}>
                {stats?.in_progress_tasks || 0}
              </div>
              <div style={{ 
                fontSize: '12px', 
                color: '#7f8c8d',
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.in_progress_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
              boxShadow: '0 4px 12px rgba(52, 152, 219, 0.3)'
            }}>
              <Activity size={24} color="white" />
            </div>
          </div>
        </div>

        {/* Finalizadas */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          transition: 'all 0.3s ease',
          cursor: 'default'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.12)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center'
          }}>
            <div>
              <div style={{ 
                fontSize: '14px', 
                color: '#27ae60', 
                fontWeight: '600',
                marginBottom: '8px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Finalizadas
              </div>
              <div style={{ 
                fontSize: '32px', 
                fontWeight: 'bold', 
                color: '#2c3e50',
                marginBottom: '4px'
              }}>
                {stats?.completed_tasks || 0}
              </div>
              <div style={{ 
                fontSize: '12px', 
                color: '#7f8c8d',
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.completed_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #27ae60 0%, #229954 100%)',
              boxShadow: '0 4px 12px rgba(39, 174, 96, 0.3)'
            }}>
              <CheckCircle size={24} color="white" />
            </div>
          </div>
        </div>

        {/* Vencidas/Retrasadas */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          transition: 'all 0.3s ease',
          cursor: 'default'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-4px)';
          e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.12)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0)';
          e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center'
          }}>
            <div>
              <div style={{ 
                fontSize: '14px', 
                color: '#e74c3c', 
                fontWeight: '600',
                marginBottom: '8px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Vencidas/Retrasadas
              </div>
              <div style={{ 
                fontSize: '32px', 
                fontWeight: 'bold', 
                color: '#2c3e50',
                marginBottom: '4px'
              }}>
                {stats?.overdue_tasks || 0}
              </div>
              <div style={{ 
                fontSize: '12px', 
                color: '#7f8c8d',
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.overdue_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
              boxShadow: '0 4px 12px rgba(231, 76, 60, 0.3)'
            }}>
              <AlertCircle size={24} color="white" />
            </div>
          </div>
        </div>
      </div>

      {/* Sección de Gráficos */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))', 
        gap: '30px',
        marginBottom: '30px'
      }}>
        {/* Gráfico de Pie */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          overflow: 'hidden'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
            color: 'white',
            padding: '20px 24px',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <PieChartIcon size={20} />
              Distribución de Actividades
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Estado actual del sistema de gestión
            </p>
          </div>
          <div style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
              {/* Gráfico de Pie */}
              <div style={{ flex: '0 0 300px' }}>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={false}
                      outerRadius={90}
                      innerRadius={30}
                      fill="#3498db"
                      dataKey="value"
                      stroke="#fff"
                      strokeWidth={2}
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value, name) => [value, name]}
                      labelStyle={{ color: '#2c3e50', fontWeight: '600' }}
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #e1e5e9',
                        borderRadius: '8px',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              {/* Leyendas */}
              <div style={{ flex: 1, paddingLeft: '20px' }}>
                <div style={{ fontSize: '14px', fontWeight: '600', color: '#2c3e50', marginBottom: '16px' }}>
                  Detalle por Estado:
                </div>
                {pieData.map((item, index) => (
                  <div key={index} style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    marginBottom: '12px',
                    padding: '8px 12px',
                    backgroundColor: '#f8f9fa',
                    borderRadius: '8px',
                    border: '1px solid #e1e5e9'
                  }}>
                    <div style={{
                      width: '16px',
                      height: '16px',
                      backgroundColor: item.color,
                      borderRadius: '50%',
                      marginRight: '12px',
                      flexShrink: 0
                    }}></div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: '14px', fontWeight: '600', color: '#2c3e50', marginBottom: '2px' }}>
                        {item.name}
                      </div>
                      <div style={{ fontSize: '12px', color: '#666' }}>
                        {item.value} actividades ({((item.value / (stats?.total_tasks || 1)) * 100).toFixed(1)}%)
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Gráfico de Barras - Actividades por ARL */}
        {user?.role === 'admin' && (
          <div style={{
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            border: '1px solid #f0f0f0',
            overflow: 'hidden'
          }}>
            <div style={{
              background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
              color: 'white',
              padding: '20px 24px',
              borderBottom: '1px solid #f0f0f0'
            }}>
              <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BarChart size={20} />
                Actividades por ARL
              </h3>
              <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
                Distribución de actividades por Administradora de Riesgos Laborales
              </p>
            </div>
            <div style={{ padding: '20px' }}>
              <ResponsiveContainer width="100%" height={300}>
                <RechartsBarChart data={companyTaskData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e1e5e9" />
                  <XAxis 
                    dataKey="name" 
                    tick={{ fontSize: 12, fill: '#666' }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis 
                    tick={{ fontSize: 12, fill: '#666' }}
                    label={{ value: 'Número de Actividades', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #e1e5e9',
                      borderRadius: '8px',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                    }}
                    formatter={(value, name) => [value, name]}
                  />
                  <Bar dataKey="total" fill="#3498db" name="Total" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="pendientes" fill="#f39c12" name="Pendientes" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="en_progreso" fill="#3498db" name="En Ejecución" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="completadas" fill="#27ae60" name="Finalizadas" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="vencidas" fill="#e74c3c" name="Vencidas" radius={[4, 4, 0, 0]} />
                </RechartsBarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>

      {/* Gráfico de Responsables (Solo Admin) */}
      {user?.role === 'admin' && userTaskData.length > 0 && (
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          overflow: 'hidden',
          marginBottom: '30px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
            color: 'white',
            padding: '20px 24px',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Users size={20} />
              Carga de Trabajo por Responsable
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Distribución de actividades asignadas a cada responsable ARL
            </p>
          </div>
          <div style={{ padding: '20px' }}>
            <ResponsiveContainer width="100%" height={350}>
              <RechartsBarChart data={userTaskData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e1e5e9" />
                <XAxis 
                  dataKey="name" 
                  tick={{ fontSize: 12, fill: '#666' }}
                  angle={-45}
                  textAnchor="end"
                  height={100}
                />
                <YAxis 
                  tick={{ fontSize: 12, fill: '#666' }}
                  label={{ value: 'Número de Actividades', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e1e5e9',
                    borderRadius: '8px',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                  }}
                  formatter={(value, name) => [value, name]}
                />
                <Bar dataKey="total" fill="#3498db" name="Total Asignadas" radius={[4, 4, 0, 0]} />
                <Bar dataKey="completadas" fill="#27ae60" name="Finalizadas" radius={[4, 4, 0, 0]} />
              </RechartsBarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tabla de Clientes con Estadísticas (Solo Admin) */}
      {user?.role === 'admin' && companyTaskData.length > 0 && (
        <div style={{
          background: 'white',
          borderRadius: '16px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          overflow: 'hidden',
          marginBottom: '30px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
            color: 'white',
            padding: '20px 24px',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Building2 size={20} />
              Resumen por Cliente ARL
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Detalle de actividades por cada cliente del sistema
            </p>
          </div>
          <div style={{ padding: '0' }}>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f8f9fa' }}>
                    <th style={{ padding: '16px', textAlign: 'left', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Cliente
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Total
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Pendientes
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      En Ejecución
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Finalizadas
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Vencidas
                    </th>
                    <th style={{ padding: '16px', textAlign: 'center', borderBottom: '2px solid #e1e5e9', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                      Progreso
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {companyTaskData.slice(0, 10).map((client, index) => {
                    const progress = client.total > 0 ? (client.completadas / client.total) * 100 : 0;
                    return (
                      <tr key={index} style={{ 
                        borderBottom: '1px solid #f0f0f0',
                        backgroundColor: index % 2 === 0 ? '#fff' : '#f8f9fa'
                      }}>
                        <td style={{ padding: '16px', fontSize: '13px', color: '#2c3e50', maxWidth: '300px' }}>
                          <div style={{ fontWeight: '500' }}>
                            {client.name.length > 40 ? `${client.name.substring(0, 40)}...` : client.name}
                          </div>
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center', fontSize: '14px', fontWeight: '600', color: '#2c3e50' }}>
                          {client.total}
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <CountBadge count={client.pendientes} color="#f39c12" />
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <CountBadge count={client.en_progreso} color="#3498db" />
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <CountBadge count={client.completadas} color="#27ae60" />
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <CountBadge count={client.vencidas} color="#e74c3c" />
                        </td>
                        <td style={{ padding: '16px', textAlign: 'center' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div style={{
                              width: '60px',
                              height: '8px',
                              backgroundColor: '#e1e5e9',
                              borderRadius: '4px',
                              overflow: 'hidden'
                            }}>
                              <div style={{
                                width: `${progress}%`,
                                height: '100%',
                                backgroundColor: progress > 70 ? '#27ae60' : progress > 40 ? '#f39c12' : '#e74c3c',
                                transition: 'width 0.3s ease'
                              }}></div>
                            </div>
                            <span style={{ fontSize: '12px', fontWeight: '600', color: '#2c3e50' }}>
                              {progress.toFixed(0)}%
                            </span>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            {companyTaskData.length > 10 && (
              <div style={{ padding: '16px', textAlign: 'center', backgroundColor: '#f8f9fa', borderTop: '1px solid #e1e5e9' }}>
                <span style={{ fontSize: '14px', color: '#666' }}>
                  Mostrando 10 de {companyTaskData.length} clientes
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Resumen Ejecutivo Simplificado */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        border: '1px solid #f0f0f0',
        overflow: 'hidden'
      }}>
        <div style={{
          background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
          color: 'white',
          padding: '20px 24px',
          borderBottom: '1px solid #f0f0f0'
        }}>
          <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Target size={20} />
            Indicadores de Rendimiento
          </h3>
          <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
            Métricas clave del sistema de gestión ARL
          </p>
        </div>
        <div style={{ padding: '30px' }}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
            gap: '24px' 
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#27ae60' }}>
                {stats && stats.total_tasks > 0 ? ((stats.completed_tasks / stats.total_tasks) * 100).toFixed(1) : 0}%
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Tasa de Finalización</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#e74c3c' }}>
                {stats && stats.total_tasks > 0 ? ((stats.overdue_tasks / stats.total_tasks) * 100).toFixed(1) : 0}%
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Tasa de Retraso</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3498db' }}>
                {stats && stats.total_tasks > 0 ? ((stats.in_progress_tasks / stats.total_tasks) * 100).toFixed(1) : 0}%
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>En Ejecución</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f39c12' }}>
                {stats && stats.total_tasks > 0 ? ((stats.pending_tasks / stats.total_tasks) * 100).toFixed(1) : 0}%
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Pendientes</div>
            </div>
          </div>

          {/* Explicación de la Lógica */}
          <div style={{ 
            marginTop: '30px', 
            padding: '20px', 
            backgroundColor: '#e8f4fd', 
            borderRadius: '12px',
            border: '1px solid #3498db',
            borderLeft: '4px solid #3498db'
          }}>
            <h4 style={{ margin: '0 0 12px 0', fontSize: '16px', fontWeight: '600', color: '#2c3e50', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertCircle size={18} color="#3498db" />
              Explicación de los Datos
            </h4>
            <div style={{ fontSize: '14px', color: '#2c3e50', lineHeight: '1.6' }}>
              <p style={{ margin: '0 0 8px 0' }}>
                <strong>Actividades Pendientes:</strong> Tareas que están en estado inicial y requieren ser iniciadas.
              </p>
              <p style={{ margin: '0 0 8px 0' }}>
                <strong>Actividades Vencidas:</strong> Tareas que tienen fechas de vencimiento que ya pasaron y requieren atención inmediata.
              </p>
              <p style={{ margin: '0' }}>
                <strong>Lógica:</strong> Una actividad puede estar pendiente pero vencida si su fecha límite ya expiró.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;