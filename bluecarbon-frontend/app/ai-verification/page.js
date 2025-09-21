'use client';

import { useRouter } from 'next/navigation';
import { useState, useRef } from 'react';

export default function AIVerificationPage() {
  const router = useRouter();
  const fileInputRef = useRef(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setAnalysisResults(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && (file.type.startsWith('image/') || file.type.startsWith('video/'))) {
      setUploadedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setAnalysisResults(null);
    }
  };

  const analyzeEvidence = async () => {
    if (!uploadedFile) return;
    
    setIsAnalyzing(true);
    
    // Simulate AI analysis (replace with actual API call)
    setTimeout(() => {
      const mockResults = {
        ndviScore: Math.random() * 0.8 + 0.2, // Random NDVI between 0.2-1.0
        vegetationCoverage: Math.random() * 80 + 10, // Random coverage 10-90%
        plantedArea: Math.random() * 70 + 20, // Random planted area 20-90%
        emptyLand: Math.random() * 30 + 5, // Random empty land 5-35%
        healthIndex: Math.random() * 30 + 70, // Health index 70-100%
        confidence: Math.random() * 20 + 80, // Confidence 80-100%
        mangroveDetected: Math.random() > 0.3,
        analysisType: uploadedFile.type.startsWith('video/') ? 'Video Analysis' : 'Image Analysis',
        timestamp: new Date().toISOString(),
        fileName: uploadedFile.name
      };
      
      setAnalysisResults(mockResults);
      setAnalysisHistory(prev => [mockResults, ...prev.slice(0, 4)]);
      setIsAnalyzing(false);
    }, 3000);
  };

  const clearAnalysis = () => {
    setUploadedFile(null);
    setPreviewUrl(null);
    setAnalysisResults(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f8fafc'
    }}>
      {/* Main Header */}
      <section style={{
        backgroundColor: '#ffffff',
        padding: '20px 0',
        borderBottom: '1px solid #ddd'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '20px'
          }}>
            <div>
              <h1 style={{
                fontSize: '28px',
                fontWeight: 'bold',
                color: '#1e3a8a',
                margin: '0',
                cursor: 'pointer'
              }} onClick={() => router.push('/landing')}>
                Blue Carbon Services Portal
              </h1>
              <p style={{
                fontSize: '14px',
                color: '#666',
                margin: '5px 0 0 0'
              }}>
                AI-Powered Evidence Verification System
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '40px 20px' }}>
        
        {/* Page Header */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{
            fontSize: '36px',
            fontWeight: 'bold',
            color: '#1e3a8a',
            margin: '0 0 16px 0'
          }}>
            🤖 AI Evidence Verification
          </h1>
          <p style={{
            fontSize: '18px',
            color: '#666',
            margin: '0 0 8px 0'
          }}>
            Advanced computer vision analysis for mangrove and vegetation verification
          </p>
          <p style={{
            fontSize: '14px',
            color: '#8b5cf6',
            margin: 0
          }}>
            Upload field photos or videos to verify actual plant growth using NDVI analysis
          </p>
        </div>

        {/* Analysis Dashboard */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'start' }}>
          
          {/* Upload and Analysis Section */}
          <div>
            {/* File Upload Area */}
            <div style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              padding: '32px',
              marginBottom: '24px'
            }}>
              <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginBottom: '24px' }}>
                📸 Upload Evidence
              </h2>
              
              {!uploadedFile ? (
                <div
                  style={{
                    border: '2px dashed #d1d5db',
                    borderRadius: '8px',
                    padding: '48px 32px',
                    textAlign: 'center',
                    backgroundColor: '#f9fafb',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  onMouseOver={(e) => {
                    e.currentTarget.style.borderColor = '#2563eb';
                    e.currentTarget.style.backgroundColor = '#eff6ff';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.borderColor = '#d1d5db';
                    e.currentTarget.style.backgroundColor = '#f9fafb';
                  }}
                >
                  <div style={{ fontSize: '48px', marginBottom: '16px' }}>📁</div>
                  <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#374151', marginBottom: '8px' }}>
                    Drop your files here or click to browse
                  </h3>
                  <p style={{ color: '#6b7280', marginBottom: '16px' }}>
                    Supports: JPG, PNG, TIFF, MP4, AVI, MOV
                  </p>
                  <div style={{
                    display: 'inline-block',
                    backgroundColor: '#2563eb',
                    color: 'white',
                    padding: '12px 24px',
                    borderRadius: '6px',
                    fontWeight: '600'
                  }}>
                    Choose Files
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*,video/*"
                    onChange={handleFileUpload}
                    style={{ display: 'none' }}
                  />
                </div>
              ) : (
                <div>
                  {/* File Preview */}
                  <div style={{
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    padding: '16px',
                    marginBottom: '24px',
                    backgroundColor: '#f9fafb'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                      <div style={{ fontSize: '24px' }}>
                        {uploadedFile.type.startsWith('video/') ? '🎥' : '🖼️'}
                      </div>
                      <div>
                        <h4 style={{ margin: '0 0 4px 0', fontSize: '16px', fontWeight: '600', color: '#374151' }}>
                          {uploadedFile.name}
                        </h4>
                        <p style={{ margin: 0, fontSize: '14px', color: '#6b7280' }}>
                          {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB • {uploadedFile.type}
                        </p>
                      </div>
                    </div>
                    
                    {previewUrl && uploadedFile.type.startsWith('image/') && (
                      <img
                        src={previewUrl}
                        alt="Preview"
                        style={{
                          width: '100%',
                          maxHeight: '200px',
                          objectFit: 'cover',
                          borderRadius: '6px'
                        }}
                      />
                    )}
                    
                    {previewUrl && uploadedFile.type.startsWith('video/') && (
                      <video
                        src={previewUrl}
                        controls
                        style={{
                          width: '100%',
                          maxHeight: '200px',
                          borderRadius: '6px'
                        }}
                      />
                    )}
                  </div>

                  {/* Analysis Controls */}
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button
                      onClick={analyzeEvidence}
                      disabled={isAnalyzing}
                      style={{
                        flex: 1,
                        padding: '14px 20px',
                        backgroundColor: isAnalyzing ? '#9ca3af' : '#16a34a',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: isAnalyzing ? 'not-allowed' : 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '8px'
                      }}
                    >
                      {isAnalyzing ? '🔄' : '🤖'} 
                      {isAnalyzing ? 'Analyzing...' : 'Start AI Analysis'}
                    </button>
                    <button
                      onClick={clearAnalysis}
                      style={{
                        padding: '14px 20px',
                        backgroundColor: '#ef4444',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer'
                      }}
                    >
                      Clear
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Analysis Progress */}
            {isAnalyzing && (
              <div style={{
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                padding: '24px'
              }}>
                <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px' }}>
                  🔍 AI Analysis in Progress
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ fontSize: '20px' }}>⚡</div>
                    <span>Processing image data...</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ fontSize: '20px' }}>🌱</div>
                    <span>Calculating NDVI values...</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ fontSize: '20px' }}>🧠</div>
                    <span>Detecting vegetation patterns...</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ fontSize: '20px' }}>📊</div>
                    <span>Generating analysis report...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div>
            {analysisResults && (
              <div style={{
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                padding: '32px'
              }}>
                <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginBottom: '24px' }}>
                  📊 Analysis Results
                </h2>
                
                {/* Key Metrics */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '32px' }}>
                  <div style={{
                    backgroundColor: '#f0f9ff',
                    border: '1px solid #0ea5e9',
                    borderRadius: '8px',
                    padding: '16px',
                    textAlign: 'center'
                  }}>
                    <h3 style={{ fontSize: '32px', fontWeight: 'bold', color: '#0284c7', margin: '0 0 4px 0' }}>
                      {analysisResults.ndviScore.toFixed(3)}
                    </h3>
                    <p style={{ margin: 0, fontSize: '14px', color: '#0284c7', fontWeight: '600' }}>NDVI Score</p>
                  </div>
                  
                  <div style={{
                    backgroundColor: '#f0fdf4',
                    border: '1px solid #22c55e',
                    borderRadius: '8px',
                    padding: '16px',
                    textAlign: 'center'
                  }}>
                    <h3 style={{ fontSize: '32px', fontWeight: 'bold', color: '#16a34a', margin: '0 0 4px 0' }}>
                      {analysisResults.confidence.toFixed(1)}%
                    </h3>
                    <p style={{ margin: 0, fontSize: '14px', color: '#16a34a', fontWeight: '600' }}>Confidence</p>
                  </div>
                </div>

                {/* Detailed Analysis */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', color: '#374151' }}>Vegetation Coverage</span>
                      <span style={{ fontWeight: '600', color: '#16a34a' }}>{analysisResults.vegetationCoverage.toFixed(1)}%</span>
                    </div>
                    <div style={{ 
                      width: '100%', 
                      height: '8px', 
                      backgroundColor: '#e5e7eb', 
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${analysisResults.vegetationCoverage}%`,
                        height: '100%',
                        backgroundColor: '#16a34a',
                        borderRadius: '4px'
                      }} />
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', color: '#374151' }}>Planted Area</span>
                      <span style={{ fontWeight: '600', color: '#2563eb' }}>{analysisResults.plantedArea.toFixed(1)}%</span>
                    </div>
                    <div style={{ 
                      width: '100%', 
                      height: '8px', 
                      backgroundColor: '#e5e7eb', 
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${analysisResults.plantedArea}%`,
                        height: '100%',
                        backgroundColor: '#2563eb',
                        borderRadius: '4px'
                      }} />
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', color: '#374151' }}>Empty Land</span>
                      <span style={{ fontWeight: '600', color: '#dc2626' }}>{analysisResults.emptyLand.toFixed(1)}%</span>
                    </div>
                    <div style={{ 
                      width: '100%', 
                      height: '8px', 
                      backgroundColor: '#e5e7eb', 
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${analysisResults.emptyLand}%`,
                        height: '100%',
                        backgroundColor: '#dc2626',
                        borderRadius: '4px'
                      }} />
                    </div>
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', color: '#374151' }}>Health Index</span>
                      <span style={{ fontWeight: '600', color: '#059669' }}>{analysisResults.healthIndex.toFixed(1)}%</span>
                    </div>
                    <div style={{ 
                      width: '100%', 
                      height: '8px', 
                      backgroundColor: '#e5e7eb', 
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${analysisResults.healthIndex}%`,
                        height: '100%',
                        backgroundColor: '#059669',
                        borderRadius: '4px'
                      }} />
                    </div>
                  </div>
                </div>

                {/* Detection Status */}
                <div style={{
                  marginTop: '24px',
                  padding: '16px',
                  backgroundColor: analysisResults.mangroveDetected ? '#dcfce7' : '#fef3c7',
                  border: `1px solid ${analysisResults.mangroveDetected ? '#16a34a' : '#f59e0b'}`,
                  borderRadius: '8px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '20px' }}>
                      {analysisResults.mangroveDetected ? '✅' : '⚠️'}
                    </span>
                    <span style={{ 
                      fontWeight: '600', 
                      color: analysisResults.mangroveDetected ? '#166534' : '#92400e' 
                    }}>
                      {analysisResults.mangroveDetected ? 'Mangrove Vegetation Detected' : 'Limited Vegetation Detected'}
                    </span>
                  </div>
                  <p style={{ 
                    margin: '8px 0 0 0', 
                    fontSize: '14px', 
                    color: analysisResults.mangroveDetected ? '#166534' : '#92400e' 
                  }}>
                    {analysisResults.mangroveDetected 
                      ? 'AI has identified healthy mangrove vegetation patterns consistent with successful planting efforts.'
                      : 'AI analysis suggests limited or sparse vegetation. Consider verifying planting status or environmental conditions.'
                    }
                  </p>
                </div>

                {/* Export Results */}
                <div style={{ marginTop: '24px', textAlign: 'center' }}>
                  <button
                    onClick={() => console.log('Export results:', analysisResults)}
                    style={{
                      padding: '12px 24px',
                      backgroundColor: '#8b5cf6',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      fontSize: '14px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}
                  >
                    📄 Export Analysis Report
                  </button>
                </div>
              </div>
            )}

            {/* Analysis History */}
            {analysisHistory.length > 0 && (
              <div style={{
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                padding: '24px',
                marginTop: '24px'
              }}>
                <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px' }}>
                  📈 Recent Analysis History
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {analysisHistory.slice(0, 3).map((result, index) => (
                    <div key={index} style={{
                      padding: '12px',
                      border: '1px solid #e5e7eb',
                      borderRadius: '6px',
                      fontSize: '14px'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: '600', color: '#374151' }}>{result.fileName}</span>
                        <span style={{ color: '#6b7280' }}>
                          {new Date(result.timestamp).toLocaleString()}
                        </span>
                      </div>
                      <div style={{ marginTop: '4px', color: '#6b7280' }}>
                        NDVI: {result.ndviScore.toFixed(3)} • Vegetation: {result.vegetationCoverage.toFixed(1)}% • Confidence: {result.confidence.toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Technical Information */}
        <div style={{ marginTop: '60px' }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
            padding: '40px'
          }}>
            <h2 style={{ fontSize: '28px', fontWeight: '600', color: '#1e3a8a', marginBottom: '24px', textAlign: 'center' }}>
              🧠 How Our AI Analysis Works
            </h2>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>🌿</div>
                <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#374151', marginBottom: '12px' }}>
                  NDVI Calculation
                </h3>
                <p style={{ margin: 0, color: '#6b7280', lineHeight: '1.6' }}>
                  Normalized Difference Vegetation Index analysis using near-infrared and red light reflectance to accurately measure vegetation health and density.
                </p>
              </div>

              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>🎯</div>
                <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#374151', marginBottom: '12px' }}>
                  Computer Vision
                </h3>
                <p style={{ margin: 0, color: '#6b7280', lineHeight: '1.6' }}>
                  Advanced image processing algorithms detect planted areas, analyze growth patterns, and differentiate between healthy vegetation and bare land.
                </p>
              </div>

              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📊</div>
                <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#374151', marginBottom: '12px' }}>
                  Machine Learning
                </h3>
                <p style={{ margin: 0, color: '#6b7280', lineHeight: '1.6' }}>
                  Trained models specifically for mangrove and coastal vegetation recognition, providing high-confidence verification results for blue carbon projects.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Services Count Section */}
      <section style={{ backgroundColor: '#2563eb', color: 'white', padding: '32px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
            <div style={{ textAlign: 'center' }}>
              <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>AI-Powered</p>
              <p style={{ fontSize: '18px', margin: 0 }}>Evidence Verification System</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <p style={{ margin: 0 }}>
                <span style={{ color: 'white' }}>
                  Advanced computer vision for <span style={{ fontWeight: '600' }}>blue carbon verification</span>
                </span>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ backgroundColor: '#374151', color: 'white' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '32px 20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px', marginBottom: '32px' }}>
            <button
              onClick={() => router.push('/about')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              About Us
            </button>
            <button
              onClick={() => router.push('/help')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              Help
            </button>
            <button
              onClick={() => router.push('/terms')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              Terms and Conditions
            </button>
            <button
              onClick={() => router.push('/sitemap')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              Site Map
            </button>
            <button
              onClick={() => router.push('/policy')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              Website Policy
            </button>
            <button
              onClick={() => router.push('/contact')}
              style={{
                background: 'none',
                border: 'none',
                color: '#93c5fd',
                cursor: 'pointer',
                textAlign: 'left',
                fontSize: '14px'
              }}
              onMouseOver={(e) => e.target.style.color = '#dbeafe'}
              onMouseOut={(e) => e.target.style.color = '#93c5fd'}
            >
              Contact Us
            </button>
          </div>
          
          <div style={{ borderTop: '1px solid #4b5563', paddingTop: '16px', fontSize: '14px', color: '#9ca3af' }}>
            <p style={{ margin: 0 }}>
              This is the Blue Carbon Services Portal of India, developed to enable single window access to marine conservation and blue carbon services provided by various Government entities.
            </p>
            <p style={{ margin: '8px 0 0 0' }}>
              Last Updated: Sep 21, 2025
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}