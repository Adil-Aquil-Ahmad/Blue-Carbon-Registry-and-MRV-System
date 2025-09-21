'use client'
import { useState, useEffect } from 'react'
import { getProjects, getEvidences, verifyProject, getCredits } from '@/lib/api'
import { useAuth, withAuth } from '@/app/contexts/AuthContext'

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
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="text-sm text-gray-600">Welcome back, {user?.username}</p>
            </div>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'projects', name: 'Projects & Verifications', icon: '🏛️' },
              { id: 'users', name: 'User Management', icon: '👥' },
              { id: 'stats', name: 'Statistics', icon: '📊' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === 'projects' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Projects & Evidence Verification</h2>
              
              {projects.length === 0 ? (
                <div className="bg-white rounded-lg p-6 text-center">
                  <p className="text-gray-500">No projects found</p>
                </div>
              ) : (
                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                  <ul className="divide-y divide-gray-200">
                    {projects.map(project => (
                      <li key={project.id} className="px-6 py-4">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <h3 className="text-lg font-medium text-gray-900">{project.name}</h3>
                            <p className="text-sm text-gray-500">{project.location} • {project.hectares} hectares</p>
                            <p className="text-xs text-gray-400">Owner: {project.owner}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-medium text-gray-900">
                              {project.evidences?.length || 0} Evidence(s)
                            </p>
                            <p className="text-xs text-gray-500">
                              {project.totalIssuedCredits || 0} Credits Issued
                            </p>
                          </div>
                        </div>
                        
                        {project.evidences && project.evidences.length > 0 && (
                          <div className="mt-4">
                            <h4 className="text-sm font-medium text-gray-900 mb-2">Evidence to Verify:</h4>
                            <div className="space-y-2">
                              {project.evidences.filter(e => !e.verified).map(evidence => (
                                <div key={evidence.evidenceId} className="flex items-center justify-between bg-yellow-50 p-3 rounded-md">
                                  <div>
                                    <p className="text-sm font-medium">Evidence #{evidence.evidenceId}</p>
                                    <p className="text-xs text-gray-500">
                                      Uploader: {evidence.uploader} • GPS: {evidence.gps} • CO2: {evidence.co2}
                                    </p>
                                  </div>
                                  <button
                                    onClick={() => handleVerify(evidence.evidenceId, project.id, project.owner)}
                                    className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                                  >
                                    Verify & Mint
                                  </button>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {activeTab === 'users' && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">User Management</h2>
              
              {users.length === 0 ? (
                <div className="bg-white rounded-lg p-6 text-center">
                  <p className="text-gray-500">No users found</p>
                </div>
              ) : (
                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                  <div className="px-4 py-5 sm:p-6">
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Organization</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {users.map(user => (
                            <tr key={user.id}>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div>
                                  <div className="text-sm font-medium text-gray-900">{user.username}</div>
                                  <div className="text-sm text-gray-500">{user.email}</div>
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                  user.role === 'admin' ? 'bg-red-100 text-red-800' :
                                  user.role === 'ngo' ? 'bg-blue-100 text-blue-800' :
                                  'bg-gray-100 text-gray-800'
                                }`}>
                                  {user.role.toUpperCase()}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {user.organization_name || '-'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                  user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                }`}>
                                  {user.is_active ? 'Active' : 'Inactive'}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {new Date(user.created_at).toLocaleDateString()}
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
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-gray-900">Statistics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <span className="text-2xl">🏛️</span>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Total Projects
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {projects.length}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <span className="text-2xl">👥</span>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Total Users
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {users.length}
                          </dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <span className="text-2xl">✅</span>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">
                            Verified Evidence
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">
                            {projects.reduce((total, p) => total + (p.evidences?.filter(e => e.verified).length || 0), 0)}
                          </dd>
                        </dl>
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