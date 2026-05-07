'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Topbar from './Topbar';
import Sidebar from './Sidebar';
import DemoNav from './DemoNav';

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [isAuth, setIsAuth] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
    const loggedIn = localStorage.getItem('isLoggedIn');
    const userStr = localStorage.getItem('user');
    
    if (loggedIn === 'true' && userStr) {
      setIsAuth(true);
      try {
        const u = JSON.parse(userStr);
        const role = u.role || 'DOCTOR';
        
        // RBAC Route Protection Logic
        if (pathname.startsWith('/audit') && role !== 'ADMIN') {
          router.push('/');
        } else if ((pathname.startsWith('/queue') || pathname.startsWith('/discharge') || pathname.startsWith('/radiology')) && (role === 'ADMIN' || role === 'RESEARCHER')) {
          router.push('/');
        } else if (role === 'NURSE' && (pathname === '/' || pathname.startsWith('/audit') || pathname.startsWith('/radiology'))) {
          router.push('/queue');
        }
      } catch (e) {}
    } else {
      setIsAuth(false);
      if (pathname !== '/login') {
        router.push('/login');
      }
    }
  }, [pathname, router]);

  // Prevent flash of content during hydration
  if (!mounted) {
    return <div style={{ background: 'var(--navy-950)', minHeight: '100vh' }} />;
  }

  const isLoginPage = pathname === '/login';

  if (isLoginPage) {
    return <>{children}</>;
  }

  if (!isAuth) {
    return null; // Return null until redirect completes
  }

  return (
    <>
      <Topbar onMenuClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} />
      <div className="layout">
        <Sidebar isOpen={isMobileMenuOpen} onClose={() => setIsMobileMenuOpen(false)} />
        {children}
      </div>
      {/* Backdrop for mobile menu */}
      {isMobileMenuOpen && (
        <div 
          className="mobile-backdrop"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
      <DemoNav />
    </>
  );
}
