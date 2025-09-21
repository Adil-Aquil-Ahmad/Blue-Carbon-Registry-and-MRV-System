'use client';

import { useRouter } from 'next/navigation';

export default function SiteMapPage() {
  const router = useRouter();

  return (
    <div style={{
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff'
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
                Marine Ecosystem Conservation & Blue Carbon Registry
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content Area */}
      <main id="main-content" style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', minHeight: '600px' }}>
        <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '40px' }}>
          
          {/* Page Title */}
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <h1 style={{
              fontSize: '36px',
              fontWeight: 'bold',
              color: '#1e3a8a',
              margin: '0 0 16px 0'
            }}>
              Site Map
            </h1>
            <p style={{
              fontSize: '18px',
              color: '#666',
              margin: 0
            }}>
              Navigation guide to all pages and services on the Blue Carbon Services Portal
            </p>
          </div>

          {/* Site Map Content */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
            
            {/* Main Pages Section */}
            <div style={{ padding: '24px', backgroundColor: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                🏠 Main Pages
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/landing')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Home Page
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Portal landing page and overview</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/about')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    About Us
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Portal information and mission</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/help')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Help & Support
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- FAQ and support resources</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/terms')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Terms & Conditions
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Legal terms and usage policies</span>
                </li>
              </ul>
            </div>

            {/* Services Section */}
            <div style={{ padding: '24px', backgroundColor: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                ⚙️ Services
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/services')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    All Services
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Complete services directory</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Blue Carbon Projects</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Project registration & management</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Environmental Clearances</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Permit applications & approvals</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Marine Conservation</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Conservation programs & initiatives</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Carbon Trading</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Credit verification & trading</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Research & Monitoring</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- MRV systems & protocols</span>
                </li>
              </ul>
            </div>

            {/* Government Resources Section */}
            <div style={{ padding: '24px', backgroundColor: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                🏛️ Government Resources
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/topics')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Topics
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Blue carbon topics & resources</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/my-government')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    My Government
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Government departments & contacts</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/people-groups')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    People Groups
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Citizen categories & services</span>
                </li>
              </ul>
            </div>

            {/* User Services Section */}
            <div style={{ padding: '24px', backgroundColor: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                👤 User Services
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/auth/register')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Register
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Create new user account</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <button
                    onClick={() => router.push('/auth/login')}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#007cba',
                      cursor: 'pointer',
                      fontSize: '16px',
                      textDecoration: 'underline',
                      padding: 0
                    }}
                  >
                    Login
                  </button>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Access user dashboard</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Projects Dashboard</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Manage your blue carbon projects</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Upload Evidence</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Submit project documentation</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Admin Panel</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Administrative functions</span>
                </li>
              </ul>
            </div>

            {/* Contact & Legal Section */}
            <div style={{ padding: '24px', backgroundColor: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                📞 Contact & Legal
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Contact Us</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Get in touch with support</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Website Policy</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Portal usage policies</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Privacy Policy</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Data protection & privacy</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Accessibility</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Portal accessibility features</span>
                </li>
              </ul>
            </div>

            {/* Quick Access Section */}
            <div style={{ padding: '24px', backgroundColor: '#eff6ff', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
              <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1e3a8a', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                ⚡ Quick Access
              </h2>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Search Services</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Find services by keyword</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Ministry Directory</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Browse by government ministry</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Service Categories</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Browse by service type</span>
                </li>
                <li style={{ marginBottom: '8px' }}>
                  <span style={{ color: '#374151', fontSize: '16px' }}>Most Viewed</span>
                  <span style={{ color: '#666', fontSize: '14px', marginLeft: '8px' }}>- Popular services & resources</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Portal Statistics */}
          <div style={{ 
            marginTop: '40px', 
            padding: '24px', 
            backgroundColor: '#1e3a8a', 
            color: 'white',
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <h3 style={{ fontSize: '24px', fontWeight: '600', marginBottom: '16px', margin: '0 0 16px 0' }}>
              Portal Overview
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
              <div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>2,847</div>
                <div style={{ fontSize: '16px', opacity: 0.9 }}>Services Listed</div>
              </div>
              <div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>13</div>
                <div style={{ fontSize: '16px', opacity: 0.9 }}>Government Ministries</div>
              </div>
              <div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>10</div>
                <div style={{ fontSize: '16px', opacity: 0.9 }}>Service Categories</div>
              </div>
              <div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>6</div>
                <div style={{ fontSize: '16px', opacity: 0.9 }}>Main Portal Sections</div>
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
            <span style={{
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              backgroundColor: 'rgba(255,255,255,0.1)',
              padding: '4px 8px',
              borderRadius: '4px'
            }}>
              Site Map
            </span>
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