'use client'
import { useState, useEffect } from 'react'
import { getProjects, getEvidences, verifyProject, getCredits } from '@/lib/api'
import { useAuth, withAuth } from '@/app/contexts/AuthContext'

// Add spinner animation CSS
const spinnerKeyframes = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`

function AdminPage() {
  const [projects, setProjects] = useState([])
  const [credits, setCredits] = useState([])
  const [verifications, setVerifications] = useState([])
  const [users, setUsers] = useState([])
  const [activeTab, setActiveTab] = useState('projects')
  const [loading, setLoading] = useState(true)
  const { user, logout, getAuthToken } = useAuth()

  // 🔄 Load projects + evidences + credits
  async function loadData() {
    try {
      const proj = await getProjects()

      // fetch evidences for each project
      const projectsWithEvidences = await Promise.all(
        proj.map(async p => {
          const evidences = await getEvidences(p.id)
          return { ...p, evidences }
        })
      )
      setProjects(projectsWithEvidences)

      // credits for each project owner
      const creditData = await Promise.all(
        proj.map(p => getCredits(p.owner))
      )
      setCredits(creditData)
    } catch (err) {
      console.error("❌ Failed to load data", err)
    } finally {
      setLoading(false)
    }
  }

  // Load users (admin only)
  async function loadUsers() {
    try {
      const token = getAuthToken()
      const response = await fetch('http://localhost:8000/admin/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const usersData = await response.json()
        setUsers(usersData)
      }
    } catch (err) {
      console.error("❌ Failed to load users", err)
    }
  }

  useEffect(() => {
    loadData()
    if (activeTab === 'users') {
      loadUsers()
    }
  }, [activeTab])

  async function handleVerify(evidenceId, projectId, owner) {
    try {
      await verifyProject(evidenceId, { mint_receipt: true, mint_amount: 100 })

      // refresh after successful verification
      await loadData()

      setVerifications(prev => [
        ...prev,
        { id: 'v' + Date.now(), projectId, time: new Date().toISOString() }
      ])
      alert('✅ Evidence verified & credits minted')
    } catch (err) {
      console.error(err)
      alert('❌ Verification failed: ' + err.message)
    }
  }

  if (loading) {
    return (
      <>
        <style dangerouslySetInnerHTML={{ __html: spinnerKeyframes }} />
        <div style={{ 
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '20px',
          fontFamily: 'Arial, sans-serif',
          backgroundColor: '#ffffff'
        }}>
          <div style={{
            textAlign: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            padding: '50px 60px',
            borderRadius: '24px',
            boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
            border: '1px solid rgba(255, 255, 255, 0.3)'
          }}>
            <div style={{
              width: '64px',
              height: '64px',
              border: '4px solid #e5e7eb',
              borderTop: '4px solid #4f46e5',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 20px auto'
            }}></div>
            <p style={{
              color: '#64748b',
              fontSize: '18px',
              fontWeight: '500'
            }}>
              Loading admin dashboard...
            </p>
          </div>
        </div>
      </>
    )
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#ffffff',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.3)'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '20px 0'
          }}>
            <div>
              <h1 style={{
                fontSize: '28px',
                fontWeight: '700',
                color: '#2d3748',
                margin: 0,
                marginBottom: '5px'
              }}>
                Admin Dashboard
              </h1>
              <p style={{
                fontSize: '14px',
                color: '#64748b',
                margin: 0
              }}>
                Welcome back, {user?.username}
              </p>
            </div>
            <button
              onClick={logout}
              style={{
                padding: '10px 20px',
                background: 'linear-gradient(135deg, #dc2626, #b91c1c)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(220, 38, 38, 0.3)',
                transition: 'all 0.2s ease'
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '30px 20px'
      }}>
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderRadius: '16px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          marginBottom: '30px'
        }}>
          <div style={{
            display: 'flex',
            borderBottom: '1px solid #e5e7eb'
          }}>
            {[
              { id: 'projects', name: 'Projects & Verifications', icon: '🏛️' },
              { id: 'users', name: 'User Management', icon: '👥' },
              { id: 'stats', name: 'Statistics', icon: '📊' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  flex: 1,
                  padding: '20px 30px',
                  textAlign: 'center',
                  fontWeight: '600',
                  fontSize: '16px',
                  border: 'none',
                  background: activeTab === tab.id ? 'rgba(79, 70, 229, 0.05)' : 'transparent',
                  color: activeTab === tab.id ? '#4f46e5' : '#64748b',
                  borderBottom: activeTab === tab.id ? '3px solid #4f46e5' : 'none',
                  borderRadius: tab.id === 'projects' ? '16px 0 0 0' : tab.id === 'stats' ? '0 16px 0 0' : '0',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px'
                }}
              >
                <span style={{ fontSize: '18px' }}>{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'projects' && (
            <div style={{ marginBottom: '30px' }}>
              <h2 style={{
                fontSize: '24px',
                fontWeight: '600',
                color: '#2d3748',
                marginBottom: '20px'
              }}>
                Projects & Evidence Verification
              </h2>
              
              {projects.length === 0 ? (
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  padding: '40px',
                  textAlign: 'center'
                }}>
                  <p style={{
                    color: '#64748b',
                    fontSize: '16px'
                  }}>
                    No projects found
                  </p>
                </div>
              ) : (
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  overflow: 'hidden'
                }}>
                  <div>
                    {projects.map((project, index) => (
                      <div key={project.id} style={{
                        padding: '25px 30px',
                        borderBottom: index < projects.length - 1 ? '1px solid #e5e7eb' : 'none'
                      }}>
                        <div style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          marginBottom: '15px'
                        }}>
                          <div style={{ flex: 1 }}>
                            <h3 style={{
                              fontSize: '18px',
                              fontWeight: '600',
                              color: '#2d3748',
                              margin: 0,
                              marginBottom: '5px'
                            }}>
                              {project.name}
                            </h3>
                            <p style={{
                              fontSize: '14px',
                              color: '#64748b',
                              margin: 0,
                              marginBottom: '3px'
                            }}>
                              {project.location} • {project.hectares} hectares
                            </p>
                            <p style={{
                              fontSize: '12px',
                              color: '#9ca3af',
                              margin: 0,
                              fontFamily: 'monospace'
                            }}>
                              Owner: {project.owner}
                            </p>
                          </div>
                          <div style={{ textAlign: 'right' }}>
                            <p style={{
                              fontSize: '14px',
                              fontWeight: '600',
                              color: '#2d3748',
                              margin: 0,
                              marginBottom: '3px'
                            }}>
                              {project.evidences?.length || 0} Evidence(s)
                            </p>
                            <p style={{
                              fontSize: '12px',
                              color: '#64748b',
                              margin: 0
                            }}>
                              {project.totalIssuedCredits || 0} Credits Issued
                            </p>
                          </div>
                        </div>
                        
                        {project.evidences && project.evidences.length > 0 && (
                          <div style={{ marginTop: '20px' }}>
                            <h4 style={{
                              fontSize: '14px',
                              fontWeight: '600',
                              color: '#2d3748',
                              marginBottom: '10px'
                            }}>
                              Evidence to Verify:
                            </h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                              {project.evidences.filter(e => !e.verified).map(evidence => (
                                <div key={evidence.evidenceId} style={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  justifyContent: 'space-between',
                                  backgroundColor: '#fef3c7',
                                  padding: '15px',
                                  borderRadius: '12px',
                                  border: '1px solid #fbbf24'
                                }}>
                                  <div>
                                    <p style={{
                                      fontSize: '14px',
                                      fontWeight: '600',
                                      color: '#92400e',
                                      margin: 0,
                                      marginBottom: '5px'
                                    }}>
                                      Evidence #{evidence.evidenceId}
                                    </p>
                                    <p style={{
                                      fontSize: '12px',
                                      color: '#b45309',
                                      margin: 0
                                    }}>
                                      Uploader: {evidence.uploader} • GPS: {evidence.gps} • CO2: {evidence.co2}
                                    </p>
                                  </div>
                                  <button
                                    onClick={() => handleVerify(evidence.evidenceId, project.id, project.owner)}
                                    style={{
                                      padding: '8px 16px',
                                      background: 'linear-gradient(135deg, #10b981, #059669)',
                                      color: 'white',
                                      border: 'none',
                                      borderRadius: '8px',
                                      fontSize: '14px',
                                      fontWeight: '600',
                                      cursor: 'pointer',
                                      boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)',
                                      transition: 'all 0.2s ease'
                                    }}
                                  >
                                    Verify & Mint
                                  </button>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'users' && (
            <div style={{ marginBottom: '30px' }}>
              <h2 style={{
                fontSize: '24px',
                fontWeight: '600',
                color: '#2d3748',
                marginBottom: '20px'
              }}>
                User Management
              </h2>
              
              {users.length === 0 ? (
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  padding: '40px',
                  textAlign: 'center'
                }}>
                  <p style={{
                    color: '#64748b',
                    fontSize: '16px'
                  }}>
                    No users found
                  </p>
                </div>
              ) : (
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  overflow: 'hidden'
                }}>
                  <div style={{ padding: '20px 30px' }}>
                    <div style={{ overflowX: 'auto' }}>
                      <table style={{
                        width: '100%',
                        borderCollapse: 'collapse'
                      }}>
                        <thead>
                          <tr style={{ backgroundColor: '#f8fafc' }}>
                            <th style={{
                              padding: '15px 20px',
                              textAlign: 'left',
                              fontSize: '12px',
                              fontWeight: '600',
                              color: '#64748b',
                              textTransform: 'uppercase',
                              letterSpacing: '1px',
                              borderBottom: '1px solid #e5e7eb'
                            }}>
                              User
                            </th>
                            <th style={{
                              padding: '15px 20px',
                              textAlign: 'left',
                              fontSize: '12px',
                              fontWeight: '600',
                              color: '#64748b',
                              textTransform: 'uppercase',
                              letterSpacing: '1px',
                              borderBottom: '1px solid #e5e7eb'
                            }}>
                              Role
                            </th>
                            <th style={{
                              padding: '15px 20px',
                              textAlign: 'left',
                              fontSize: '12px',
                              fontWeight: '600',
                              color: '#64748b',
                              textTransform: 'uppercase',
                              letterSpacing: '1px',
                              borderBottom: '1px solid #e5e7eb'
                            }}>
                              Organization
                            </th>
                            <th style={{
                              padding: '15px 20px',
                              textAlign: 'left',
                              fontSize: '12px',
                              fontWeight: '600',
                              color: '#64748b',
                              textTransform: 'uppercase',
                              letterSpacing: '1px',
                              borderBottom: '1px solid #e5e7eb'
                            }}>
                              Status
                            </th>
                            <th style={{
                              padding: '15px 20px',
                              textAlign: 'left',
                              fontSize: '12px',
                              fontWeight: '600',
                              color: '#64748b',
                              textTransform: 'uppercase',
                              letterSpacing: '1px',
                              borderBottom: '1px solid #e5e7eb'
                            }}>
                              Created
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {users.map((userItem, index) => (
                            <tr key={userItem.id} style={{
                              borderBottom: index < users.length - 1 ? '1px solid #f1f5f9' : 'none'
                            }}>
                              <td style={{
                                padding: '20px',
                                whiteSpace: 'nowrap'
                              }}>
                                <div>
                                  <div style={{
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    color: '#2d3748',
                                    marginBottom: '3px'
                                  }}>
                                    {userItem.username}
                                  </div>
                                  <div style={{
                                    fontSize: '14px',
                                    color: '#64748b'
                                  }}>
                                    {userItem.email}
                                  </div>
                                </div>
                              </td>
                              <td style={{
                                padding: '20px',
                                whiteSpace: 'nowrap'
                              }}>
                                <span style={{
                                  display: 'inline-flex',
                                  padding: '4px 12px',
                                  fontSize: '12px',
                                  fontWeight: '600',
                                  borderRadius: '20px',
                                  backgroundColor: userItem.role === 'admin' ? '#fef2f2' : 
                                                  userItem.role === 'ngo' ? '#eff6ff' : '#f8fafc',
                                  color: userItem.role === 'admin' ? '#dc2626' : 
                                         userItem.role === 'ngo' ? '#2563eb' : '#64748b'
                                }}>
                                  {userItem.role.toUpperCase()}
                                </span>
                              </td>
                              <td style={{
                                padding: '20px',
                                whiteSpace: 'nowrap',
                                fontSize: '14px',
                                color: '#64748b'
                              }}>
                                {userItem.organization_name || '-'}
                              </td>
                              <td style={{
                                padding: '20px',
                                whiteSpace: 'nowrap'
                              }}>
                                <span style={{
                                  display: 'inline-flex',
                                  padding: '4px 12px',
                                  fontSize: '12px',
                                  fontWeight: '600',
                                  borderRadius: '20px',
                                  backgroundColor: userItem.is_active ? '#f0fdf4' : '#fef2f2',
                                  color: userItem.is_active ? '#16a34a' : '#dc2626'
                                }}>
                                  {userItem.is_active ? 'Active' : 'Inactive'}
                                </span>
                              </td>
                              <td style={{
                                padding: '20px',
                                whiteSpace: 'nowrap',
                                fontSize: '14px',
                                color: '#64748b'
                              }}>
                                {new Date(userItem.created_at).toLocaleDateString()}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'stats' && (
            <div style={{ marginBottom: '30px' }}>
              <h2 style={{
                fontSize: '24px',
                fontWeight: '600',
                color: '#2d3748',
                marginBottom: '20px'
              }}>
                Statistics
              </h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: '20px'
              }}>
                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  overflow: 'hidden'
                }}>
                  <div style={{ padding: '25px' }}>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <div style={{ 
                        flexShrink: 0,
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginRight: '15px'
                      }}>
                        <span style={{ fontSize: '24px' }}>🏛️</span>
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#64748b',
                          marginBottom: '5px',
                          textTransform: 'uppercase',
                          letterSpacing: '1px'
                        }}>
                          Total Projects
                        </div>
                        <div style={{
                          fontSize: '28px',
                          fontWeight: '700',
                          color: '#2d3748'
                        }}>
                          {projects.length}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  overflow: 'hidden'
                }}>
                  <div style={{ padding: '25px' }}>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <div style={{ 
                        flexShrink: 0,
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        background: 'linear-gradient(135deg, #10b981, #059669)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginRight: '15px'
                      }}>
                        <span style={{ fontSize: '24px' }}>👥</span>
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#64748b',
                          marginBottom: '5px',
                          textTransform: 'uppercase',
                          letterSpacing: '1px'
                        }}>
                          Total Users
                        </div>
                        <div style={{
                          fontSize: '28px',
                          fontWeight: '700',
                          color: '#2d3748'
                        }}>
                          {users.length}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(20px)',
                  WebkitBackdropFilter: 'blur(20px)',
                  borderRadius: '16px',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  overflow: 'hidden'
                }}>
                  <div style={{ padding: '25px' }}>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <div style={{ 
                        flexShrink: 0,
                        width: '50px',
                        height: '50px',
                        borderRadius: '12px',
                        background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginRight: '15px'
                      }}>
                        <span style={{ fontSize: '24px' }}>✅</span>
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{
                          fontSize: '14px',
                          fontWeight: '600',
                          color: '#64748b',
                          marginBottom: '5px',
                          textTransform: 'uppercase',
                          letterSpacing: '1px'
                        }}>
                          Verified Evidence
                        </div>
                        <div style={{
                          fontSize: '28px',
                          fontWeight: '700',
                          color: '#2d3748'
                        }}>
                          {projects.reduce((total, p) => total + (p.evidences?.filter(e => e.verified).length || 0), 0)}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// Export with admin authentication required
export default withAuth(AdminPage, 'admin')