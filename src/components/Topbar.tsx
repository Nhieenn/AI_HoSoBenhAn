'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

interface TopbarProps {
  onMenuClick?: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [user, setUser] = useState({
    id: 'NH',
    name: 'BS. Nguyễn V. Hùng',
    dept: 'Khoa Nội · A1',
    role: 'DOCTOR'
  });

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        const u = JSON.parse(userStr);
        setUser(u);
      } catch (e) {}
    }
    
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const showOverview = user.role === 'ADMIN' || user.role === 'DOCTOR' || user.role === 'RESEARCHER';
  const showQueue = user.role === 'DOCTOR' || user.role === 'NURSE';
  const showRecords = user.role === 'DOCTOR' || user.role === 'NURSE' || user.role === 'RESEARCHER';
  const showKnowledge = user.role === 'ADMIN' || user.role === 'DOCTOR' || user.role === 'RESEARCHER';
  const showSystem = user.role === 'ADMIN';

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('user');
    router.push('/login');
  };

  return (
    <header className="topbar">
      <div className="brand-block">
        <button className="mobile-menu-btn" onClick={onMenuClick}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
        <div className="brand-emblem">
          <svg viewBox="0 0 24 24" fill="#d4332e" stroke="#d4a857" strokeWidth="0.5">
            <path d="M12 2 L14.4 8.5 L21.5 8.5 L15.8 13 L18.2 19.5 L12 15.5 L5.8 19.5 L8.2 13 L2.5 8.5 L9.6 8.5 Z"/>
          </svg>
        </div>
        <div className="brand-text">
          <div className="brand-name">ViMedAI <span style={{fontSize:'8px',background:'var(--gold)',color:'var(--navy-900)',padding:'1px 3px',borderRadius:'2px',marginLeft:'4px'}}>v1.0</span></div>
          <div className="brand-sub">HỌC VIỆN QUÂN Y · BV103</div>
        </div>
      </div>

      <nav className="top-nav">
        {showOverview && (
          <Link href="/" className={`top-nav-link ${pathname === '/' ? 'active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
            Tổng quan
          </Link>
        )}
        {showQueue && (
          <Link href="/queue" className={`top-nav-link ${pathname.startsWith('/queue') || pathname.startsWith('/discharge') || pathname.startsWith('/radiology') ? 'active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>
            Hàng đợi
            <span className="badge">12</span>
          </Link>
        )}
        {showRecords && (
          <a className="top-nav-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Bệnh nhân
          </a>
        )}
        {showKnowledge && (
          <a className="top-nav-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            Tri thức
          </a>
        )}
        {showSystem && (
          <Link href="/audit" className={`top-nav-link ${pathname === '/audit' ? 'active' : ''}`}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Nhật ký
          </Link>
        )}
      </nav>

      <div className="top-right">
        <div className="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>
          <input placeholder="Tìm BN, mã ca, viết tắt..." />
          <span style={{ fontSize: '9px', color: 'var(--navy-300)', background: 'var(--navy-900)', padding: '1px 4px', borderRadius: '3px', marginLeft: 'auto' }}>⌘K</span>
        </div>
        
        <div className="top-status">
          <span className="status-led live"></span>
          <div className="status-text">
            <span style={{ fontSize: '9px', color: 'var(--navy-300)', textTransform: 'uppercase' }}>Chế độ</span>
            <span style={{ fontSize: '11px', color: '#fff', fontWeight: 600 }}>TRỢ LÝ AI</span>
          </div>
          <div className="status-text" style={{marginLeft:'12px', borderLeft:'1px solid var(--navy-800)', paddingLeft:'12px'}}>
            <span style={{ fontSize: '9px', color: 'var(--navy-300)', textTransform: 'uppercase' }}>Độ trễ P95</span>
            <span style={{ fontSize: '11px', color: '#fff', fontWeight: 600 }}>8.4s</span>
          </div>
        </div>

        <div className="top-user" style={{ position: 'relative', cursor: 'pointer' }} onClick={() => setShowDropdown(!showDropdown)} ref={dropdownRef}>
          <div className="user-av">{user.id}</div>
          <div className="user-info">
            <div style={{ fontSize: '11px', fontWeight: 600, color: '#fff' }}>{user.name}</div>
            <div style={{ fontSize: '10px', color: 'var(--navy-300)' }}>{user.dept}</div>
          </div>
          
          {showDropdown && (
            <div style={{
              position: 'absolute',
              top: '100%',
              right: '10px',
              marginTop: '8px',
              background: 'var(--navy-900)',
              border: '1px solid var(--navy-700)',
              borderRadius: 'var(--r-sm)',
              boxShadow: 'var(--shadow-md)',
              minWidth: '150px',
              zIndex: 100
            }}>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  handleLogout();
                }}
                style={{
                  width: '100%',
                  padding: '10px 14px',
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--danger)',
                  fontSize: '12px',
                  fontWeight: 600,
                  textAlign: 'left',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  borderBottom: '1px solid transparent'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'transparent';
                }}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '14px', height: '14px' }}>
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
                </svg>
                Đăng xuất
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
