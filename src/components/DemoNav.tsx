'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function DemoNav() {
  const pathname = usePathname();
  const [lastRadiologyId, setLastRadiologyId] = useState('BN-2410');

  useEffect(() => {
    const saved = localStorage.getItem('last_radiology_id');
    if (saved) {
      setLastRadiologyId(saved);
    }
  }, []);

  useEffect(() => {
    if (pathname && pathname.startsWith('/radiology/')) {
      const parts = pathname.split('/');
      const id = parts[parts.length - 1];
      if (id) {
        setLastRadiologyId(id);
        localStorage.setItem('last_radiology_id', id);
      }
    }
  }, [pathname]);

  const tabs = [
    { label: 'TỔNG QUAN', href: '/' },
    { label: 'HÀNG ĐỢI', href: '/queue' },
    { label: 'CA CĐHA', href: `/radiology/${lastRadiologyId}` },
  ];

  return (
    <div className="floating-demo">
      <span className="demo-tag">DEMO</span>
      {tabs.map((tab) => {
        let isActive = false;
        if (tab.label === 'TỔNG QUAN') {
          isActive = pathname === '/';
        } else if (tab.label === 'HÀNG ĐỢI') {
          isActive = pathname === '/queue' || pathname.startsWith('/discharge');
        } else if (tab.label === 'CA CĐHA') {
          isActive = pathname.startsWith('/radiology');
        }
        
        return (
          <Link 
            key={tab.label} 
            href={tab.href}
            className={`demo-btn ${isActive ? 'active' : ''}`}
          >
            {tab.label}
          </Link>
        );
      })}
    </div>
  );
}
