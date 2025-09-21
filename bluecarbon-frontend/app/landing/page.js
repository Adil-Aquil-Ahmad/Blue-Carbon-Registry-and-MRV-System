'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import { useEffect } from 'react';

export default function LandingPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/projects');
    }
  }, [isAuthenticated, router]);

  return (
    <div style={{
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundImage: 'url("/one.jpg")', // Replace "one.jpg" with your actual image filename
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: 'fixed'
    }}>
      {/* Top Header Bar */}
      <section style={{
        backgroundColor: 'rgba(248, 248, 248, 0.95)',
        padding: '10px 0',
        borderBottom: '1px solid #ddd',
        fontSize: '14px',
        backdropFilter: 'blur(10px)'
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
            <a href="#main-content" style={{ color: '#007cba', textDecoration: 'none' }}>Skip to main content</a>
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
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        padding: '20px 0',
        borderBottom: '1px solid #ddd',
        backdropFilter: 'blur(10px)'
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
                bluecarbon.gov.in
              </h1>
              <p style={{
                margin: 0,
                fontSize: '16px',
                color: '#007cba',
                fontStyle: 'italic'
              }}>
                national portal of blue carbon registry
              </p>
            </div>
          </div>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '40px'
          }}>
            <div style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: '10px'
            }}
            onClick={() => router.push('/topics')}
            >
              <div style={{
                width: '50px',
                height: '50px',
                backgroundColor: '#f0f0f0',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                fontSize: '20px'
              }}>
                📊
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>TOPICS</span>
            </div>
            
            <div style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: '10px'
            }}
            onClick={() => router.push('/services')}
            >
              <div style={{
                width: '50px',
                height: '50px',
                backgroundColor: '#f0f0f0',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                fontSize: '20px'
              }}>
                🏛️
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>SERVICES</span>
            </div>
            
            <div style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: '10px'
            }}
            onClick={() => router.push('/my-government')}
            >
              <div style={{
                width: '50px',
                height: '50px',
                backgroundColor: '#f0f0f0',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                fontSize: '20px'
              }}>
                🏢
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>MY GOVERNMENT</span>
            </div>
            
            <div style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: '10px'
            }}
            onClick={() => router.push('/people-groups')}
            >
              <div style={{
                width: '50px',
                height: '50px',
                backgroundColor: '#f0f0f0',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                fontSize: '20px'
              }}>
              👥
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>PEOPLE GROUPS</span>
            </div>
            
            <div style={{
              textAlign: 'center',
              cursor: 'pointer',
              padding: '10px'
            }}
            onClick={() => router.push('/topics')}
            >
              <div style={{
                width: '50px',
                height: '50px',
                backgroundColor: '#f0f0f0',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 8px',
                fontSize: '20px'
              }}>
                🌍
              </div>
              <span style={{ fontSize: '12px', color: '#666' }}>BLUE CARBON</span>
            </div>
          </div>
        </div>
      </section>

      {/* Search Section */}
      <section style={{
        backgroundColor: 'rgba(74, 144, 226, 0.9)',
        padding: '20px 0',
        color: 'white',
        backdropFilter: 'blur(10px)'
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
            gap: '15px',
            flex: 1
          }}>
            <input
              type="text"
              placeholder="Search - Keyword, Phrase"
              style={{
                padding: '12px 16px',
                border: 'none',
                borderRadius: '4px',
                fontSize: '16px',
                width: '400px',
                outline: 'none'
              }}
            />
            <button
              style={{
                padding: '12px 24px',
                backgroundColor: '#FF8C00',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              Search
            </button>
            <button
              style={{
                background: 'none',
                border: '1px solid rgba(255,255,255,0.5)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Advanced Search ▼
            </button>
          </div>
          
          <div style={{
            backgroundColor: 'rgba(255,255,255,0.1)',
            padding: '15px',
            borderRadius: '8px',
            minWidth: '200px'
          }}>
            <h3 style={{
              margin: '0 0 10px 0',
              fontSize: '14px',
              fontWeight: 'bold',
              color: 'white'
            }}>
              MOST SEARCHED
            </h3>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '5px'
            }}>
              <a href="#" style={{ color: 'white', textDecoration: 'none', fontSize: '12px' }}>Birth Certificate</a>
              <a href="#" style={{ color: 'white', textDecoration: 'none', fontSize: '12px' }}>Project Registration</a>
              <a href="#" style={{ color: 'white', textDecoration: 'none', fontSize: '12px' }}>Carbon Credits</a>
            </div>
          </div>
        </div>
      </section>

      {/* Hero Banner Section */}
      <section style={{
        background: 'rgba(30, 60, 114, 0.7)', // Semi-transparent overlay instead of solid gradient
        color: 'white',
        padding: '60px 0',
        position: 'relative',
        backdropFilter: 'blur(2px)'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px',
          display: 'grid',
          gridTemplateColumns: '2fr 1fr',
          gap: '40px',
          alignItems: 'center'
        }}>
          <div>
            <h2 style={{
              fontSize: '48px',
              fontWeight: 'bold',
              margin: '0 0 20px 0',
              lineHeight: '1.1',
              color: '#FFD700'
            }}>
              Share your ideas & Suggestions with MRV for
            </h2>
            <h1 style={{
              fontSize: '64px',
              fontWeight: 'bold',
              margin: '0 0 20px 0',
              background: 'linear-gradient(45deg, #FF6B35, #F7931E, #FFD700)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              lineHeight: '1.1'
            }}>
              Blue Carbon
            </h1>
            <p style={{
              fontSize: '24px',
              margin: '0 0 30px 0',
              fontWeight: 'normal'
            }}>
              on 28<sup>th</sup> Sep 2025
            </p>
            <div style={{
              backgroundColor: 'rgba(255,255,255,0.1)',
              padding: '20px',
              borderRadius: '8px',
              marginBottom: '30px'
            }}>
              <p style={{ margin: '0 0 10px 0', fontSize: '18px', fontWeight: 'bold' }}>
                Click Here or Register for Blue Carbon MRV
              </p>
              <p style={{ margin: 0, fontSize: '14px' }}>
                The registration portal shall remain open from 5th - 26th September 2025
              </p>
            </div>
            <div style={{
              display: 'flex',
              gap: '20px'
            }}>
              <button
                onClick={() => router.push('/auth/register')}
                style={{
                  background: 'linear-gradient(135deg, #10b981, #059669)',
                  color: 'white',
                  border: 'none',
                  padding: '15px 30px',
                  borderRadius: '8px',
                  fontSize: '18px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)'
                }}
              >
                Register Now
              </button>
              <button
                onClick={() => router.push('/auth/login')}
                style={{
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  border: '2px solid rgba(255, 255, 255, 0.5)',
                  padding: '15px 30px',
                  borderRadius: '8px',
                  fontSize: '18px',
                  fontWeight: 'bold',
                  cursor: 'pointer'
                }}
              >
                Login
              </button>
            </div>
          </div>
          
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center'
          }}>
            <div style={{
              background: 'rgba(255,255,255,0.1)',
              borderRadius: '20px',
              padding: '30px',
              textAlign: 'center',
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{
                margin: '0 0 20px 0',
                fontSize: '24px',
                color: '#FFD700'
              }}>
                Blue Carbon MRV Platform
              </h3>
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '15px',
                marginBottom: '20px'
              }}>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '15px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 'bold'
                }}>
                  Projects
                </div>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '15px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 'bold'
                }}>
                  Evidence
                </div>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '15px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 'bold'
                }}>
                  Verification
                </div>
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: '15px',
                  borderRadius: '8px',
                  fontSize: '14px',
                  fontWeight: 'bold'
                }}>
                  Credits
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Three Column Content Section */}
      <section style={{
        padding: '40px 0',
        backgroundColor: 'rgba(248, 249, 250, 0.9)',
        backdropFilter: 'blur(10px)'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 20px',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: '30px'
        }}>
          {/* News Highlights */}
          <div style={{
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{
              backgroundColor: '#666',
              color: 'white',
              padding: '10px 15px',
              margin: '-20px -20px 20px -20px',
              borderRadius: '8px 8px 0 0',
              fontSize: '16px',
              fontWeight: 'bold'
            }}>
              News & Press Releases
            </div>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0
            }}>
              <li style={{ marginBottom: '15px', paddingLeft: '15px', position: 'relative' }}>
                <span style={{ position: 'absolute', left: '0', top: '0', color: '#007cba' }}>»</span>
                <a href="#" style={{ color: '#333', textDecoration: 'none', fontSize: '14px', lineHeight: '1.4' }}>
                  Blue Carbon projects secure exclusive rights to explore coastal ecosystems...
                </a>
              </li>
              <li style={{ marginBottom: '15px', paddingLeft: '15px', position: 'relative' }}>
                <span style={{ position: 'absolute', left: '0', top: '0', color: '#007cba' }}>»</span>
                <a href="#" style={{ color: '#333', textDecoration: 'none', fontSize: '14px', lineHeight: '1.4' }}>
                  MRV framework crucial for global carbon prosperity, says PM Modi
                </a>
              </li>
              <li style={{ marginBottom: '15px', paddingLeft: '15px', position: 'relative' }}>
                <span style={{ position: 'absolute', left: '0', top: '0', color: '#007cba' }}>»</span>
                <a href="#" style={{ color: '#333', textDecoration: 'none', fontSize: '14px', lineHeight: '1.4' }}>
                  New carbon credit regulations announced for coastal restoration
                </a>
              </li>
            </ul>
            <div style={{ textAlign: 'right', marginTop: '20px' }}>
              <a href="#" style={{ color: '#007cba', fontSize: '12px', textDecoration: 'none' }}>more news..</a>
            </div>
          </div>

          {/* Most Requested Information */}
          <div style={{
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{
              backgroundColor: '#f0f0f0',
              color: '#333',
              padding: '10px 15px',
              margin: '-20px -20px 20px -20px',
              borderRadius: '8px 8px 0 0',
              fontSize: '16px',
              fontWeight: 'bold',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              Information
              <span style={{ fontSize: '20px' }}>📊</span>
            </div>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0
            }}>
              <li style={{ marginBottom: '12px' }}>
                <a href="#" style={{ color: '#007cba', textDecoration: 'none', fontSize: '14px' }}>
                  » Project Registration Guidelines
                </a>
              </li>
              <li style={{ marginBottom: '12px' }}>
                <a href="#" style={{ color: '#007cba', textDecoration: 'none', fontSize: '14px' }}>
                  » Carbon Credit Verification Process
                </a>
              </li>
              <li style={{ marginBottom: '12px' }}>
                <a href="#" style={{ color: '#007cba', textDecoration: 'none', fontSize: '14px' }}>
                  » MRV Documentation Requirements
                </a>
              </li>
              <li style={{ marginBottom: '12px' }}>
                <a href="#" style={{ color: '#007cba', textDecoration: 'none', fontSize: '14px' }}>
                  » Coastal Ecosystem Assessment Forms
                </a>
              </li>
              <li style={{ marginBottom: '12px' }}>
                <a href="#" style={{ color: '#007cba', textDecoration: 'none', fontSize: '14px' }}>
                  » Blue Carbon Registry Portal
                </a>
              </li>
            </ul>
          </div>

          {/* Activities & Initiatives */}
          <div style={{
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            backdropFilter: 'blur(10px)'
          }}>
            <h3 style={{
              margin: '0 0 20px 0',
              fontSize: '16px',
              fontWeight: 'bold',
              color: '#333'
            }}>
              Activities & Initiatives
            </h3>
            
            <div style={{
              border: '1px solid #ddd',
              borderRadius: '8px',
              overflow: 'hidden',
              marginBottom: '20px'
            }}>
              <div style={{
                padding: '15px',
                backgroundColor: '#f8f9fa'
              }}>
                <img 
                  src="/logo_1.png" 
                  alt="Blue Carbon Initiative" 
                  style={{
                    width: '40px',
                    height: '40px',
                    float: 'left',
                    marginRight: '15px',
                    objectFit: 'contain'
                  }}
                />
                <h4 style={{
                  margin: '0 0 5px 0',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  color: '#333'
                }}>
                  International Year of Blue Carbon
                </h4>
                <p style={{
                  margin: 0,
                  fontSize: '12px',
                  color: '#666',
                  lineHeight: '1.4'
                }}>
                  On this occasion, various programs & discussions related to blue carbon are being organized throughout the year
                </p>
              </div>
            </div>

            <div style={{
              backgroundColor: '#e8f4f8',
              padding: '15px',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <h4 style={{
                margin: '0 0 10px 0',
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#007cba'
              }}>
                Blue Carbon MRV Portal
              </h4>
              <p style={{
                margin: '0 0 10px 0',
                fontSize: '12px',
                color: '#333'
              }}>
                Digital platform for monitoring, reporting & verification
              </p>
            </div>
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