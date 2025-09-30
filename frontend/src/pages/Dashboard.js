import React from 'react';
import { useQuery } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { dashboardService } from '../services/api';
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  Users, 
  Building2,
  TrendingUp,
  Calendar
} from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const { user } = useAuth();
  
  const { data: stats, isLoading } = useQuery(
    ['dashboard-stats', user?.company_id, user?.role],
    () => dashboardService.getStats(user?.role === 'admin' ? null : user?.company_id),
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

  if (isLoading) {
    return <div className="loading">Cargando dashboard...</div>;
  }


  const pieData = stats ? [
    { name: 'Pendientes', value: stats.pending_tasks, color: '#ffc107' },
    { name: 'En Progreso', value: stats.in_progress_tasks, color: '#17a2b8' },
    { name: 'Completadas', value: stats.completed_tasks, color: '#28a745' },
    { name: 'Vencidas', value: stats.overdue_tasks, color: '#dc3545' },
  ] : [];

  const barData = companyStats && Array.isArray(companyStats) ? companyStats
    .filter(company => company.task_stats.total_tasks > 0) // Solo empresas con tareas
    .map(company => ({
      name: company.company.name,
      total: company.task_stats.total_tasks,
      completadas: company.task_stats.completed_tasks,
      pendientes: company.task_stats.pending_tasks,
      en_progreso: company.task_stats.in_progress_tasks,
      vencidas: company.task_stats.overdue_tasks,
    })) : [];

  return (
    <div style={{ 
      padding: '20px', 
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      minHeight: '100vh'
    }}>
      

      {/* Header del Dashboard */}
      <div style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '30px',
        borderRadius: '12px',
        marginBottom: '30px',
        boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '32px', fontWeight: 'bold' }}>
              📊 Dashboard de Tareas
            </h1>
            <p style={{ margin: '8px 0 0', opacity: 0.9, fontSize: '16px' }}>
              Resumen ejecutivo del sistema de gestión de tareas
            </p>
          </div>
          <div style={{ 
            background: 'rgba(255,255,255,0.2)', 
            padding: '20px', 
            borderRadius: '12px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold' }}>
              {stats ? stats.total_tasks : 0}
            </div>
            <div style={{ fontSize: '14px', opacity: 0.9 }}>
              Total de Tareas
            </div>
          </div>
        </div>
      </div>
      
      
      {/* Estadísticas Principales - Ancho Completo */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(4, 1fr)', 
        gap: '20px', 
        marginBottom: '40px',
        width: '100%'
      }}>
        {/* Tareas Pendientes */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '32px',
          boxShadow: '0 10px 40px rgba(255, 193, 7, 0.15)',
          border: '3px solid #ffc107',
          position: 'relative',
          overflow: 'hidden',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }}
        onMouseOver={(e) => {
          e.target.style.transform = 'translateY(-8px) scale(1.02)';
          e.target.style.boxShadow = '0 20px 60px rgba(255, 193, 7, 0.25)';
        }}
        onMouseOut={(e) => {
          e.target.style.transform = 'translateY(0) scale(1)';
          e.target.style.boxShadow = '0 10px 40px rgba(255, 193, 7, 0.15)';
        }}>
          <div style={{
            position: 'absolute',
            top: '-20px',
            right: '-20px',
            width: '100px',
            height: '100px',
            background: 'linear-gradient(135deg, #ffc107 0%, #ff8f00 100%)',
            borderRadius: '50%',
            opacity: 0.1
          }}></div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', zIndex: 1 }}>
            <div>
              <div style={{ 
                fontSize: '64px', 
                fontWeight: '900', 
                color: '#ffc107', 
                margin: 0,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
                lineHeight: 1
              }}>
                {stats ? stats.pending_tasks : 0}
              </div>
              <div style={{ 
                fontSize: '18px', 
                fontWeight: '700', 
                color: '#856404', 
                margin: '8px 0 4px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Pendientes
              </div>
              <div style={{ 
                fontSize: '14px', 
                color: '#6c5b00', 
                margin: 0,
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.pending_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              fontSize: '64px', 
              color: '#ffc107',
              filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.1))'
            }}>
              ⏳
            </div>
          </div>
        </div>

        {/* En Progreso */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '32px',
          boxShadow: '0 10px 40px rgba(23, 162, 184, 0.15)',
          border: '3px solid #17a2b8',
          position: 'relative',
          overflow: 'hidden',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }}
        onMouseOver={(e) => {
          e.target.style.transform = 'translateY(-8px) scale(1.02)';
          e.target.style.boxShadow = '0 20px 60px rgba(23, 162, 184, 0.25)';
        }}
        onMouseOut={(e) => {
          e.target.style.transform = 'translateY(0) scale(1)';
          e.target.style.boxShadow = '0 10px 40px rgba(23, 162, 184, 0.15)';
        }}>
          <div style={{
            position: 'absolute',
            top: '-20px',
            right: '-20px',
            width: '100px',
            height: '100px',
            background: 'linear-gradient(135deg, #17a2b8 0%, #138496 100%)',
            borderRadius: '50%',
            opacity: 0.1
          }}></div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', zIndex: 1 }}>
            <div>
              <div style={{ 
                fontSize: '64px', 
                fontWeight: '900', 
                color: '#17a2b8', 
                margin: 0,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
                lineHeight: 1
              }}>
                {stats ? stats.in_progress_tasks : 0}
              </div>
              <div style={{ 
                fontSize: '18px', 
                fontWeight: '700', 
                color: '#0c5460', 
                margin: '8px 0 4px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                En Progreso
              </div>
              <div style={{ 
                fontSize: '14px', 
                color: '#0a4a52', 
                margin: 0,
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.in_progress_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              fontSize: '64px', 
              color: '#17a2b8',
              filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.1))'
            }}>
              🔄
            </div>
          </div>
        </div>

        {/* Completadas */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '32px',
          boxShadow: '0 10px 40px rgba(40, 167, 69, 0.15)',
          border: '3px solid #28a745',
          position: 'relative',
          overflow: 'hidden',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }}
        onMouseOver={(e) => {
          e.target.style.transform = 'translateY(-8px) scale(1.02)';
          e.target.style.boxShadow = '0 20px 60px rgba(40, 167, 69, 0.25)';
        }}
        onMouseOut={(e) => {
          e.target.style.transform = 'translateY(0) scale(1)';
          e.target.style.boxShadow = '0 10px 40px rgba(40, 167, 69, 0.15)';
        }}>
          <div style={{
            position: 'absolute',
            top: '-20px',
            right: '-20px',
            width: '100px',
            height: '100px',
            background: 'linear-gradient(135deg, #28a745 0%, #1e7e34 100%)',
            borderRadius: '50%',
            opacity: 0.1
          }}></div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', zIndex: 1 }}>
            <div>
              <div style={{ 
                fontSize: '64px', 
                fontWeight: '900', 
                color: '#28a745', 
                margin: 0,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
                lineHeight: 1
              }}>
                {stats ? stats.completed_tasks : 0}
              </div>
              <div style={{ 
                fontSize: '18px', 
                fontWeight: '700', 
                color: '#155724', 
                margin: '8px 0 4px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Completadas
              </div>
              <div style={{ 
                fontSize: '14px', 
                color: '#0f4a1a', 
                margin: 0,
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.completed_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              fontSize: '64px', 
              color: '#28a745',
              filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.1))'
            }}>
              ✅
            </div>
          </div>
        </div>

        {/* Vencidas */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '32px',
          boxShadow: '0 10px 40px rgba(220, 53, 69, 0.15)',
          border: '3px solid #dc3545',
          position: 'relative',
          overflow: 'hidden',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }}
        onMouseOver={(e) => {
          e.target.style.transform = 'translateY(-8px) scale(1.02)';
          e.target.style.boxShadow = '0 20px 60px rgba(220, 53, 69, 0.25)';
        }}
        onMouseOut={(e) => {
          e.target.style.transform = 'translateY(0) scale(1)';
          e.target.style.boxShadow = '0 10px 40px rgba(220, 53, 69, 0.15)';
        }}>
          <div style={{
            position: 'absolute',
            top: '-20px',
            right: '-20px',
            width: '100px',
            height: '100px',
            background: 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)',
            borderRadius: '50%',
            opacity: 0.1
          }}></div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', zIndex: 1 }}>
            <div>
              <div style={{ 
                fontSize: '64px', 
                fontWeight: '900', 
                color: '#dc3545', 
                margin: 0,
                textShadow: '2px 2px 4px rgba(0,0,0,0.1)',
                lineHeight: 1
              }}>
                {stats ? stats.overdue_tasks : 0}
              </div>
              <div style={{ 
                fontSize: '18px', 
                fontWeight: '700', 
                color: '#721c24', 
                margin: '8px 0 4px',
                textTransform: 'uppercase',
                letterSpacing: '1px'
              }}>
                Vencidas
              </div>
              <div style={{ 
                fontSize: '14px', 
                color: '#5a1a1f', 
                margin: 0,
                fontWeight: '500'
              }}>
                {stats && stats.total_tasks > 0 ? ((stats.overdue_tasks / stats.total_tasks) * 100).toFixed(1) : 0}% del total
              </div>
            </div>
            <div style={{ 
              fontSize: '64px', 
              color: '#dc3545',
              filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.1))'
            }}>
              ⚠️
            </div>
          </div>
        </div>
      </div>

      {/* Sección de Gráficos Mejorada */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: '30px' }}>
        {/* Gráfico de Distribución */}
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '0',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          overflow: 'hidden'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '20px 24px',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>
              📊 Distribución de Tareas
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Estado actual del proyecto
            </p>
          </div>
          <div style={{ padding: '24px', height: '350px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, value, percent }) => 
                    `${name}: ${value} (${(percent * 100).toFixed(1)}%)`
                  }
                  labelLine={false}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value, name) => [value, name]}
                  labelStyle={{ color: '#333' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gráfico por Empresa (solo para admin) */}
        {user?.role === 'admin' && companyStats && Array.isArray(companyStats) && (
          <div style={{
            background: 'white',
            borderRadius: '16px',
            padding: '0',
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            border: '1px solid #f0f0f0',
            overflow: 'hidden'
          }}>
            <div style={{
              background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
              color: 'white',
              padding: '20px 24px',
              borderBottom: '1px solid #f0f0f0'
            }}>
              <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>
                🏢 Tareas por Empresa
              </h3>
              <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
                Comparativa entre empresas
              </p>
            </div>
            <div style={{ padding: '24px' }}>
              <div style={{ height: '450px', marginBottom: '20px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={barData} margin={{ top: 20, right: 30, left: 20, bottom: 100 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis 
                      dataKey="name" 
                      tick={{ fontSize: 12 }}
                      angle={-45}
                      textAnchor="end"
                      height={100}
                      interval={0}
                    />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip 
                      formatter={(value, name) => {
                        const labels = {
                          'total': 'Total de Tareas',
                          'completadas': 'Completadas',
                          'pendientes': 'Pendientes',
                          'en_progreso': 'En Progreso',
                          'vencidas': 'Vencidas'
                        };
                        return [value, labels[name] || name];
                      }}
                      labelStyle={{ color: '#333' }}
                      contentStyle={{
                        backgroundColor: 'white',
                        border: '1px solid #ccc',
                        borderRadius: '8px',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                        padding: '12px'
                      }}
                    />
                    <Bar 
                      dataKey="completadas" 
                      fill="#28a745" 
                      radius={[4, 4, 0, 0]}
                      name="completadas"
                    />
                    <Bar 
                      dataKey="en_progreso" 
                      fill="#17a2b8" 
                      radius={[4, 4, 0, 0]}
                      name="en_progreso"
                    />
                    <Bar 
                      dataKey="pendientes" 
                      fill="#ffc107" 
                      radius={[4, 4, 0, 0]}
                      name="pendientes"
                    />
                    <Bar 
                      dataKey="vencidas" 
                      fill="#dc3545" 
                      radius={[4, 4, 0, 0]}
                      name="vencidas"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              
              {/* Leyenda del gráfico mejorada */}
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '16px',
                padding: '20px',
                background: '#f8f9fa',
                borderRadius: '12px',
                border: '1px solid #e9ecef'
              }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  padding: '12px',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#28a745', 
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(40, 167, 69, 0.3)'
                  }}></div>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: '600', color: '#333' }}>Completadas</div>
                    <div style={{ fontSize: '12px', color: '#666' }}>Tareas finalizadas</div>
                  </div>
                </div>
                
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  padding: '12px',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#17a2b8', 
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(23, 162, 184, 0.3)'
                  }}></div>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: '600', color: '#333' }}>En Progreso</div>
                    <div style={{ fontSize: '12px', color: '#666' }}>Actualmente trabajando</div>
                  </div>
                </div>
                
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  padding: '12px',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#ffc107', 
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(255, 193, 7, 0.3)'
                  }}></div>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: '600', color: '#333' }}>Pendientes</div>
                    <div style={{ fontSize: '12px', color: '#666' }}>Esperando inicio</div>
                  </div>
                </div>
                
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px',
                  padding: '12px',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#dc3545', 
                    borderRadius: '4px',
                    boxShadow: '0 2px 4px rgba(220, 53, 69, 0.3)'
                  }}></div>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: '600', color: '#333' }}>Vencidas</div>
                    <div style={{ fontSize: '12px', color: '#666' }}>Requieren atención</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Información adicional para usuarios regulares */}
      {user?.role !== 'admin' && (
        <div style={{
          background: 'white',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #f0f0f0',
          marginTop: '30px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #6c757d 0%, #495057 100%)',
            color: 'white',
            padding: '16px 20px',
            borderRadius: '12px',
            marginBottom: '20px'
          }}>
            <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>
              ℹ️ Información de tu Empresa
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
              Estadísticas específicas de {user?.company?.name || 'tu empresa'}
            </p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>
                {stats?.total_tasks || 0}
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Total de Tareas</div>
            </div>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>
                {stats?.completed_tasks || 0}
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Completadas</div>
            </div>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffc107' }}>
                {stats?.pending_tasks || 0}
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>Pendientes</div>
            </div>
            <div style={{ textAlign: 'center', padding: '16px' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#17a2b8' }}>
                {stats?.in_progress_tasks || 0}
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>En Progreso</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
