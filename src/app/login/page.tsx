'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

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

    // Artificial account logic
    setTimeout(() => {
      if (username === 'bacsihung' && password === 'password123') {
        localStorage.setItem('isLoggedIn', 'true');
        // Add artificial user info
        localStorage.setItem('user', JSON.stringify({
          id: 'NH',
          name: 'BS. Nguyễn V. Hùng',
          dept: 'Khoa Nội · A1',
          role: 'doctor'
        }));
        router.push('/');
      } else {
        setError('Tên đăng nhập hoặc mật khẩu không chính xác.');
        setLoading(false);
      }
    }, 600); // Simulate network delay
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-head">
          <div className="login-logo">
            <svg viewBox="0 0 24 24" fill="#d4332e" stroke="#d4a857" strokeWidth="0.5" style={{ width: '28px', height: '28px' }}>
              <path d="M12 2 L14.4 8.5 L21.5 8.5 L15.8 13 L18.2 19.5 L12 15.5 L5.8 19.5 L8.2 13 L2.5 8.5 L9.6 8.5 Z"/>
            </svg>
          </div>
          <h1 className="login-title">ViMedAI</h1>
          <div className="login-sub">HỆ THỐNG AI TẠO SINH Y KHOA TIẾNG VIỆT</div>
        </div>

        <div className="login-body">
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
