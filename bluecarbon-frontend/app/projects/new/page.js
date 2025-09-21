'use client'
import { useState } from 'react'
import { registerProject } from '@/lib/api'
import { useRouter } from 'next/navigation'

export default function NewProject() {
  const [form, setForm] = useState({
    name: "",
    location: "",
    hectares: 0,
    owner: "",
    metadata: ""
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      await registerProject(form)
      router.push("/projects")
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#ffffff',
      fontFamily: 'Arial, sans-serif',
      padding: '40px 20px'
    }}>
      <div style={{
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        {/* Header */}
        <div style={{ marginBottom: '40px', textAlign: 'center' }}>
          <h1 style={{
            fontSize: '32px',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '10px'
          }}>
            Register New Project
          </h1>
          <p style={{
            color: '#64748b',
            fontSize: '16px',
            margin: 0
          }}>
            Create a new blue carbon project in the registry
          </p>
        </div>

        {/* Form Card */}
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderRadius: '24px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          padding: '40px 50px'
        }}>
          {error && (
            <div style={{
              backgroundColor: '#fef2f2',
              color: '#dc2626',
              padding: '15px',
              borderRadius: '12px',
              marginBottom: '25px',
              fontSize: '15px',
              border: '1px solid #fecaca',
              fontWeight: '500'
            }}>
              Error: {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Project Name *
              </label>
              <input
                name="name"
                type="text"
                placeholder="Enter project name"
                value={form.name}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa'
                }}
              />
            </div>

            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Location *
              </label>
              <input
                name="location"
                type="text"
                placeholder="Enter project location"
                value={form.location}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa'
                }}
              />
            </div>

            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Area (Hectares) *
              </label>
              <input
                name="hectares"
                type="number"
                placeholder="Enter area in hectares"
                value={form.hectares}
                onChange={handleChange}
                min="0"
                step="0.01"
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa'
                }}
              />
            </div>

            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Owner Wallet Address *
              </label>
              <input
                name="owner"
                type="text"
                placeholder="Enter blockchain wallet address"
                value={form.owner}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa',
                  fontFamily: 'monospace'
                }}
              />
            </div>

            <div style={{ marginBottom: '30px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Project Metadata *
              </label>
              <textarea
                name="metadata"
                placeholder="Enter project metadata (JSON format or description)"
                value={form.metadata}
                onChange={handleChange}
                required
                rows={4}
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa',
                  resize: 'vertical',
                  minHeight: '120px'
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
              <button
                type="submit"
                disabled={loading}
                style={{
                  flex: 1,
                  background: loading ? '#9ca3af' : 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                  color: 'white',
                  border: 'none',
                  padding: '16px 24px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: loading ? 'none' : '0 4px 15px rgba(79, 70, 229, 0.3)'
                }}
              >
                {loading ? 'Creating Project...' : 'Create Project'}
              </button>
              
              <button
                type="button"
                onClick={() => router.push('/projects')}
                style={{
                  background: 'linear-gradient(135deg, #64748b, #475569)',
                  color: 'white',
                  border: 'none',
                  padding: '16px 24px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 4px 15px rgba(100, 116, 139, 0.3)'
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
