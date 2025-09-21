'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const [userRole, setUserRole] = useState('ngo'); // 'ngo', 'gram_panchayat', or 'individual'
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    organization_name: '',
    wallet_address: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          role: userRole,
          organization_name: formData.organization_name || null,
          wallet_address: formData.wallet_address || null
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user_info', JSON.stringify(data.user));
      router.push('/projects');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#ffffff'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '500px',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        padding: '50px 60px',
        borderRadius: '24px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
        border: '1px solid rgba(255, 255, 255, 0.3)'
      }}>
        <div style={{
          marginBottom: '20px',
          textAlign: 'left'
        }}>
          <button
            onClick={() => router.push('/landing')}
            style={{
              background: 'transparent',
              color: '#64748b',
              border: 'none',
              padding: '8px 0',
              fontSize: '14px',
              fontWeight: '500',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'color 0.2s ease'
            }}
            onMouseOver={(e) => {
              e.target.style.color = '#3b82f6';
            }}
            onMouseOut={(e) => {
              e.target.style.color = '#64748b';
            }}
          >
            ← Back to Home
          </button>
        </div>
        
        <h1 style={{
          fontSize: '32px',
          fontWeight: '600',
          marginBottom: '10px',
          color: '#2d3748',
          textAlign: 'center'
        }}>
          Create Account
        </h1>

        <p style={{
          fontSize: '16px',
          marginBottom: '20px',
          color: '#64748b',
          textAlign: 'center'
        }}>
          Join the Blue Carbon Registry
        </p>

        <p style={{
          fontSize: '15px',
          marginBottom: '30px',
          color: '#64748b',
          textAlign: 'center'
        }}>
          Already have an account?{' '}
          <button
            onClick={() => router.push('/auth/login')}
            style={{
              background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
              color: 'white',
              border: 'none',
              padding: '6px 12px',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              borderRadius: '6px',
              boxShadow: '0 2px 8px rgba(59, 130, 246, 0.3)'
            }}
          >
            Sign in
          </button>
        </p>

        {/* Role Selector */}
        <div style={{ marginBottom: '25px' }}>
          <div style={{
            display: 'flex',
            backgroundColor: '#f8fafc',
            border: '2px solid #e2e8f0',
            borderRadius: '12px',
            padding: '4px',
            gap: '4px'
          }}>
            <button
              type="button"
              onClick={() => setUserRole('ngo')}
              style={{
                flex: 1,
                padding: '12px 16px',
                border: 'none',
                backgroundColor: userRole === 'ngo' ? '#4f46e5' : 'transparent',
                color: userRole === 'ngo' ? '#fff' : '#64748b',
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: userRole === 'ngo' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
            >
              NGO
            </button>
            <button
              type="button"
              onClick={() => setUserRole('gram_panchayat')}
              style={{
                flex: 1,
                padding: '12px 16px',
                border: 'none',
                backgroundColor: userRole === 'gram_panchayat' ? '#10b981' : 'transparent',
                color: userRole === 'gram_panchayat' ? '#fff' : '#64748b',
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: userRole === 'gram_panchayat' ? '0 4px 12px rgba(16, 185, 129, 0.3)' : 'none'
              }}
            >
              Gram Panchayat
            </button>
            <button
              type="button"
              onClick={() => setUserRole('individual')}
              style={{
                flex: 1,
                padding: '12px 16px',
                border: 'none',
                backgroundColor: userRole === 'individual' ? '#f59e0b' : 'transparent',
                color: userRole === 'individual' ? '#fff' : '#64748b',
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: userRole === 'individual' ? '0 4px 12px rgba(245, 158, 11, 0.3)' : 'none'
              }}
            >
              Individual
            </button>
          </div>
        </div>

        <p style={{
          fontSize: '15px',
          marginBottom: '25px',
          color: '#64748b',
          textAlign: 'center'
        }}>
          Already have an account?{' '}
          <button
            onClick={() => router.push('/auth/login')}
            style={{
              background: 'linear-gradient(135deg, #10b981, #059669)',
              color: 'white',
              border: 'none',
              padding: '6px 12px',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              borderRadius: '6px',
              boxShadow: '0 2px 8px rgba(16, 185, 129, 0.3)'
            }}
          >
            Sign in
          </button>
        </p>

        {error && (
          <div style={{
            backgroundColor: '#fef2f2',
            color: '#dc2626',
            padding: '15px',
            borderRadius: '12px',
            marginBottom: '25px',
            fontSize: '15px',
            border: '1px solid #fecaca',
            fontWeight: '500'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              fontSize: '15px',
              fontWeight: '600',
              marginBottom: '8px',
              color: '#374151'
            }}>
              Username *
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              placeholder="Choose a username"
              style={{
                width: '100%',
                padding: '14px 16px',
                border: '2px solid #e5e7eb',
                borderRadius: '12px',
                fontSize: '15px',
                boxSizing: 'border-box',
                transition: 'all 0.2s ease',
                backgroundColor: '#fafafa'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              fontSize: '15px',
              fontWeight: '600',
              marginBottom: '8px',
              color: '#374151'
            }}>
              Email *
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="Enter your email address"
              style={{
                width: '100%',
                padding: '14px 16px',
                border: '2px solid #e5e7eb',
                borderRadius: '12px',
                fontSize: '15px',
                boxSizing: 'border-box',
                transition: 'all 0.2s ease',
                backgroundColor: '#fafafa'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              fontSize: '15px',
              fontWeight: '600',
              marginBottom: '8px',
              color: '#374151'
            }}>
              Password *
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                placeholder="Create a strong password"
                style={{
                  width: '100%',
                  padding: '14px 16px',
                  paddingRight: '60px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa'
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                  color: 'white',
                  border: 'none',
                  padding: '6px 10px',
                  fontSize: '12px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  borderRadius: '6px'
                }}
              >
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '25px' }}>
            <label style={{
              display: 'block',
              fontSize: '15px',
              fontWeight: '600',
              marginBottom: '8px',
              color: '#374151'
            }}>
              Confirm Password *
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showConfirmPassword ? "text" : "password"}
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                required
                placeholder="Confirm your password"
                style={{
                  width: '100%',
                  padding: '14px 16px',
                  paddingRight: '60px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  fontSize: '15px',
                  boxSizing: 'border-box',
                  transition: 'all 0.2s ease',
                  backgroundColor: '#fafafa'
                }}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'linear-gradient(135deg, #f59e0b, #d97706)',
                  color: 'white',
                  border: 'none',
                  padding: '6px 10px',
                  fontSize: '12px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  borderRadius: '6px'
                }}
              >
                {showConfirmPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            style={{
              width: '100%',
              background: isLoading ? '#9ca3af' : 'linear-gradient(135deg, #4f46e5, #7c3aed)',
              color: 'white',
              border: 'none',
              padding: '16px 24px',
              borderRadius: '12px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  );
}
