'use client'
import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { getProjects } from '@/lib/api'

// ethers v6 imports
import { ethers } from 'ethers'
import { keccak256, toUtf8Bytes } from 'ethers'

// ABI
import BlueCarbonRegistry from '@/artifacts/contracts/BlueCarbonRegistry.sol/BlueCarbonRegistry.json'

const REGISTRY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512" // replace with deployed contract address

// Simple map component using Leaflet
const MapSelector = ({ coordinates, onCoordinatesChange }) => {
  const [mapLoaded, setMapLoaded] = useState(false)
  const [showMap, setShowMap] = useState(false)

  useEffect(() => {
    if (showMap && !mapLoaded) {
      // Load Leaflet CSS and JS dynamically
      const loadLeaflet = async () => {
        if (typeof window !== 'undefined' && !window.L) {
          // Load CSS
          const link = document.createElement('link')
          link.rel = 'stylesheet'
          link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
          document.head.appendChild(link)

          // Load JS
          const script = document.createElement('script')
          script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
          script.onload = () => {
            setMapLoaded(true)
            initializeMap()
          }
          document.head.appendChild(script)
        } else if (window.L) {
          setMapLoaded(true)
          initializeMap()
        }
      }

      loadLeaflet()
    }
  }, [showMap])

  const initializeMap = () => {
    if (!window.L) return

    // Default coordinates (center of world)
    const defaultLat = coordinates ? parseFloat(coordinates.split(',')[0]) : 0
    const defaultLng = coordinates ? parseFloat(coordinates.split(',')[1]) : 0

    const map = window.L.map('map-container').setView([defaultLat, defaultLng], 2)

    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    let marker = null
    if (coordinates) {
      marker = window.L.marker([defaultLat, defaultLng]).addTo(map)
    }

    map.on('click', (e) => {
      const { lat, lng } = e.latlng
      const coordString = `${lat.toFixed(6)},${lng.toFixed(6)}`
      onCoordinatesChange(coordString)

      if (marker) {
        map.removeLayer(marker)
      }
      marker = window.L.marker([lat, lng]).addTo(map)
    })
  }

  return (
    <div>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
        <button
          type="button"
          onClick={() => setShowMap(!showMap)}
          style={{
            padding: '8px 16px',
            background: 'linear-gradient(135deg, #10b981, #059669)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
        >
          {showMap ? '📍 Hide Map' : '🗺️ Select from Map'}
        </button>
        
        {coordinates && (
          <button
            type="button"
            onClick={() => onCoordinatesChange('')}
            style={{
              padding: '8px 16px',
              background: 'linear-gradient(135deg, #dc2626, #b91c1c)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '14px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            Clear Location
          </button>
        )}
      </div>

      {showMap && (
        <div style={{
          marginBottom: '15px',
          border: '2px solid #e5e7eb',
          borderRadius: '12px',
          overflow: 'hidden'
        }}>
          <div 
            id="map-container" 
            style={{ 
              height: '300px', 
              width: '100%',
              backgroundColor: '#f3f4f6'
            }}
          >
            {!mapLoaded && (
              <div style={{
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#64748b',
                fontSize: '16px'
              }}>
                Loading map...
              </div>
            )}
          </div>
          <div style={{
            padding: '10px 15px',
            backgroundColor: '#f8fafc',
            fontSize: '13px',
            color: '#64748b',
            borderTop: '1px solid #e5e7eb'
          }}>
            💡 Click anywhere on the map to select coordinates
          </div>
        </div>
      )}
    </div>
  )
}

export default function UploadPage() {
  const search = useSearchParams()
  const router = useRouter()
  const queryProjectId = search.get('projectId') || ''

  const [projectId, setProjectId] = useState(queryProjectId)
  const [projects, setProjects] = useState([])
  const [uploader, setUploader] = useState('')
  const [gps, setGps] = useState('')
  // Removed co2 state - now calculated automatically by AI
  // Removed files state - now using specific before/after image uploads
  const [status, setStatus] = useState('')
  
  // New fields for AI verification - separate before/after images
  const [beforeImage, setBeforeImage] = useState(null)
  const [afterImage, setAfterImage] = useState(null)
  const [projectAreaHectares, setProjectAreaHectares] = useState('')
  const [timePeriodYears, setTimePeriodYears] = useState('1.0')
  const [ecosystemType, setEcosystemType] = useState('mangrove')
  
  // Estimation state
  const [estimation, setEstimation] = useState(null)
  const [estimationLoading, setEstimationLoading] = useState(false)
  const [showEstimation, setShowEstimation] = useState(false)

  useEffect(() => {
    getProjects()
      .then(setProjects)
      .catch(err => setStatus("Failed to fetch projects: " + err.message))
  }, [])

  // Function to estimate carbon credits
  async function estimateCredits() {
    if (!projectAreaHectares || projectAreaHectares <= 0) {
      setStatus('Please enter a valid project area to get estimation')
      return
    }

    setEstimationLoading(true)
    setEstimation(null)

    try {
      const formData = new FormData()
      formData.append('project_area_hectares', projectAreaHectares)
      formData.append('time_period_years', timePeriodYears)
      formData.append('ecosystem_type', ecosystemType)

      // Add images if available (for AI analysis)
      if (beforeImage && afterImage) {
        // Both images available - AI analysis
        formData.append('before_image', beforeImage)
        formData.append('after_image', afterImage)
      } else if (beforeImage) {
        // Only before image
        formData.append('before_image', beforeImage)
      } else if (afterImage) {
        // Only after image  
        formData.append('after_image', afterImage)
      }

      const response = await fetch('http://127.0.0.1:8000/estimate-carbon-credits', {
        method: 'POST',
        body: formData
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.detail || 'Estimation failed')
      }

      setEstimation(result)
      setShowEstimation(true)

    } catch (error) {
      console.error('Estimation error:', error)
      setStatus('Estimation failed: ' + error.message)
    } finally {
      setEstimationLoading(false)
    }
  }

  // Auto-estimate when key parameters change
  useEffect(() => {
    if (projectAreaHectares && parseFloat(projectAreaHectares) > 0) {
      const timer = setTimeout(() => {
        estimateCredits()
      }, 1000) // Debounce for 1 second

      return () => clearTimeout(timer)
    }
  }, [projectAreaHectares, timePeriodYears, ecosystemType, beforeImage, afterImage])

  async function handleSubmit(e) {
    e.preventDefault()

    if (!projectId) {
      setStatus('Error: No project selected')
      return
    }

    setStatus('Uploading evidence...')

    try {
      // --- Step 1: upload files to backend ---
      const form = new FormData()
      form.append('project_id', projectId)
      form.append('uploader', uploader)
      form.append('gps', gps)
      // CO2 will be calculated automatically by AI analysis
      
      // Add new AI verification fields
      // Determine evidence type based on which images are uploaded
      let evidenceType = 'general'
      if (beforeImage && afterImage) {
        evidenceType = 'before_after_pair'
      } else if (beforeImage) {
        evidenceType = 'before'
      } else if (afterImage) {
        evidenceType = 'after'
      }
      
      form.append('evidence_type', evidenceType)
      if (projectAreaHectares) {
        form.append('project_area_hectares', projectAreaHectares)
      }
      form.append('time_period_years', timePeriodYears)
      
      // Add before/after images for AI analysis
      if (beforeImage) form.append('files', beforeImage)
      if (afterImage) form.append('files', afterImage)

      const resp = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: form
      })

      const data = await resp.json()
      if (!resp.ok) throw new Error(JSON.stringify(data))

      // --- Step 2: hash evidence (demo = hash filenames) ---
      const evidenceHash = keccak256(
        toUtf8Bytes((data.files || []).join(','))
      )
      const evidenceURI = "ipfs://Qmf4TMib7PrH6KNPY9GxshULyKbrjTJNTyWASjsBasQXH7" // TODO: replace with actual IPFS CID

      setStatus('Uploading to blockchain...')

      // --- Step 3: push evidence to blockchain ---
      if (!window.ethereum) throw new Error("MetaMask not available")
      await window.ethereum.request({ method: "eth_requestAccounts" })

      const provider = new ethers.BrowserProvider(window.ethereum) // ethers v6
      const signer = await provider.getSigner()
      const registry = new ethers.Contract(REGISTRY_ADDRESS, BlueCarbonRegistry.abi, signer)

      const tx = await registry.uploadEvidence(
        projectId,
        evidenceHash,
        evidenceURI
      )
      const receipt = await tx.wait()

      // Parse emitted EvidenceUploaded event for evidenceId
      const event = receipt.logs?.map(l => {
        try {
          return registry.interface.parseLog(l)
        } catch {
          return null
        }
      }).find(e => e && e.name === "EvidenceUploaded")

      const evidenceId = event?.args?.evidenceId?.toString()

      setStatus(`Evidence uploaded successfully! ID: ${evidenceId}`)
      setTimeout(() => router.push('/'), 2000)

    } catch (err) {
      console.error(err)
      setStatus('Upload failed: ' + (err.message || err))
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
            Upload Field Evidence
          </h1>
          <p style={{
            color: '#64748b',
            fontSize: '16px',
            margin: 0
          }}>
            Submit evidence for carbon sequestration verification
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
          <form onSubmit={handleSubmit}>
            {/* Project Selection */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Project *
              </label>
              {projects.length ? (
                <select 
                  value={projectId} 
                  onChange={e => setProjectId(e.target.value)}
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
                    cursor: 'pointer'
                  }}
                >
                  <option value="">Select project</option>
                  {projects.map(p => (
                    <option key={p.id} value={p.id}>
                      {p.name} ({p.location})
                    </option>
                  ))}
                </select>
              ) : (
                <div style={{
                  padding: '16px 20px',
                  backgroundColor: '#fef3c7',
                  border: '1px solid #fbbf24',
                  borderRadius: '12px',
                  color: '#92400e',
                  fontSize: '15px'
                }}>
                  No projects found. Please register a project first.
                </div>
              )}
            </div>

            {/* Uploader */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Uploader *
              </label>
              <input
                type="text"
                value={uploader}
                onChange={e => setUploader(e.target.value)}
                placeholder="Name or wallet address"
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

            {/* GPS Coordinates */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                GPS Coordinates *
              </label>
              
              <MapSelector 
                coordinates={gps} 
                onCoordinatesChange={setGps} 
              />
              
              <input
                type="text"
                value={gps}
                onChange={e => setGps(e.target.value)}
                placeholder="lat,lon (e.g. 40.7128,-74.0060) or select from map above"
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
              <p style={{
                fontSize: '13px',
                color: '#64748b',
                margin: '8px 0 0 0'
              }}>
                You can either click on the map above to select coordinates or manually enter them
              </p>
            </div>

            {/* CO2 will be calculated automatically by AI analysis */}

            {/* Before and After Image Uploads */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '15px',
                color: '#374151'
              }}>
                Before & After Images for AI Analysis
              </label>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '20px',
                marginBottom: '15px'
              }}>
                {/* Before Image Upload */}
                <div style={{
                  border: '2px dashed #e5e7eb',
                  borderRadius: '12px',
                  padding: '20px',
                  textAlign: 'center',
                  backgroundColor: beforeImage ? '#f0fdf4' : '#fafafa',
                  borderColor: beforeImage ? '#22c55e' : '#e5e7eb',
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ marginBottom: '10px' }}>
                    <span style={{
                      fontSize: '24px',
                      marginBottom: '8px',
                      display: 'block'
                    }}>📷</span>
                    <div style={{
                      fontSize: '14px',
                      fontWeight: '600',
                      color: '#374151',
                      marginBottom: '5px'
                    }}>
                      Before Image
                    </div>
                    <div style={{
                      fontSize: '12px',
                      color: '#64748b'
                    }}>
                      {beforeImage ? beforeImage.name : 'Land before restoration'}
                    </div>
                  </div>
                  
                  <input
                    type="file"
                    accept="image/*"
                    onChange={e => setBeforeImage(e.target.files[0])}
                    style={{ display: 'none' }}
                    id="before-image-input"
                  />
                  
                  <button
                    type="button"
                    onClick={() => document.getElementById('before-image-input').click()}
                    style={{
                      padding: '8px 16px',
                      background: beforeImage ? 'linear-gradient(135deg, #22c55e, #16a34a)' : 'linear-gradient(135deg, #6366f1, #4f46e5)',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      fontSize: '13px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    {beforeImage ? '✓ Selected' : 'Choose Before'}
                  </button>
                  
                  {beforeImage && (
                    <button
                      type="button"
                      onClick={() => setBeforeImage(null)}
                      style={{
                        padding: '4px 8px',
                        background: 'transparent',
                        color: '#dc2626',
                        border: '1px solid #dc2626',
                        borderRadius: '6px',
                        fontSize: '11px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        marginLeft: '8px'
                      }}
                    >
                      Remove
                    </button>
                  )}
                </div>

                {/* After Image Upload */}
                <div style={{
                  border: '2px dashed #e5e7eb',
                  borderRadius: '12px',
                  padding: '20px',
                  textAlign: 'center',
                  backgroundColor: afterImage ? '#f0fdf4' : '#fafafa',
                  borderColor: afterImage ? '#22c55e' : '#e5e7eb',
                  transition: 'all 0.2s ease'
                }}>
                  <div style={{ marginBottom: '10px' }}>
                    <span style={{
                      fontSize: '24px',
                      marginBottom: '8px',
                      display: 'block'
                    }}>🌱</span>
                    <div style={{
                      fontSize: '14px',
                      fontWeight: '600',
                      color: '#374151',
                      marginBottom: '5px'
                    }}>
                      After Image
                    </div>
                    <div style={{
                      fontSize: '12px',
                      color: '#64748b'
                    }}>
                      {afterImage ? afterImage.name : 'Land after restoration'}
                    </div>
                  </div>
                  
                  <input
                    type="file"
                    accept="image/*"
                    onChange={e => setAfterImage(e.target.files[0])}
                    style={{ display: 'none' }}
                    id="after-image-input"
                  />
                  
                  <button
                    type="button"
                    onClick={() => document.getElementById('after-image-input').click()}
                    style={{
                      padding: '8px 16px',
                      background: afterImage ? 'linear-gradient(135deg, #22c55e, #16a34a)' : 'linear-gradient(135deg, #6366f1, #4f46e5)',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      fontSize: '13px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    {afterImage ? '✓ Selected' : 'Choose After'}
                  </button>
                  
                  {afterImage && (
                    <button
                      type="button"
                      onClick={() => setAfterImage(null)}
                      style={{
                        padding: '4px 8px',
                        background: 'transparent',
                        color: '#dc2626',
                        border: '1px solid #dc2626',
                        borderRadius: '6px',
                        fontSize: '11px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        marginLeft: '8px'
                      }}
                    >
                      Remove
                    </button>
                  )}
                </div>
              </div>

              <div style={{
                padding: '12px',
                backgroundColor: beforeImage && afterImage ? '#f0fdf4' : '#fef3c7',
                border: `1px solid ${beforeImage && afterImage ? '#22c55e' : '#f59e0b'}`,
                borderRadius: '8px',
                fontSize: '13px',
                color: beforeImage && afterImage ? '#15803d' : '#92400e'
              }}>
                {beforeImage && afterImage ? (
                  <span>✅ Both images uploaded! AI will analyze vegetation change for accurate credit estimation.</span>
                ) : (
                  <span>💡 Upload both before and after images to enable AI-powered greenery comparison and accurate carbon credit calculation.</span>
                )}
              </div>
            </div>

            {/* Project Area */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Project Area (hectares) *
              </label>
              <input
                type="number"
                value={projectAreaHectares}
                onChange={e => setProjectAreaHectares(e.target.value)}
                placeholder="e.g. 5.0"
                min="0"
                step="0.1"
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
              <p style={{
                fontSize: '13px',
                color: '#64748b',
                margin: '8px 0 0 0'
              }}>
                Area of your carbon sequestration project in hectares
              </p>
            </div>

            {/* Ecosystem Type */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Ecosystem Type
              </label>
              <select
                value={ecosystemType}
                onChange={e => setEcosystemType(e.target.value)}
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa',
                  cursor: 'pointer'
                }}
              >
                <option value="mangrove">Mangrove</option>
                <option value="seagrass">Seagrass</option>
                <option value="saltmarsh">Saltmarsh</option>
                <option value="mixed">Mixed Blue Carbon</option>
              </select>
            </div>

            {/* Time Period */}
            <div style={{ marginBottom: '25px' }}>
              <label style={{
                display: 'block',
                fontSize: '15px',
                fontWeight: '600',
                marginBottom: '8px',
                color: '#374151'
              }}>
                Time Period (years)
              </label>
              <input
                type="number"
                value={timePeriodYears}
                onChange={e => setTimePeriodYears(e.target.value)}
                placeholder="1.0"
                min="0.1"
                step="0.1"
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

            {/* Carbon Credit Estimation */}
            {(estimation || estimationLoading) && (
              <div style={{
                marginBottom: '30px',
                padding: '25px',
                backgroundColor: '#f8fafc',
                border: '2px solid #e2e8f0',
                borderRadius: '16px'
              }}>
                <h3 style={{
                  fontSize: '18px',
                  fontWeight: '700',
                  color: '#1e293b',
                  marginBottom: '15px',
                  display: 'flex',
                  alignItems: 'center'
                }}>
                  {beforeImage && afterImage ? '�' : '�🎯'} Carbon Credit Estimation
                  {beforeImage && afterImage && (
                    <span style={{
                      marginLeft: '10px',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: '#059669',
                      backgroundColor: '#f0fdf4',
                      padding: '4px 8px',
                      borderRadius: '6px',
                      border: '1px solid #bbf7d0'
                    }}>
                      AI Greenery Analysis
                    </span>
                  )}
                </h3>
                
                {estimationLoading && (
                  <div style={{
                    textAlign: 'center',
                    color: '#64748b',
                    fontSize: '15px'
                  }}>
                    {beforeImage && afterImage ? '🌿 Analyzing vegetation change between images...' : '🔄 Calculating estimation...'}
                  </div>
                )}

                {estimation && !estimationLoading && (
                  <div>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                      gap: '15px',
                      marginBottom: '20px'
                    }}>
                      <div style={{
                        textAlign: 'center',
                        padding: '15px',
                        backgroundColor: 'white',
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0'
                      }}>
                        <div style={{
                          fontSize: '28px',
                          fontWeight: '700',
                          color: '#059669',
                          marginBottom: '5px'
                        }}>
                          {estimation.estimated_credits}
                        </div>
                        <div style={{
                          fontSize: '14px',
                          color: '#64748b',
                          fontWeight: '600'
                        }}>
                          Estimated Credits
                        </div>
                      </div>

                      <div style={{
                        textAlign: 'center',
                        padding: '15px',
                        backgroundColor: 'white',
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0'
                      }}>
                        <div style={{
                          fontSize: '20px',
                          fontWeight: '700',
                          color: '#0284c7',
                          marginBottom: '5px'
                        }}>
                          {estimation.co2_sequestration_kg} kg
                        </div>
                        <div style={{
                          fontSize: '14px',
                          color: '#64748b',
                          fontWeight: '600'
                        }}>
                          CO₂ Sequestration
                        </div>
                      </div>

                      <div style={{
                        textAlign: 'center',
                        padding: '15px',
                        backgroundColor: 'white',
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0'
                      }}>
                        <div style={{
                          fontSize: '16px',
                          fontWeight: '700',
                          color: estimation.confidence_level?.includes('High') ? '#059669' : 
                                estimation.confidence_level?.includes('Medium') ? '#d97706' : '#dc2626',
                          marginBottom: '5px'
                        }}>
                          {estimation.confidence_level || 'Medium Confidence'}
                        </div>
                        <div style={{
                          fontSize: '14px',
                          color: '#64748b',
                          fontWeight: '600'
                        }}>
                          Confidence
                        </div>
                      </div>

                      {/* Green Progress Multiplier Card */}
                      {estimation.green_progress_multiplier && (
                        <div style={{
                          textAlign: 'center',
                          padding: '15px',
                          backgroundColor: 'white',
                          borderRadius: '12px',
                          border: '1px solid #e2e8f0'
                        }}>
                          <div style={{
                            fontSize: '20px',
                            fontWeight: '700',
                            color: estimation.green_progress_multiplier >= 1.3 ? '#059669' :
                                  estimation.green_progress_multiplier >= 1.0 ? '#d97706' : '#dc2626',
                            marginBottom: '5px'
                          }}>
                            {estimation.green_progress_multiplier.toFixed(2)}x
                          </div>
                          <div style={{
                            fontSize: '14px',
                            color: '#64748b',
                            fontWeight: '600'
                          }}>
                            Green Progress
                          </div>
                        </div>
                      )}
                    </div>

                    <div style={{
                      fontSize: '13px',
                      color: '#64748b',
                      textAlign: 'center',
                      fontStyle: 'italic'
                    }}>
                      Method: {estimation.calculation_method} • Type: {estimation.estimation_type}
                      {estimation.greenness_analysis && (
                        <>
                          <span> • Green Progress: {estimation.green_progress_level}</span>
                          <span> • Vegetation Change: {estimation.greenness_analysis.green_improvement}%</span>
                        </>
                      )}
                    </div>

                    {/* Detailed Greenness Analysis Information */}
                    {estimation.greenness_analysis && estimation.greenness_analysis.multiplier_justification && (
                      <div style={{
                        marginTop: '15px',
                        padding: '12px',
                        backgroundColor: '#f0f9ff',
                        border: '1px solid #0ea5e9',
                        borderRadius: '8px',
                        fontSize: '13px',
                        color: '#0369a1'
                      }}>
                        🌱 <strong>Green Progress Analysis:</strong> {estimation.greenness_analysis.multiplier_justification}
                      </div>
                    )}

                    {/* Breakdown Information */}
                    {estimation.breakdown && Object.keys(estimation.breakdown).length > 0 && (
                      <div style={{
                        marginTop: '15px',
                        padding: '12px',
                        backgroundColor: '#f8fafc',
                        border: '1px solid #cbd5e1',
                        borderRadius: '8px',
                        fontSize: '13px',
                        color: '#475569'
                      }}>
                        <div style={{ fontWeight: '600', marginBottom: '8px' }}>📊 Calculation Breakdown:</div>
                        {Object.entries(estimation.breakdown).map(([key, value]) => (
                          <div key={key} style={{ marginBottom: '4px' }}>
                            <strong>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> {value}
                          </div>
                        ))}
                      </div>
                    )}

                    {estimation.disclaimer && (
                      <div style={{
                        marginTop: '15px',
                        padding: '12px',
                        backgroundColor: '#fef3c7',
                        border: '1px solid #f59e0b',
                        borderRadius: '8px',
                        fontSize: '13px',
                        color: '#92400e'
                      }}>
                        ⚠️ {estimation.disclaimer}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* File Upload */}
            {/* Evidence images handled by before/after upload section above */}

            {/* Status Message */}
            {status && (
              <div style={{
                padding: '15px',
                borderRadius: '12px',
                marginBottom: '25px',
                fontSize: '15px',
                fontWeight: '500',
                backgroundColor: status.includes('Error') || status.includes('failed') ? '#fef2f2' : '#f0fdf4',
                color: status.includes('Error') || status.includes('failed') ? '#dc2626' : '#16a34a',
                border: `1px solid ${status.includes('Error') || status.includes('failed') ? '#fecaca' : '#bbf7d0'}`
              }}>
                {status}
              </div>
            )}

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
              <button
                type="submit"
                style={{
                  flex: 1,
                  background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                  color: 'white',
                  border: 'none',
                  padding: '16px 24px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 4px 15px rgba(79, 70, 229, 0.3)'
                }}
              >
                Upload & Anchor
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
