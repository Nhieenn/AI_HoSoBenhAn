'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function DemoNav() {
  const pathname = usePathname();

  const tabs = [
    { label: 'TỔNG QUAN', href: '/' },
    { label: 'HÀNG ĐỢI', href: '/queue' },
    { label: 'CĐHA', href: '/radiology/BN-2410' },
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
        } else if (tab.label === 'CĐHA') {
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
