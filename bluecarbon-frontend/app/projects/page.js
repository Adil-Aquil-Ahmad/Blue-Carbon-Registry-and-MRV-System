'use client'
import { useEffect, useState } from 'react'
import { getMyProjects, getAllProjectsLimited, getEvidences, deleteProject } from '@/lib/api'
import { useAuth } from '@/app/contexts/AuthContext'
import Link from 'next/link'

// Add spinner animation CSS
const spinnerKeyframes = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`

export default function ProjectList() {
  const [myProjects, setMyProjects] = useState([])
  const [allProjects, setAllProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('my')
  const [deleteLoading, setDeleteLoading] = useState(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null)
  const { user } = useAuth()

  // Delete project function
  async function handleDeleteProject(projectId) {
    setDeleteLoading(projectId)
    try {
      await deleteProject(projectId)
      // Remove the project from the local state
      setMyProjects(prev => prev.filter(p => p.id !== projectId))
      setShowDeleteConfirm(null)
      // Optional: Show success notification
      alert('Project deleted successfully!')
    } catch (err) {
      console.error('Error deleting project:', err)
      alert(`Error deleting project: ${err.message}`)
    } finally {
      setDeleteLoading(null)
    }
  }

  // Load user's own projects with full details (filtered by user's wallet address)
  async function loadMyProjects() {
    try {
      const projects = await getMyProjects()
      // Filter projects to only show ones owned by the current NGO's wallet address
      const filteredProjects = user?.wallet_address 
        ? projects.filter(p => p.owner === user.wallet_address)
        : projects
      const projectsWithDetails = await Promise.all(
        filteredProjects.map(async (p) => {
          const evidences = await getEvidences(p.id)
          return {
            ...p,
            evidences,
            verified: p.totalIssuedCredits > 0,
          }
        })
      )
      setMyProjects(projectsWithDetails)
    } catch (err) {
      console.error('Error loading my projects:', err)
      setError(err.message)
    }
  }

  // Load all projects with limited data for other users' projects (excluding user's own)
  async function loadAllProjects() {
    try {
      const projects = await getAllProjectsLimited()
      // Filter projects to exclude ones owned by the current NGO's wallet address
      const filteredProjects = user?.wallet_address 
        ? projects.filter(p => p.owner !== user.wallet_address)
        : projects
      setAllProjects(filteredProjects)
    } catch (err) {
      console.error('Error loading all projects:', err)
      setError(err.message)
    }
  }

  useEffect(() => {
    if (user) {
      Promise.all([loadMyProjects(), loadAllProjects()])
        .finally(() => setLoading(false))
    }
  }, [user])

  if (!user) {
    return (
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
          width: '100%',
          maxWidth: '500px',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          padding: '50px 60px',
          borderRadius: '24px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          textAlign: 'center'
        }}>
          <div style={{
            width: '80px',
            height: '80px',
            background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 30px auto'
          }}>
            <svg style={{ width: '40px', height: '40px', color: 'white' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 style={{
            fontSize: '28px',
            fontWeight: '600',
            marginBottom: '15px',
            color: '#2d3748'
          }}>
            Authentication Required
          </h2>
          <p style={{
            fontSize: '16px',
            marginBottom: '30px',
            color: '#64748b'
          }}>
            Please log in to view and manage your carbon projects.
          </p>
          <Link href="/auth/login" style={{
            display: 'inline-block',
            background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
            color: 'white',
            textDecoration: 'none',
            padding: '14px 28px',
            borderRadius: '12px',
            fontSize: '16px',
            fontWeight: '600',
            boxShadow: '0 4px 15px rgba(79, 70, 229, 0.3)',
            transition: 'all 0.2s ease'
          }}>
            Login to Continue
          </Link>
        </div>
      </div>
    )
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
              Loading projects...
            </p>
          </div>
        </div>
      </>
    )
  }
  
  if (error) {
    return (
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
          width: '100%',
          maxWidth: '500px',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          padding: '50px 60px',
          borderRadius: '24px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          textAlign: 'center'
        }}>
          <div style={{
            width: '80px',
            height: '80px',
            backgroundColor: '#fef2f2',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 30px auto'
          }}>
            <svg style={{ width: '40px', height: '40px', color: '#dc2626' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 style={{
            fontSize: '24px',
            fontWeight: '600',
            marginBottom: '15px',
            color: '#dc2626'
          }}>
            Error Loading Projects
          </h2>
          <p style={{
            fontSize: '16px',
            color: '#dc2626'
          }}>
            {error}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#ffffff',
      fontFamily: 'Arial, sans-serif',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        {/* Header Section */}
        <div style={{ marginBottom: '40px' }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between', 
            marginBottom: '20px',
            flexWrap: 'wrap',
            gap: '20px'
          }}>
            <div>
              <h1 style={{
                fontSize: '36px',
                fontWeight: '700',
                background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                marginBottom: '10px'
              }}>
                Carbon Projects Dashboard
              </h1>
              <p style={{
                color: '#64748b',
                fontSize: '18px',
                margin: 0
              }}>
                Manage and monitor your blue carbon initiatives
              </p>
            </div>
            <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
              <Link href="/upload" style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                background: 'linear-gradient(135deg, #10b981, #059669)',
                color: 'white',
                textDecoration: 'none',
                padding: '12px 20px',
                borderRadius: '12px',
                fontSize: '16px',
                fontWeight: '600',
                boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)',
                transition: 'all 0.2s ease'
              }}>
                <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Upload Evidence
              </Link>
              {(user?.role === 'ngo' || user?.role === 'admin') && (
                <Link href="/projects/new" style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                  color: 'white',
                  textDecoration: 'none',
                  padding: '12px 20px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: '600',
                  boxShadow: '0 4px 15px rgba(79, 70, 229, 0.3)',
                  transition: 'all 0.2s ease'
                }}>
                  <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  New Project
                </Link>
              )}
            </div>
          </div>
        </div>
        
        {/* Tab Navigation */}
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderRadius: '16px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          marginBottom: '40px'
        }}>
          <div style={{ display: 'flex', borderBottom: '1px solid #e5e7eb' }}>
            <button
              onClick={() => setActiveTab('my')}
              style={{
                flex: 1,
                padding: '20px 30px',
                textAlign: 'center',
                fontWeight: '600',
                fontSize: '16px',
                border: 'none',
                background: activeTab === 'my' ? 'rgba(79, 70, 229, 0.05)' : 'transparent',
                color: activeTab === 'my' ? '#4f46e5' : '#64748b',
                borderBottom: activeTab === 'my' ? '3px solid #4f46e5' : 'none',
                borderTopLeftRadius: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                My Projects
                <span style={{
                  backgroundColor: '#4f46e5',
                  color: 'white',
                  fontSize: '12px',
                  fontWeight: '600',
                  padding: '4px 8px',
                  borderRadius: '20px'
                }}>
                  {myProjects.length}
                </span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('all')}
              style={{
                flex: 1,
                padding: '20px 30px',
                textAlign: 'center',
                fontWeight: '600',
                fontSize: '16px',
                border: 'none',
                background: activeTab === 'all' ? 'rgba(79, 70, 229, 0.05)' : 'transparent',
                color: activeTab === 'all' ? '#4f46e5' : '#64748b',
                borderBottom: activeTab === 'all' ? '3px solid #4f46e5' : 'none',
                borderTopRightRadius: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                <svg style={{ width: '20px', height: '20px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Other Projects
                <span style={{
                  backgroundColor: '#64748b',
                  color: 'white',
                  fontSize: '12px',
                  fontWeight: '600',
                  padding: '4px 8px',
                  borderRadius: '20px'
                }}>
                  {allProjects.length}
                </span>
              </div>
            </button>
          </div>
        </div>

      {/* My Projects Tab */}
      {activeTab === 'my' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl p-6 border border-blue-100">
            <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              My Projects
            </h2>
            <p className="text-gray-600">
              {user?.wallet_address 
                ? (
                  <span className="flex items-center gap-2">
                    <span>Projects owned by your wallet:</span>
                    <code className="bg-white px-2 py-1 rounded border text-sm font-mono">{user.wallet_address}</code>
                  </span>
                )
                : 'Projects you own - full details available'
              }
            </p>
          </div>
          
          {myProjects.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-700 mb-2">No Projects Yet</h3>
              <p className="text-gray-500 mb-6">You haven't created any carbon projects yet. Start your first project to begin your carbon impact journey.</p>
              <Link href="/projects/new" className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 transform hover:scale-105">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Create Your First Project
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {myProjects.map((p) => (
                <div key={p.id} className="group relative">
                  <Link href={`/projects/${p.id}`} className="block">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-xl hover:border-blue-200 transition-all duration-300 transform group-hover:scale-105">
                      <div className="flex items-start justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800 group-hover:text-blue-600 transition-colors duration-200">
                          {p.name}
                        </h3>
                        {p.verified ? (
                          <span className="inline-flex items-center gap-1 bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-1 rounded-full">
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                            Verified
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-1 rounded-full">
                            <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Pending
                          </span>
                        )}
                      </div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center gap-2 text-gray-600">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                          <span className="text-sm">{p.location}</span>
                          <span className="text-gray-400">•</span>
                          <span className="text-sm font-medium">{p.hectares} ha</span>
                        </div>
                        
                        <div className="flex items-center gap-2 text-gray-600">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          <span className="text-sm font-mono text-xs">{p.owner.slice(0, 6)}...{p.owner.slice(-4)}</span>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 pt-3 border-t border-gray-100">
                          <div className="text-center">
                            <div className="text-lg font-bold text-blue-600">{p.totalIssuedCredits}</div>
                            <div className="text-xs text-gray-500">Credits</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-green-600">{p.evidences.length}</div>
                            <div className="text-xs text-gray-500">Evidence{p.evidences.length !== 1 ? 's' : ''}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                  
                  {/* Delete Button */}
                  <button
                    onClick={(e) => {
                      e.preventDefault()
                      e.stopPropagation()
                      setShowDeleteConfirm(p.id)
                    }}
                    className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg z-10"
                    title="Delete Project"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Other Projects Tab */}
      {activeTab === 'all' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-gray-50 to-slate-50 rounded-xl p-6 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-2">
              <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Other Projects
            </h2>
            <p className="text-gray-600">
              {user.role === 'admin' 
                ? 'All projects in the registry - full administrative access available' 
                : 'Projects from other NGOs - limited information displayed for privacy'
              }
            </p>
          </div>
          
          {allProjects.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-700 mb-2">No Other Projects</h3>
              <p className="text-gray-500">There are currently no projects from other organizations in the registry.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {allProjects.map((p) => (
                <div key={p.id} className="group">
                  {user.role === 'admin' ? (
                    // Full view for admin users
                    <Link href={`/projects/${p.id}`} className="block">
                      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-xl hover:border-blue-200 transition-all duration-300 transform group-hover:scale-105">
                        <div className="flex items-start justify-between mb-4">
                          <h3 className="text-lg font-bold text-gray-800 group-hover:text-blue-600 transition-colors duration-200">
                            {p.name}
                          </h3>
                          {p.totalIssuedCredits > 0 ? (
                            <span className="inline-flex items-center gap-1 bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-1 rounded-full">
                              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              </svg>
                              Verified
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-1 rounded-full">
                              <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                              </svg>
                              Pending
                            </span>
                          )}
                        </div>
                        
                        <div className="space-y-3">
                          <div className="flex items-center gap-2 text-gray-600">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span className="text-sm">{p.location}</span>
                            <span className="text-gray-400">•</span>
                            <span className="text-sm font-medium">{p.hectares} ha</span>
                          </div>
                          
                          <div className="flex items-center gap-2 text-gray-600">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            <span className="text-sm font-mono text-xs">{p.owner.slice(0, 6)}...{p.owner.slice(-4)}</span>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4 pt-3 border-t border-gray-100">
                            <div className="text-center">
                              <div className="text-lg font-bold text-blue-600">{p.totalIssuedCredits}</div>
                              <div className="text-xs text-gray-500">Credits</div>
                            </div>
                            <div className="text-center">
                              <div className="text-lg font-bold text-green-600">{p.evidences?.length || 0}</div>
                              <div className="text-xs text-gray-500">Evidence{(p.evidences?.length || 0) !== 1 ? 's' : ''}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </Link>
                  ) : (
                    // Limited view for NGO users - only show address
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-all duration-300">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-gray-800">Project #{p.id}</h3>
                        <span className="inline-flex items-center gap-1 bg-gray-100 text-gray-600 text-xs font-semibold px-2.5 py-1 rounded-full">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                          </svg>
                          Limited View
                        </span>
                      </div>
                      
                      <div className="space-y-3">
                        <div className="bg-gray-50 rounded-lg p-4">
                          <div className="text-sm text-gray-600 mb-1">Owner Address</div>
                          <div className="font-mono text-sm bg-white border rounded px-3 py-2 break-all">
                            {p.owner}
                          </div>
                        </div>
                        
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                          <div className="flex items-center gap-2 text-blue-700 text-sm">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>Limited access - only owner address visible to maintain privacy</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.732 15.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Delete Project</h3>
                <p className="text-gray-600">This action cannot be undone</p>
              </div>
            </div>
            
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete <strong>Project #{showDeleteConfirm}</strong>? 
              This will permanently remove all associated evidence data.
            </p>
            
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
                disabled={deleteLoading}
              >
                Cancel
              </button>
              <button
                onClick={() => handleDeleteProject(showDeleteConfirm)}
                disabled={deleteLoading === showDeleteConfirm}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {deleteLoading === showDeleteConfirm ? (
                  <>
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Deleting...
                  </>
                ) : (
                  'Delete Project'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  )
}
