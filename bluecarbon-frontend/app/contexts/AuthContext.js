'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check for stored auth data on component mount
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user_info');
    
    if (token && userInfo) {
      try {
        const parsedUser = JSON.parse(userInfo);
        setUser(parsedUser);
        
        // Verify token is still valid
        verifyToken(token);
      } catch (error) {
        console.error('Error parsing user info:', error);
        logout();
      }
    }
    
    setIsLoading(false);
  }, []);

  const verifyToken = async (token, forceLogoutOnFail = false) => {
    try {
      const response = await fetch('http://localhost:8000/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Token verification failed');
      }
      
      const userData = await response.json();
      setUser(userData);
      return true;
    } catch (error) {
      console.error('Token verification failed:', error);
      if (forceLogoutOnFail) {
        logout();
      } else {
        // Keep user logged in locally if verification fails (e.g., server down)
        console.warn('Token verification failed, but keeping user logged in locally');
      }
      return false;
    }
  };

  const login = (userData, token) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_info', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    setUser(null);
    router.push('/auth/login');
  };

  const getAuthToken = () => {
    return localStorage.getItem('access_token');
  };

  const isAuthenticated = () => {
    return !!user;
  };

  const isAdmin = () => {
    return user?.role === 'admin';
  };

  const isNGO = () => {
    return user?.role === 'ngo';
  };

  const value = {
    user,
    isLoading,
    login,
    logout,
    getAuthToken,
    isAuthenticated,
    isAdmin,
    isNGO
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Higher-order component for protecting routes
export function withAuth(Component, requiredRole = null) {
  return function AuthenticatedComponent(props) {
    const { user, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!isLoading) {
        if (!user) {
          router.push('/auth/login');
          return;
        }
        
        if (requiredRole && user.role !== requiredRole) {
          router.push('/unauthorized');
          return;
        }
      }
    }, [user, isLoading, router]);

    if (isLoading) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      );
    }

    if (!user || (requiredRole && user.role !== requiredRole)) {
      return null;
    }

    return <Component {...props} />;
  };
}