'use client';

import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function Navigation() {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const router = useRouter();

  if (!isAuthenticated()) {
    return (
      <nav className="nav">
        <div className="brand">
          <div className="logo">BC</div>
          <div>
            BlueCarbon MRV
            <div className="small text-gray-500">Registry & Tokenization</div>
          </div>
        </div>
        
        <div className="flex gap-3 items-center">
          <button onClick={() => router.push('/auth/login')} className="btn">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 0a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Login
          </button>
          <button onClick={() => router.push('/auth/register')} className="btn secondary">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            Register
          </button>
        </div>
      </nav>
    );
  }

  return (
    <nav className="nav">
      <div className="brand">
        <div className="logo">BC</div>
        <div>
          BlueCarbon MRV
          <div className="small text-gray-500">Registry & Tokenization</div>
        </div>
      </div>

      <div className="flex gap-3 items-center">
        {(user?.role === 'ngo' && !isAdmin()) && (
          <button onClick={() => router.push('/projects/new')} className="btn secondary">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Project
          </button>
        )}
        
        {!isAdmin() && (
          <button onClick={() => router.push('/upload')} className="btn secondary">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Upload Evidence
          </button>
        )}
        
        <div className="flex items-center gap-4 pl-6 border-l border-gray-300">
          <div className="text-right">
            <div className="text-sm font-semibold text-gray-700">{user?.username}</div>
            <div className="text-xs text-gray-500">
              {user?.role?.toUpperCase()} {user?.organization_name && `• ${user.organization_name}`}
            </div>
          </div>
          <button 
            onClick={logout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 0a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}