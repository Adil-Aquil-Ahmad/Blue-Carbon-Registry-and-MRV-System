'use client';

import { useRouter } from 'next/navigation';

export default function MyGovernmentPage() {
  const router = useRouter();

  return (
    <div style={{
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff'
    }}>
      {/* Top Header Bar */}
      <section style={{
        backgroundColor: '#f8f8f8',
        padding: '10px 0',
        borderBottom: '1px solid #ddd',
        fontSize: '14px'
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
            gap: '10px'
          }}>
            <span style={{ color: '#666' }}>भारत सरकार</span>
            <span style={{ color: '#007cba', fontWeight: 'bold' }}>GOVERNMENT OF INDIA</span>
          </div>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '15px'
          }}>
            <button
              onClick={() => router.push('/')}
              style={{
                background: 'none',
                border: 'none',
                color: '#007cba',
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              Home
            </button>
            <span style={{ color: '#666' }}>|</span>
            <button
              onClick={() => router.push('/auth/login')}
              style={{
                background: 'none',
                border: 'none',
                color: '#007cba',
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              Login
            </button>
            <img 
              src="/logo_1.png" 
              alt="Ashok Stambha" 
              style={{
                width: '40px',
                height: '40px',
                objectFit: 'contain',
                marginLeft: '15px'
              }}
            />
          </div>
        </div>
      </section>

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
                margin: 0,
                fontSize: '32px',
                fontWeight: 'bold',
                color: '#007cba',
                lineHeight: '1.2'
              }}>
                My Government
              </h1>
              <p style={{
                margin: 0,
                fontSize: '16px',
                color: '#007cba',
                fontStyle: 'italic'
              }}>
                government departments and services
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '40px 20px'
      }}>
        {/* Government Departments */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Government Departments
          </h2>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
            gap: '20px',
            marginBottom: '30px'
          }}>
            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              backgroundColor: '#ffffff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>🌿 Ministry of Environment, Forest and Climate Change</h3>
              <p style={{ color: '#666', lineHeight: '1.6', marginBottom: '15px' }}>
                Lead ministry for environmental protection, forest conservation, and climate change initiatives.
              </p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button style={{
                  backgroundColor: '#007cba',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Visit Website
                </button>
                <button style={{
                  backgroundColor: 'transparent',
                  color: '#007cba',
                  border: '1px solid #007cba',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Contact
                </button>
              </div>
            </div>

            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              backgroundColor: '#ffffff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>🌊 Ministry of Earth Sciences</h3>
              <p style={{ color: '#666', lineHeight: '1.6', marginBottom: '15px' }}>
                Responsible for ocean research, coastal zone management, and marine ecosystem studies.
              </p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button style={{
                  backgroundColor: '#007cba',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Visit Website
                </button>
                <button style={{
                  backgroundColor: 'transparent',
                  color: '#007cba',
                  border: '1px solid #007cba',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Contact
                </button>
              </div>
            </div>

            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              backgroundColor: '#ffffff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>🐟 Ministry of Fisheries, Animal Husbandry & Dairying</h3>
              <p style={{ color: '666', lineHeight: '1.6', marginBottom: '15px' }}>
                Oversight of coastal fisheries and marine aquaculture development programs.
              </p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button style={{
                  backgroundColor: '#007cba',
                  color: 'white',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Visit Website
                </button>
                <button style={{
                  backgroundColor: 'transparent',
                  color: '#007cba',
                  border: '1px solid #007cba',
                  padding: '8px 16px',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}>
                  Contact
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Key Initiatives */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Key Government Initiatives
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '20px'
          }}>
            {[
              {
                title: '🌱 National Action Plan on Climate Change',
                description: 'Comprehensive strategy for climate mitigation and adaptation',
                status: 'Active'
              },
              {
                title: '🏖️ Coastal Regulation Zone Guidelines',
                description: 'Framework for sustainable coastal development',
                status: 'Updated 2024'
              },
              {
                title: '💚 Green India Mission',
                description: 'Increasing forest and tree cover across the country',
                status: 'Ongoing'
              },
              {
                title: '🌊 Blue Economy Policy',
                description: 'Sustainable development of marine resources',
                status: 'New'
              },
              {
                title: '🔄 Carbon Neutral India 2070',
                description: 'National commitment to net-zero emissions',
                status: 'Target Set'
              },
              {
                title: '🐾 Biodiversity Conservation',
                description: 'Protection of coastal and marine biodiversity',
                status: 'Priority'
              }
            ].map((initiative, index) => (
              <div key={index} style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '20px',
                backgroundColor: '#f8f9fa',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = '#e9ecef';
                e.currentTarget.style.borderColor = '#007cba';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = '#f8f9fa';
                e.currentTarget.style.borderColor = '#ddd';
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '10px'
                }}>
                  <h4 style={{ color: '#333', margin: 0, fontSize: '16px' }}>{initiative.title}</h4>
                  <span style={{
                    backgroundColor: '#007cba',
                    color: 'white',
                    padding: '2px 8px',
                    borderRadius: '12px',
                    fontSize: '12px'
                  }}>
                    {initiative.status}
                  </span>
                </div>
                <p style={{ color: '#666', margin: 0, fontSize: '14px', lineHeight: '1.5' }}>
                  {initiative.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Quick Links */}
        <section>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Quick Government Links
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '15px'
          }}>
            {[
              { name: '🏛️ India.gov.in', desc: 'National Portal' },
              { name: '📋 MyGov.in', desc: 'Citizen Participation' },
              { name: '💼 Digital India', desc: 'Digital Services' },
              { name: '🌐 PMO India', desc: 'Prime Minister Office' },
              { name: '📊 Data.gov.in', desc: 'Open Government Data' },
              { name: '⚖️ Legislative Dept', desc: 'Law & Justice' },
              { name: '🎯 NITI Aayog', desc: 'Policy Think Tank' },
              { name: '📱 Aadhaar', desc: 'Identity Services' }
            ].map((link, index) => (
              <div key={index} style={{
                border: '1px solid #ddd',
                borderRadius: '6px',
                padding: '15px',
                backgroundColor: '#ffffff',
                textAlign: 'center',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = '#f0f8ff';
                e.currentTarget.style.borderColor = '#007cba';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = '#ffffff';
                e.currentTarget.style.borderColor = '#ddd';
              }}>
                <h4 style={{ color: '#007cba', marginBottom: '5px', fontSize: '14px' }}>{link.name}</h4>
                <p style={{ color: '#666', fontSize: '12px', margin: 0 }}>{link.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer style={{
        backgroundColor: '#333',
        color: 'white',
        padding: '40px 0',
        marginTop: '60px'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px',
          textAlign: 'center'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginBottom: '20px'
          }}>
            <img 
              src="/logo_1.png" 
              alt="Government Logo" 
              style={{
                width: '40px',
                height: '40px',
                objectFit: 'contain',
                marginRight: '15px'
              }}
            />
            <div>
              <h3 style={{ margin: 0, fontSize: '18px' }}>Blue Carbon Registry</h3>
              <p style={{ margin: 0, fontSize: '14px', opacity: 0.8 }}>Ministry of Environment, Forest and Climate Change</p>
            </div>
          </div>
          <p style={{ margin: 0, fontSize: '14px', opacity: 0.8 }}>
            © 2025 Government of India. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}