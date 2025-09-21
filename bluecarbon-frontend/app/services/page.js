'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function ServicesPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [location, setLocation] = useState('district');
  const [selectedState, setSelectedState] = useState('');
  const [districtName, setDistrictName] = useState('');
  const [pinCode, setPinCode] = useState('');
  const [isAdvancedSearch, setIsAdvancedSearch] = useState(false);

  const categories = [
    { id: '1', name: 'Blue Carbon Projects', icon: '🌊' },
    { id: '2', name: 'Environmental Clearances', icon: '🌿' },
    { id: '3', name: 'Marine Conservation', icon: '🐟' },
    { id: '4', name: 'Carbon Trading', icon: '💰' },
    { id: '5', name: 'Research & Monitoring', icon: '📊' },
    { id: '6', name: 'Education & Training', icon: '📚' },
    { id: '7', name: 'Coastal Management', icon: '🏖️' },
    { id: '8', name: 'Fisheries & Aquaculture', icon: '🚢' },
    { id: '9', name: 'Tourism & Recreation', icon: '✈️' },
    { id: '10', name: 'Community Services', icon: '👥' }
  ];

  const ministries = [
    { name: 'M/o Environment, Forest & Climate Change', services: 45 },
    { name: 'M/o Earth Sciences', services: 28 },
    { name: 'M/o Fisheries, Animal Husbandry & Dairying', services: 32 },
    { name: 'M/o Shipping', services: 24 },
    { name: 'M/o Tourism', services: 18 },
    { name: 'M/o Science & Technology', services: 21 }
  ];

  const inFocusServices = [
    {
      title: 'Blue Carbon Project Registration Portal',
      description: 'Register your mangrove, seagrass, or salt marsh conservation project for carbon credit verification and trading in the national blue carbon marketplace.'
    },
    {
      title: 'Coastal Zone Environmental Impact Assessment',
      description: 'Submit environmental impact assessments for coastal development projects with automated compliance checking and expert review services.'
    },
    {
      title: 'Marine Protected Area Application System',
      description: 'Apply for designation of marine protected areas or special conservation zones for critical blue carbon ecosystem preservation.'
    }
  ];

  const mostViewed = [
    'Blue Carbon Project Registration',
    'Marine Ecosystem Health Check',
    'Coastal Development Permits',
    'Carbon Credit Verification Status',
    'Mangrove Restoration Guidelines',
    'Fisheries License Renewal'
  ];

  const states = [
    'Andaman and Nicobar Islands', 'Andhra Pradesh', 'Goa', 'Gujarat', 
    'Karnataka', 'Kerala', 'Maharashtra', 'Odisha', 'Tamil Nadu', 
    'West Bengal', 'Puducherry', 'Lakshadweep', 'Daman and Diu'
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    console.log('Searching for:', searchQuery);
  };

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

      {/* Hero Section with Search */}
      <section style={{ background: 'linear-gradient(to right, #2563eb, #1e40af)', color: 'white' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '48px 20px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            {/* Search Section */}
            <div style={{ flex: 1 }}>
              <div style={{ backgroundColor: 'white', borderRadius: '8px', padding: '24px', color: '#111827' }}>
                <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px', margin: 0 }}>
                  Search a <span style={{ color: '#2563eb' }}>Government Service</span>
                </h3>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ display: 'flex' }}>
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Type Keyword (e.g., Blue Carbon, Mangrove, Carbon Credit)"
                      style={{
                        flex: 1,
                        padding: '8px 16px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px 0 0 6px',
                        fontSize: '14px',
                        outline: 'none'
                      }}
                    />
                    <button
                      onClick={handleSearch}
                      style={{
                        padding: '8px 24px',
                        backgroundColor: '#2563eb',
                        color: 'white',
                        border: 'none',
                        borderRadius: '0 6px 6px 0',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center'
                      }}
                    >
                      🔍
                    </button>
                  </div>
                  
                  <button
                    type="button"
                    onClick={() => setIsAdvancedSearch(!isAdvancedSearch)}
                    style={{
                      color: '#2563eb',
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '14px',
                      textAlign: 'left'
                    }}
                  >
                    Advanced Search
                  </button>

                  {isAdvancedSearch && (
                    <div style={{ backgroundColor: '#f9fafb', padding: '16px', borderRadius: '6px' }}>
                      {/* Category Selection */}
                      <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '4px' }}>Category</label>
                        <select
                          value={selectedCategory}
                          onChange={(e) => setSelectedCategory(e.target.value)}
                          style={{
                            width: '100%',
                            padding: '8px 12px',
                            border: '1px solid #d1d5db',
                            borderRadius: '6px',
                            fontSize: '14px',
                            outline: 'none'
                          }}
                        >
                          <option value="">Select Category</option>
                          {categories.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.name}</option>
                          ))}
                        </select>
                      </div>

                      {/* Location Selection */}
                      <div style={{ marginBottom: '16px' }}>
                        <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>Location</label>
                        <div style={{ display: 'flex', gap: '16px', marginBottom: '12px' }}>
                          <label style={{ display: 'flex', alignItems: 'center', fontSize: '14px' }}>
                            <input
                              type="radio"
                              value="district"
                              checked={location === 'district'}
                              onChange={(e) => setLocation(e.target.value)}
                              style={{ marginRight: '8px' }}
                            />
                            State/District
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', fontSize: '14px' }}>
                            <input
                              type="radio"
                              value="pin_code"
                              checked={location === 'pin_code'}
                              onChange={(e) => setLocation(e.target.value)}
                              style={{ marginRight: '8px' }}
                            />
                            Pin Code
                          </label>
                        </div>

                        {location === 'district' ? (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            <select
                              value={selectedState}
                              onChange={(e) => setSelectedState(e.target.value)}
                              style={{
                                width: '100%',
                                padding: '8px 12px',
                                border: '1px solid #d1d5db',
                                borderRadius: '6px',
                                fontSize: '14px',
                                outline: 'none'
                              }}
                            >
                              <option value="">Select Coastal State</option>
                              {states.map((state, index) => (
                                <option key={index} value={state}>{state}</option>
                              ))}
                            </select>
                            <input
                              type="text"
                              value={districtName}
                              onChange={(e) => setDistrictName(e.target.value)}
                              placeholder="District Name"
                              style={{
                                width: '100%',
                                padding: '8px 12px',
                                border: '1px solid #d1d5db',
                                borderRadius: '6px',
                                fontSize: '14px',
                                outline: 'none'
                              }}
                            />
                          </div>
                        ) : (
                          <input
                            type="text"
                            value={pinCode}
                            onChange={(e) => setPinCode(e.target.value)}
                            placeholder="Pin Code"
                            style={{
                              width: '100%',
                              padding: '8px 12px',
                              border: '1px solid #d1d5db',
                              borderRadius: '6px',
                              fontSize: '14px',
                              outline: 'none'
                            }}
                          />
                        )}
                      </div>

                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          onClick={handleSearch}
                          style={{
                            padding: '8px 16px',
                            backgroundColor: '#2563eb',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '14px'
                          }}
                        >
                          Search
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setSearchQuery('');
                            setSelectedCategory('');
                            setSelectedState('');
                            setDistrictName('');
                            setPinCode('');
                          }}
                          style={{
                            padding: '8px 16px',
                            backgroundColor: '#6b7280',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '14px'
                          }}
                        >
                          Reset
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Categories Menu */}
            <div style={{ width: '100%', maxWidth: '600px' }}>
              <div style={{ backgroundColor: '#1e40af', borderRadius: '8px', padding: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '18px', fontWeight: '600', margin: 0 }}>Services related to</h3>
                  <button
                    onClick={() => setIsMenuOpen(!isMenuOpen)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'white',
                      cursor: 'pointer',
                      fontSize: '18px',
                      display: 'block'
                    }}
                  >
                    {isMenuOpen ? '✕' : '☰'}
                  </button>
                </div>
                
                <div style={{ display: isMenuOpen ? 'flex' : 'none', flexDirection: 'column', gap: '8px' }}>
                  {categories.map((category) => (
                    <a
                      key={category.id}
                      href={`/category/${category.id}`}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        padding: '8px',
                        borderRadius: '6px',
                        color: 'white',
                        textDecoration: 'none',
                        transition: 'background-color 0.3s'
                      }}
                      onMouseOver={(e) => e.target.style.backgroundColor = '#2563eb'}
                      onMouseOut={(e) => e.target.style.backgroundColor = 'transparent'}
                    >
                      <span style={{ fontSize: '20px' }}>{category.icon}</span>
                      <span style={{ fontSize: '14px' }}>{category.name}</span>
                    </a>
                  ))}
                </div>
                
                <a
                  href="/categories"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    marginTop: '16px',
                    fontSize: '14px',
                    color: 'white',
                    textDecoration: 'none'
                  }}
                >
                  All Categories →
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Ministry Services Carousel */}
      <section style={{ backgroundColor: 'white', padding: '32px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
            {ministries.map((ministry, index) => (
              <div key={index} style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '16px',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                backgroundColor: 'white',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                transition: 'box-shadow 0.3s ease',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)'}
              onMouseOut={(e) => e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'}
              >
                <div style={{
                  width: '32px',
                  height: '32px',
                  backgroundColor: '#dbeafe',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <span style={{ color: '#2563eb', fontSize: '12px', fontWeight: '600' }}>{ministry.services}</span>
                </div>
                <div style={{ flex: 1 }}>
                  <p style={{ margin: 0, fontSize: '14px' }}>
                    <span style={{ fontWeight: '600' }}>{ministry.services} services</span>
                  </p>
                  <p style={{ margin: 0, fontSize: '12px', color: '#6b7280' }}>{ministry.name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* State Services Banner */}
      <div style={{ backgroundColor: '#eff6ff', padding: '16px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', textAlign: 'center' }}>
          <a href="/state-services" style={{
            display: 'inline-flex',
            alignItems: 'center',
            color: '#2563eb',
            textDecoration: 'none',
            fontWeight: '600',
            fontSize: '16px'
          }}>
            2,847 Services from Coastal States & UTs
            <span style={{ marginLeft: '8px' }}>↗</span>
          </a>
        </div>
      </div>

      {/* Main Content */}
      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '48px 20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '32px' }}>
          {/* In Focus Section */}
          <div>
            <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
              <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '24px', margin: 0, color: '#111827' }}>IN FOCUS</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {inFocusServices.map((service, index) => (
                  <div key={index} style={{
                    borderBottom: index < inFocusServices.length - 1 ? '1px solid #e5e7eb' : 'none',
                    paddingBottom: index < inFocusServices.length - 1 ? '16px' : '0'
                  }}>
                    <h4 style={{
                      fontSize: '16px',
                      fontWeight: '600',
                      marginBottom: '8px',
                      color: '#2563eb',
                      margin: 0
                    }}>
                      <a href="#" style={{ color: '#2563eb', textDecoration: 'none' }}
                         onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
                         onMouseOut={(e) => e.target.style.textDecoration = 'none'}>
                        {service.title}
                      </a>
                    </h4>
                    <p style={{ color: '#374151', fontSize: '14px', lineHeight: '1.5', margin: 0 }}>{service.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {/* Blue Carbon Banner */}
            <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
              <div style={{
                width: '100%',
                height: '192px',
                background: 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '18px',
                fontWeight: '600',
                textAlign: 'center',
                padding: '20px'
              }}>
                🌊 Blue Carbon Initiative<br/>
                <span style={{ fontSize: '14px', fontWeight: '400' }}>Protecting Marine Ecosystems</span>
              </div>
            </div>

            {/* Most Viewed Section */}
            <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
              <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px', margin: 0, color: '#111827' }}>Most Viewed</h3>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {mostViewed.map((service, index) => (
                  <li key={index}>
                    <a 
                      href="#" 
                      style={{
                        color: '#2563eb',
                        fontSize: '14px',
                        textDecoration: 'none',
                        display: 'block',
                        padding: '4px 0'
                      }}
                      onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
                      onMouseOut={(e) => e.target.style.textDecoration = 'none'}
                    >
                      {service}
                    </a>
                  </li>
                ))}
              </ul>
              <a href="/most-viewed" style={{
                color: '#2563eb',
                fontSize: '14px',
                textDecoration: 'none',
                marginTop: '16px',
                display: 'inline-block'
              }}
              onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
              onMouseOut={(e) => e.target.style.textDecoration = 'none'}>
                More
              </a>
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