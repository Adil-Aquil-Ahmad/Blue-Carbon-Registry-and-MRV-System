'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';

export default function LoginPage() {
  const [loginType, setLoginType] = useState('user');
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [keepLoggedIn, setKeepLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      
      login(data.user, data.access_token);

      setTimeout(() => {
        if (data.user.role === 'admin') {
          router.push('/admin');
        } else {
          router.push('/projects');
        }
      }, 100);
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
          marginBottom: '30px',
          color: '#2d3748',
          textAlign: 'center'
        }}>
          Log in
        </h1>

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
              onClick={() => setLoginType('user')}
              style={{
                flex: 1,
                padding: '12px 20px',
                border: 'none',
                backgroundColor: loginType === 'user' ? '#4f46e5' : 'transparent',
                color: loginType === 'user' ? '#fff' : '#64748b',
                borderRadius: '8px',
                fontSize: '15px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: loginType === 'user' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
            >
              NGO / User Login
            </button>
            <button
              type="button"
              onClick={() => setLoginType('admin')}
              style={{
                flex: 1,
                padding: '12px 20px',
                border: 'none',
                backgroundColor: loginType === 'admin' ? '#dc2626' : 'transparent',
                color: loginType === 'admin' ? '#fff' : '#64748b',
                borderRadius: '8px',
                fontSize: '15px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: loginType === 'admin' ? '0 4px 12px rgba(220, 38, 38, 0.3)' : 'none'
              }}
            >
              Admin Login
            </button>
          </div>
        </div>

        <p style={{
          fontSize: '15px',
          marginBottom: '25px',
          color: '#64748b',
          textAlign: 'center'
        }}>
          Don't have an account?{' '}
          <button
            onClick={() => router.push('/auth/register')}
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
            Sign up
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
              Username
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
              placeholder="Enter your username"
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

          <div style={{ marginBottom: '25px' }}>
            <label style={{
              display: 'block',
              fontSize: '15px',
              fontWeight: '600',
              marginBottom: '8px',
              color: '#374151'
            }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                required
                placeholder="Enter your password"
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

          <div style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '25px'
          }}>
            <input
              type="checkbox"
              id="keepLoggedIn"
              checked={keepLoggedIn}
              onChange={(e) => setKeepLoggedIn(e.target.checked)}
              style={{
                marginRight: '8px',
                transform: 'scale(1.2)'
              }}
            />
            <label htmlFor="keepLoggedIn" style={{
              fontSize: '14px',
              color: '#64748b',
              cursor: 'pointer'
            }}>
              Keep me logged in
            </label>
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
              transition: 'all 0.2s ease',
              marginBottom: '15px'
            }}
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>

          <div style={{
            display: 'flex',
            justifyContent: 'center'
          }}>
            <button
              type="button"
              onClick={() => {
                if (loginType === 'admin') {
                  setFormData({ username: 'admin', password: 'admin123' });
                } else {
                  setFormData({ username: '', password: '' });
                }
              }}
              style={{
                background: 'linear-gradient(135deg, #f4a261, #e76f51)',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '10px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: '0 3px 10px rgba(244, 162, 97, 0.4)'
              }}
            >
              {loginType === 'admin' ? 'Fill Admin Credentials' : 'Clear Form'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
