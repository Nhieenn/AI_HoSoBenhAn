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

  useEffect(() => {
    setMounted(true);
    const loggedIn = localStorage.getItem('isLoggedIn');
    if (loggedIn === 'true') {
      setIsAuth(true);
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
      <Topbar />
      <div className="layout">
        <Sidebar />
        {children}
      </div>
      <DemoNav />
    </>
  );
}
