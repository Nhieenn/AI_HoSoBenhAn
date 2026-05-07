'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const DEMO_ACCOUNTS = [
  { id: 'doctor', role: 'DOCTOR', name: 'Bác sĩ Điều trị', username: 'bacsihung', password: 'password123', avatar: 'NH', dept: 'Khoa Nội · A1' },
  { id: 'nurse', role: 'NURSE', name: 'Điều dưỡng/HC', username: 'dieuduong', password: 'password123', avatar: 'HC', dept: 'Khoa Khám bệnh' },
  { id: 'admin', role: 'ADMIN', name: 'Quản trị (Admin)', username: 'quantri', password: 'password123', avatar: 'QT', dept: 'Phòng CNTT' },
  { id: 'researcher', role: 'RESEARCHER', name: 'Nhà Nghiên cứu', username: 'nghiencuu', password: 'password123', avatar: 'NC', dept: 'Viện NCKH' }
];

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    setTimeout(() => {
      const account = DEMO_ACCOUNTS.find(a => a.username === username && a.password === password);
      
      if (account) {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('user', JSON.stringify({
          id: account.avatar,
          name: account.id === 'doctor' ? 'BS. Nguyễn V. Hùng' : account.name,
          dept: account.dept,
          role: account.role
        }));
        router.push('/');
      } else {
        setError('Tên đăng nhập hoặc mật khẩu không chính xác.');
        setLoading(false);
      }
    }, 600);
  };

  const fillDemo = (user: string, pass: string) => {
    setUsername(user);
    setPassword(pass);
    setError('');
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-head" style={{ paddingBottom: '16px' }}>
          <div className="login-logo">
            <svg viewBox="0 0 24 24" fill="#d4332e" stroke="#d4a857" strokeWidth="0.5" style={{ width: '28px', height: '28px' }}>
              <path d="M12 2 L14.4 8.5 L21.5 8.5 L15.8 13 L18.2 19.5 L12 15.5 L5.8 19.5 L8.2 13 L2.5 8.5 L9.6 8.5 Z"/>
            </svg>
          </div>
          <h1 className="login-title">ViMedAI</h1>
          <div className="login-sub">HỆ THỐNG AI TẠO SINH Y KHOA TIẾNG VIỆT</div>
        </div>

        <div className="login-body" style={{ paddingTop: '16px' }}>
          {/* DEMO ACCOUNTS QUICK SELECTOR */}
          <div style={{ marginBottom: '24px' }}>
            <div style={{ fontSize: '10px', color: 'var(--navy-300)', textTransform: 'uppercase', marginBottom: '8px', textAlign: 'center', fontWeight: 600 }}>
              Đăng nhập nhanh dành cho Demo
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
              {DEMO_ACCOUNTS.map((acc) => (
                <button 
                  key={acc.id}
                  type="button"
                  onClick={() => fillDemo(acc.username, acc.password)}
                  style={{
                    background: username === acc.username ? 'var(--gold)' : 'var(--navy-900)',
                    border: `1px solid ${username === acc.username ? 'var(--gold)' : 'var(--navy-700)'}`,
                    borderRadius: 'var(--r-sm)',
                    padding: '8px',
                    color: username === acc.username ? 'var(--navy-900)' : '#fff',
                    fontSize: '11px',
                    fontWeight: 600,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    textAlign: 'left',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}
                >
                  <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: 'var(--navy-800)', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '9px', border: '1px solid var(--navy-600)' }}>
                    {acc.avatar}
                  </div>
                  {acc.name}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="login-error">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '16px', height: '16px', flexShrink: 0 }}>
                <circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>
              </svg>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label className="form-label">Tên đăng nhập</label>
              <input 
                type="text" 
                className="form-input" 
                placeholder="Ví dụ: bacsihung"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
              />
            </div>

            <div className="form-group" style={{ marginBottom: '32px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                <label className="form-label">Mật khẩu</label>
                <span style={{ fontSize: '10px', color: 'var(--navy-400)', cursor: 'pointer' }}>Quên mật khẩu?</span>
              </div>
              <input 
                type="password" 
                className="form-input" 
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? (
                <>
                  <svg className="animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ width: '16px', height: '16px', animation: 'spin 1s linear infinite' }}>
                    <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
                    <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeOpacity="0.2" />
                    <path d="M21 12a9 9 0 01-9 9" strokeLinecap="round" />
                  </svg>
                  ĐANG XÁC THỰC...
                </>
              ) : (
                'ĐĂNG NHẬP VÀO HỆ THỐNG'
              )}
            </button>
          </form>

          <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '11px', color: 'var(--navy-400)' }}>
            Phiên bản thử nghiệm (Pilot) • Chỉ dùng cho nội bộ Bệnh viện
          </div>
        </div>
      </div>
    </div>
  );
}
