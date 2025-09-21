'use client';

import { useRouter } from 'next/navigation';

export default function AboutPage() {
  const router = useRouter();

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Header */}
      <header style={{ backgroundColor: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        {/* Main Header */}
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '15px 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
              <div>
                <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold', color: '#1e3a8a' }}>
                  Blue Carbon Services Portal
                </h1>
                <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>Find Marine Conservation Services Faster</p>
              </div>
              <img 
                src="/logo_1.png" 
                alt="India Portal Logo" 
                style={{ height: '48px', objectFit: 'contain' }}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Banner Section */}
      <section style={{ 
        background: 'linear-gradient(to right, #2563eb, #1e40af)', 
        color: 'white',
        padding: '60px 0',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
          opacity: 0.3
        }}></div>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', position: 'relative' }}>
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ fontSize: '48px', fontWeight: 'bold', margin: 0, marginBottom: '16px' }}>
              About the Portal
            </h2>
            <p style={{ fontSize: '18px', margin: 0, opacity: 0.9 }}>
              Empowering Marine Conservation Through Digital Innovation
            </p>
          </div>
        </div>
      </section>

      {/* Breadcrumb */}
      <div style={{ backgroundColor: 'white', padding: '12px 0', borderBottom: '1px solid #e5e7eb' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <ul style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: 0, padding: 0, listStyle: 'none', fontSize: '14px' }}>
            <li>
              <button
                onClick={() => router.push('/')}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#2563eb',
                  cursor: 'pointer',
                  textDecoration: 'underline'
                }}
              >
                Home
              </button>
            </li>
            <li style={{ color: '#6b7280' }}>›</li>
            <li style={{ color: '#374151' }}>About the Portal</li>
          </ul>
        </div>
      </div>

      {/* Main Content */}
      <main id="skipCont" style={{ maxWidth: '1200px', margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '40px' }}>
          <div style={{ marginBottom: '32px' }}>
            <h2 style={{ 
              fontSize: '28px', 
              fontWeight: 'bold', 
              color: '#1e3a8a', 
              marginBottom: '24px',
              borderBottom: '3px solid #2563eb',
              paddingBottom: '8px'
            }}>
              About the Portal
            </h2>
          </div>

          <div style={{ fontSize: '16px', lineHeight: '1.7', color: '#374151' }}>
            <p style={{ marginBottom: '24px' }}>
              Many government entities at the Central, State, District and Local levels are providing online services for marine conservation and blue carbon initiatives that have made the life of coastal communities simpler and have also increased transparency and efficiency in environmental protection. These services are provided through multiple websites and platforms.
            </p>

            <p style={{ marginBottom: '24px' }}>
              In order to list these blue carbon and marine conservation services in a well categorised and searchable interface, the Blue Carbon Services Portal (
              <a href="/" style={{ color: '#2563eb', textDecoration: 'underline' }}>bluecarbon.gov.in</a>
              ) has been developed under the ambit of the{' '}
              <a href="https://www.india.gov.in/" target="_blank" rel="noopener" style={{ color: '#2563eb', textDecoration: 'underline' }}>
                India Portal
              </a>{' '}
              project which is being executed by{' '}
              <a href="https://www.nic.in/" target="_blank" rel="noopener" style={{ color: '#2563eb', textDecoration: 'underline' }}>
                NIC
              </a>{' '}
              in collaboration with the Ministry of Environment, Forest and Climate Change.
            </p>

            <p style={{ marginBottom: '32px' }}>
              The purpose of this portal is to facilitate the listing of online services related to blue carbon ecosystems, marine conservation, and coastal management provided by various government entities under one platform and ensuring standardization with respect to content architecture and classification of services.
            </p>

            {/* Mission Section */}
            <div style={{ 
              backgroundColor: '#eff6ff', 
              padding: '24px', 
              borderRadius: '8px', 
              marginBottom: '32px',
              borderLeft: '4px solid #2563eb'
            }}>
              <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px' }}>
                Our Mission
              </h3>
              <p style={{ margin: 0, color: '#374151' }}>
                To create a unified digital platform that promotes sustainable marine ecosystem management, 
                facilitates blue carbon project development, and enables efficient access to government services 
                for coastal communities, researchers, and environmental organizations across India.
              </p>
            </div>

            {/* Key Features */}
            <div style={{ marginBottom: '32px' }}>
              <h3 style={{ fontSize: '22px', fontWeight: '600', color: '#1e3a8a', marginBottom: '20px' }}>
                Key Features
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    🌊 Blue Carbon Registry
                  </h4>
                  <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>
                    Comprehensive registration and verification system for blue carbon projects including mangroves, seagrass beds, and salt marshes.
                  </p>
                </div>
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    📊 MRV System
                  </h4>
                  <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>
                    Measuring, Reporting, and Verification platform for carbon monitoring and compliance tracking.
                  </p>
                </div>
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    🏛️ Government Services
                  </h4>
                  <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>
                    Single-window access to environmental clearances, permits, and regulatory compliance services.
                  </p>
                </div>
                <div style={{ padding: '20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                  <h4 style={{ color: '#2563eb', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    🎓 Education Hub
                  </h4>
                  <p style={{ margin: 0, fontSize: '14px', color: '#64748b' }}>
                    Training programs, certification courses, and educational resources for capacity building.
                  </p>
                </div>
              </div>
            </div>

            {/* Statistics */}
            <div style={{ 
              backgroundColor: '#1e3a8a', 
              color: 'white', 
              padding: '32px', 
              borderRadius: '8px', 
              marginBottom: '32px',
              textAlign: 'center'
            }}>
              <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '24px', margin: 0 }}>
                Portal Impact
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
                <div>
                  <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>2,847</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Services Listed</div>
                </div>
                <div>
                  <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>13</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Coastal States Covered</div>
                </div>
                <div>
                  <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>450+</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Registered Projects</div>
                </div>
                <div>
                  <div style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '8px' }}>75,000+</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Community Members</div>
                </div>
              </div>
            </div>

            {/* Partnership */}
            <div style={{ marginBottom: '32px' }}>
              <h3 style={{ fontSize: '22px', fontWeight: '600', color: '#1e3a8a', marginBottom: '20px' }}>
                Partnership & Collaboration
              </h3>
              <p style={{ marginBottom: '16px' }}>
                This portal is developed in partnership with leading research institutions, 
                coastal state governments, and international organizations working on blue carbon initiatives. 
                Our collaborative approach ensures comprehensive coverage of marine conservation services 
                and adherence to international standards for blue carbon accounting.
              </p>
              <p style={{ margin: 0 }}>
                We work closely with the Ministry of Earth Sciences, Ministry of Fisheries, Animal Husbandry & Dairying, 
                and various coastal state pollution control boards to provide seamless access to environmental services.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer Slider */}
      <section style={{ backgroundColor: '#f1f5f9', padding: '20px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '40px', flexWrap: 'wrap' }}>
            <a href="https://www.india.gov.in/" target="_blank" rel="noopener">
              <img src="/logo_1.png" alt="India Gov" style={{ height: '40px', objectFit: 'contain', opacity: 0.7 }} />
            </a>
            <a href="https://www.mygov.in/" target="_blank" rel="noopener">
              <div style={{ 
                backgroundColor: '#2563eb', 
                color: 'white', 
                padding: '8px 16px', 
                borderRadius: '4px', 
                fontSize: '14px', 
                fontWeight: '600' 
              }}>
                MyGov
              </div>
            </a>
            <a href="https://data.gov.in/" target="_blank" rel="noopener">
              <div style={{ 
                backgroundColor: '#059669', 
                color: 'white', 
                padding: '8px 16px', 
                borderRadius: '4px', 
                fontSize: '14px', 
                fontWeight: '600' 
              }}>
                Data Gov
              </div>
            </a>
            <a href="http://www.nic.in/" target="_blank" rel="noopener">
              <div style={{ 
                backgroundColor: '#7c3aed', 
                color: 'white', 
                padding: '8px 16px', 
                borderRadius: '4px', 
                fontSize: '14px', 
                fontWeight: '600' 
              }}>
                NIC
              </div>
            </a>
          </div>
        </div>
      </section>

      {/* Services Count Section */}
      <section style={{ backgroundColor: '#2563eb', color: 'white', padding: '32px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
            <div style={{ textAlign: 'center' }}>
              <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>2,847</p>
              <p style={{ fontSize: '18px', margin: 0 }}>Blue Carbon Services Listed</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <p style={{ margin: 0 }}>
                <a href="/recommend" style={{ color: 'white', textDecoration: 'none' }}
                   onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
                   onMouseOut={(e) => e.target.style.textDecoration = 'none'}>
                  Know a marine conservation service? <span style={{ fontWeight: '600' }}>Let us know.</span>
                </a>
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
            >
              Contact Us
            </button>
          </div>
          
          <div style={{ borderTop: '1px solid #4b5563', paddingTop: '16px', fontSize: '14px', color: '#9ca3af' }}>
            <p style={{ margin: 0, marginBottom: '8px' }}>
              This is the Blue Carbon Services Portal of India, developed to enable single window access to marine conservation and blue carbon services provided by various Government entities.
            </p>
            <p style={{ margin: 0 }}>Last Updated: Sep 21, 2025</p>
          </div>
        </div>
      </footer>
    </div>
  );
}