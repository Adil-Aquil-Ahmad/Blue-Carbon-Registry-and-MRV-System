'use client';

import { useRouter } from 'next/navigation';

export default function TopicsPage() {
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
                Topics
              </h1>
              <p style={{
                margin: 0,
                fontSize: '16px',
                color: '#007cba',
                fontStyle: 'italic'
              }}>
                explore blue carbon topics and resources
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
        {/* Featured Topics */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Featured Topics
          </h2>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
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
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>🌊 Blue Carbon Ecosystems</h3>
              <p style={{ color: '#666', lineHeight: '1.6' }}>
                Learn about mangroves, seagrass beds, and salt marshes that capture and store carbon dioxide.
              </p>
              <button style={{
                backgroundColor: '#007cba',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                marginTop: '10px'
              }}>
                Explore
              </button>
            </div>

            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              backgroundColor: '#ffffff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>📊 Carbon Registry</h3>
              <p style={{ color: '#666', lineHeight: '1.6' }}>
                Understanding the process of measuring, reporting, and verifying blue carbon projects.
              </p>
              <button style={{
                backgroundColor: '#007cba',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                marginTop: '10px'
              }}>
                Learn More
              </button>
            </div>

            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              padding: '20px',
              backgroundColor: '#ffffff',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ color: '#007cba', marginBottom: '10px' }}>🌱 Conservation Methods</h3>
              <p style={{ color: '#666', lineHeight: '1.6' }}>
                Best practices for protecting and restoring coastal ecosystems.
              </p>
              <button style={{
                backgroundColor: '#007cba',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                marginTop: '10px'
              }}>
                Read Guide
              </button>
            </div>
          </div>
        </section>

        {/* Topic Categories */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Browse by Category
          </h2>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '15px'
          }}>
            {[
              { title: '🔬 Research & Science', count: '15 articles' },
              { title: '📈 Policy & Governance', count: '12 articles' },
              { title: '💰 Financing & Markets', count: '8 articles' },
              { title: '🛠️ Technology & Tools', count: '10 articles' },
              { title: '🌍 Global Initiatives', count: '6 articles' },
              { title: '📚 Educational Resources', count: '20 articles' }
            ].map((category, index) => (
              <div key={index} style={{
                border: '1px solid #ddd',
                borderRadius: '6px',
                padding: '15px',
                backgroundColor: '#f8f9fa',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.target.style.backgroundColor = '#e9ecef';
                e.target.style.borderColor = '#007cba';
              }}
              onMouseOut={(e) => {
                e.target.style.backgroundColor = '#f8f9fa';
                e.target.style.borderColor = '#ddd';
              }}>
                <h4 style={{ color: '#333', marginBottom: '5px' }}>{category.title}</h4>
                <p style={{ color: '#666', fontSize: '14px', margin: 0 }}>{category.count}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Recent Updates */}
        <section>
          <h2 style={{
            fontSize: '28px',
            fontWeight: 'bold',
            color: '#333',
            marginBottom: '20px',
            borderBottom: '3px solid #007cba',
            paddingBottom: '10px'
          }}>
            Recent Updates
          </h2>

          <div style={{
            border: '1px solid #ddd',
            borderRadius: '8px',
            backgroundColor: '#ffffff'
          }}>
            {[
              {
                date: 'Sep 20, 2025',
                title: 'New Guidelines for Mangrove Carbon Assessment',
                description: 'Updated methodologies for measuring carbon storage in mangrove ecosystems.'
              },
              {
                date: 'Sep 18, 2025',
                title: 'Blue Carbon Project Registration Portal',
                description: 'Streamlined process for registering new blue carbon initiatives.'
              },
              {
                date: 'Sep 15, 2025',
                title: 'International Blue Carbon Conference 2025',
                description: 'Key findings and recommendations from the global conference.'
              }
            ].map((update, index) => (
              <div key={index} style={{
                padding: '20px',
                borderBottom: index < 2 ? '1px solid #eee' : 'none'
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '10px'
                }}>
                  <h4 style={{ color: '#007cba', margin: 0 }}>{update.title}</h4>
                  <span style={{ color: '#666', fontSize: '14px' }}>{update.date}</span>
                </div>
                <p style={{ color: '#666', margin: 0, lineHeight: '1.6' }}>{update.description}</p>
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