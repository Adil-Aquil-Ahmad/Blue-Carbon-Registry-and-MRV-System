'use client';

import { useRouter } from 'next/navigation';

export default function WebsitePolicyPage() {
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
              Website Policy
            </h1>
            <p style={{
              fontSize: '18px',
              color: '#666',
              margin: 0
            }}>
              Blue Carbon Services Portal - Usage Guidelines and Policies
            </p>
          </div>

          {/* Last Updated */}
          <div style={{ marginBottom: '32px', padding: '16px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
            <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
              <strong>Last Updated:</strong> September 21, 2025 | <strong>Version:</strong> 2.1
            </p>
          </div>

          {/* Policy Content */}
          <div style={{ lineHeight: '1.8', color: '#374151' }}>
            
            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              1. Website Overview
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The Blue Carbon Services Portal is an official Government of India website designed to provide comprehensive access to marine conservation and blue carbon services. This portal serves as a single-window platform for citizens, organizations, and stakeholders to access information, services, and resources related to blue carbon ecosystems and marine conservation.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              2. Purpose and Scope
            </h2>
            <p style={{ marginBottom: '16px' }}>
              This website facilitates:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>Access to blue carbon project registration and management services</li>
              <li>Information about marine ecosystem conservation programs</li>
              <li>Environmental clearance and permit application processes</li>
              <li>Carbon credit verification and trading mechanisms</li>
              <li>Research resources and monitoring protocols</li>
              <li>Educational materials and capacity building programs</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              3. Content Policy
            </h2>
            <h3 style={{ fontSize: '20px', fontWeight: '500', color: '#1e3a8a', marginTop: '24px', marginBottom: '12px' }}>
              3.1 Information Accuracy
            </h3>
            <p style={{ marginBottom: '16px' }}>
              We strive to ensure that all information published on this portal is accurate, up-to-date, and reliable. However, the information is provided "as is" and the Government of India makes no warranties regarding its completeness or accuracy. Users are advised to verify critical information through official channels.
            </p>

            <h3 style={{ fontSize: '20px', fontWeight: '500', color: '#1e3a8a', marginTop: '24px', marginBottom: '12px' }}>
              3.2 Content Updates
            </h3>
            <p style={{ marginBottom: '16px' }}>
              The portal content is regularly updated to reflect changes in policies, procedures, and available services. Users are encouraged to check for updates regularly, especially when accessing regulatory information or submitting applications.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              4. User Responsibilities
            </h2>
            <p style={{ marginBottom: '16px' }}>
              Users of this portal agree to:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>Provide accurate and truthful information in all submissions</li>
              <li>Use the portal only for legitimate and legal purposes</li>
              <li>Respect intellectual property rights and copyright restrictions</li>
              <li>Not attempt to disrupt or compromise the portal's security</li>
              <li>Follow all applicable laws and regulations</li>
              <li>Maintain the confidentiality of login credentials</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              5. Privacy and Data Protection
            </h2>
            <h3 style={{ fontSize: '20px', fontWeight: '500', color: '#1e3a8a', marginTop: '24px', marginBottom: '12px' }}>
              5.1 Data Collection
            </h3>
            <p style={{ marginBottom: '16px' }}>
              We collect personal information only when necessary for providing services. This includes registration details, project information, and communication preferences. All data collection complies with applicable privacy laws and regulations.
            </p>

            <h3 style={{ fontSize: '20px', fontWeight: '500', color: '#1e3a8a', marginTop: '24px', marginBottom: '12px' }}>
              5.2 Data Security
            </h3>
            <p style={{ marginBottom: '16px' }}>
              We implement appropriate technical and organizational measures to protect personal data against unauthorized access, alteration, disclosure, or destruction. However, no internet transmission is completely secure, and users share responsibility for protecting their account information.
            </p>

            <h3 style={{ fontSize: '20px', fontWeight: '500', color: '#1e3a8a', marginTop: '24px', marginBottom: '12px' }}>
              5.3 Data Sharing
            </h3>
            <p style={{ marginBottom: '16px' }}>
              Personal data may be shared with relevant government departments and agencies as required for service delivery, regulatory compliance, or legal obligations. Data is not shared with third parties for commercial purposes without explicit consent.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              6. Accessibility Commitment
            </h2>
            <p style={{ marginBottom: '16px' }}>
              We are committed to making this portal accessible to all users, including those with disabilities. The portal follows Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards. Features include:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>Screen reader compatibility</li>
              <li>Keyboard navigation support</li>
              <li>Text size adjustment options</li>
              <li>High contrast display modes</li>
              <li>Alternative text for images</li>
              <li>Clear navigation structure</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              7. Technical Requirements
            </h2>
            <p style={{ marginBottom: '16px' }}>
              For optimal experience, we recommend:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>Modern web browsers (Chrome, Firefox, Safari, Edge - latest versions)</li>
              <li>JavaScript enabled</li>
              <li>Stable internet connection</li>
              <li>PDF reader for downloading documents</li>
              <li>Email access for notifications and correspondence</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              8. Service Availability
            </h2>
            <p style={{ marginBottom: '16px' }}>
              While we strive to maintain 24/7 availability, the portal may occasionally be unavailable due to:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>Scheduled maintenance</li>
              <li>System upgrades</li>
              <li>Technical difficulties</li>
              <li>Emergency security measures</li>
            </ul>
            <p style={{ marginBottom: '16px' }}>
              Planned maintenance will be announced in advance when possible. Critical services may have alternative access methods during downtime.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              9. External Links Policy
            </h2>
            <p style={{ marginBottom: '16px' }}>
              This portal may contain links to external websites operated by other government departments, organizations, or service providers. We are not responsible for the content, privacy practices, or availability of external sites. Users should review the policies of external sites before sharing personal information.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              10. Intellectual Property
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The content, design, and structure of this portal are protected by copyright and other intellectual property laws. Government logos, emblems, and official documents remain the property of the Government of India. Users may access and use information for personal and non-commercial purposes, with proper attribution.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              11. Limitation of Liability
            </h2>
            <p style={{ marginBottom: '16px' }}>
              The Government of India shall not be liable for any direct, indirect, incidental, or consequential damages arising from the use of this portal or reliance on the information provided. This includes, but is not limited to, loss of data, business interruption, or financial losses.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              12. Feedback and Complaints
            </h2>
            <p style={{ marginBottom: '16px' }}>
              We welcome feedback about the portal and its services. Users can submit comments, suggestions, or complaints through:
            </p>
            <ul style={{ marginBottom: '16px', paddingLeft: '24px' }}>
              <li>The Help & Support section</li>
              <li>Contact forms available on relevant service pages</li>
              <li>Official email addresses provided for specific departments</li>
              <li>Grievance redressal mechanisms as applicable</li>
            </ul>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              13. Policy Updates
            </h2>
            <p style={{ marginBottom: '16px' }}>
              This Website Policy may be updated periodically to reflect changes in technology, law, or portal functionality. Significant changes will be communicated through portal notifications or announcements. Users are encouraged to review this policy regularly.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              14. Governing Law and Jurisdiction
            </h2>
            <p style={{ marginBottom: '16px' }}>
              This Website Policy is governed by the laws of India. Any disputes arising from the use of this portal shall be subject to the jurisdiction of Indian courts. International users should be aware that Indian law governs all portal activities and data processing.
            </p>

            <h2 style={{ fontSize: '24px', fontWeight: '600', color: '#1e3a8a', marginTop: '32px', marginBottom: '16px' }}>
              15. Contact Information
            </h2>
            <p style={{ marginBottom: '16px' }}>
              For questions about this Website Policy or portal usage, please contact:
            </p>
            <div style={{ 
              padding: '20px', 
              backgroundColor: '#f8f9fa', 
              borderRadius: '8px',
              marginBottom: '16px'
            }}>
              <p style={{ margin: '0 0 8px 0', fontWeight: '600' }}>Blue Carbon Services Portal Support</p>
              <p style={{ margin: '0 0 4px 0' }}>Ministry of Environment, Forest and Climate Change</p>
              <p style={{ margin: '0 0 4px 0' }}>Government of India</p>
              <p style={{ margin: '0 0 4px 0' }}>Email: support@bluecarbonservices.gov.in</p>
              <p style={{ margin: 0 }}>Help Desk: Available through the Help & Support section</p>
            </div>

            {/* Acknowledgment Notice */}
            <div style={{ 
              marginTop: '40px', 
              padding: '20px', 
              backgroundColor: '#eff6ff', 
              borderLeft: '4px solid #2563eb',
              borderRadius: '0 8px 8px 0'
            }}>
              <p style={{ margin: 0, fontWeight: '600', color: '#1e3a8a' }}>
                By using the Blue Carbon Services Portal, you acknowledge that you have read, understood, and agree to comply with this Website Policy and all applicable terms of service.
              </p>
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
            <span style={{
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              backgroundColor: 'rgba(255,255,255,0.1)',
              padding: '4px 8px',
              borderRadius: '4px'
            }}>
              Website Policy
            </span>
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