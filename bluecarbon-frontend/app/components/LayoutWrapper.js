'use client';

import { usePathname } from 'next/navigation';
import Navigation from './Navigation';

export default function LayoutWrapper({ children }) {
  const pathname = usePathname();
  
  // Check if we're on auth pages (login/register)
  const isAuthPage = pathname?.startsWith('/auth/');
  
  if (isAuthPage) {
    // For auth pages, render without container and navigation
    return <main>{children}</main>;
  }
  
  // For all other pages, render with container, navigation, and footer
  return (
    <div className="container">
      <Navigation />
      <main>{children}</main>
      
      <footer style={{ marginTop: 28, textAlign: 'center', color: '#94a3b8' }}>
        © NCCR · Blockchain BlueCarbon MRV Demo — Adapt UI freely
      </footer>
    </div>
  );
}