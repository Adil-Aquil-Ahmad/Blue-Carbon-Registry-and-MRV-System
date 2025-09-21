'use client';

import { useRouter } from 'next/navigation';

export default function TermsAndConditions() {
  const router = useRouter();

  return (
    <div style={{
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff'
    }}>
      {/* Main Header - Same as landing page */}
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
              Terms and Conditions
            </h1>
            <p style={{
              fontSize: '18px',
              color: '#666',
              margin: 0
            }}>
              Blue Carbon Services Portal - Terms of Use
            </p>
          </div>

          {/* Last Updated */}
          <div style={{ marginBottom: '32px', padding: '16px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
            <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
              <strong>Last Updated:</strong> September 21, 2025
            </p>
          </div>

          {/* Terms Content */}
          <div style={{ lineHeight: '1.8', color: '#374151' }}>
            
            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              1. Acceptance of Terms
            </h2>
            <p style={{ marginBottom: '16px' }}>
              By accessing and using the Blue Carbon Services Portal ("Portal"), you accept and agree to be bound by the terms and provision of this agreement. This Portal is operated by the Government of India for providing marine conservation and blue carbon services information.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              2. Use License
            </h2>
            <p style={{ marginBottom: '16px' }}>
              Permission is granted to temporarily access the materials on the Blue Carbon Services Portal for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>modify or copy the materials;</li>
              <li>use the materials for any commercial purpose or for any public display;</li>
              <li>attempt to reverse engineer any software contained on the Portal;</li>
              <li>remove any copyright or other proprietary notations from the materials.</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              3. Service Information Accuracy
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The materials on the Blue Carbon Services Portal are provided on an 'as is' basis. The Government of India makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              4. Data Privacy and Protection
            </h2>
            <p style={{ marginBottom: '16px' }}>
              Your privacy is important to us. Personal information collected through this Portal is governed by the Government of India's Privacy Policy and applicable data protection laws. We are committed to protecting your personal data and ensuring its security.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              5. Blue Carbon Project Registration
            </h2>
            <p style={{ marginBottom: '16px' }}>
              Users registering blue carbon projects agree to provide accurate, complete, and up-to-date information. All project data submitted will be subject to verification processes as per national blue carbon standards and environmental regulations.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              6. Limitations
            </h2>
            <p style={{ marginBottom: '16px' }}>
              In no event shall the Government of India or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on the Portal, even if the Government of India or its authorized representative has been notified orally or in writing of the possibility of such damage.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              7. Accuracy of Materials
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The materials appearing on the Blue Carbon Services Portal could include technical, typographical, or photographic errors. The Government of India does not warrant that any of the materials on its Portal are accurate, complete, or current. The Government of India may make changes to the materials contained on its Portal at any time without notice.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              8. Links
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The Government of India has not reviewed all of the sites linked to our Portal and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by the Government of India of the site. Use of any such linked website is at the user's own risk.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              9. Modifications
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The Government of India may revise these terms of service for its Portal at any time without notice. By using this Portal, you are agreeing to be bound by the then current version of these terms of service.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              10. Governing Law
            </h2>
            <p style={{ marginBottom: '16px' }}>
              These terms and conditions are governed by and construed in accordance with the laws of India and you irrevocably submit to the exclusive jurisdiction of the courts in that State or location.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              11. Contact Information
            </h2>
            <p style={{ marginBottom: '16px' }}>
              If you have any questions about these Terms and Conditions, please contact us through the Help & Support section of this Portal or through the official government channels provided.
            </p>

            {/* Acceptance Notice */}
            <div style={{ 
              marginTop: '40px', 
              padding: '20px', 
              backgroundColor: '#eff6ff', 
              borderLeft: '4px solid #2563eb',
              borderRadius: '0 8px 8px 0'
            }}>
              <p style={{ margin: 0, fontWeight: '600', color: '#1e3a8a' }}>
                By using the Blue Carbon Services Portal, you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Services Count Section - Same as your Services page */}
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

      {/* Footer - Same as your Services page */}
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