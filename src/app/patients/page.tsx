'use client';

import React from 'react';
import Link from 'next/link';

const patients = [
  { id: 'P-1002', name: 'Nguyễn Văn A', age: 45, gender: 'Nam', lastVisit: '02/05/2026', diagnosis: 'Tăng huyết áp', tag: 'PCI' },
  { id: 'P-1003', name: 'Trần Thị B', age: 38, gender: 'Nữ', lastVisit: '28/04/2026', diagnosis: 'Đái tháo đường', tag: 'BHYT' },
  { id: 'P-1004', name: 'Lê Văn C', age: 62, gender: 'Nam', lastVisit: '15/04/2026', diagnosis: 'NMCT cũ', tag: 'QN' },
  { id: 'P-1005', name: 'Hoàng Thị D', age: 29, gender: 'Nữ', lastVisit: '10/04/2026', diagnosis: 'Rối loạn nhịp', tag: 'PCI' },
];

export default function PatientList() {
  return (
    <main className="main">
      <div className="page-head">
        <div className="page-head-left">
          <div className="crumb">
            <span>Hồ sơ</span>
            <span className="crumb-sep">/</span>
            <span>Danh sách bệnh nhân</span>
          </div>
          <h1 className="page-title">Quản lý Hồ sơ Bệnh nhân</h1>
        </div>
        <div style={{display:'flex', gap:8}}>
           <div style={{position:'relative'}}>
             <input type="text" placeholder="Tìm tên, mã BN..." style={{padding:'8px 12px 8px 32px', borderRadius:6, border:'1px solid var(--border)', fontSize:'13px', width:240}} />
             <svg viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" strokeWidth="2" style={{width:14, position:'absolute', left:10, top:10}}><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
           </div>
           <button className="btn btn-accent btn-sm">Thêm hồ sơ</button>
        </div>
      </div>

      <div className="card" style={{padding:0}}>
        <table style={{width:'100%', borderCollapse:'collapse', fontSize:'13px'}}>
          <thead style={{background:'var(--navy-50)', borderBottom:'1px solid var(--border)'}}>
            <tr>
              <th style={{padding:'12px 20px', textAlign:'left'}}>MÃ BN</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>HỌ VÀ TÊN</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>TUỔI / GIỚI</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>CHẨN ĐOÁN GẦN NHẤT</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>PHÂN LOẠI</th>
              <th style={{padding:'12px 20px', textAlign:'right'}}>LẦN CUỐI</th>
              <th style={{padding:'12px 20px', textAlign:'center'}}>THAO TÁC</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p, i) => (
              <tr key={i} style={{borderBottom:'1px solid var(--border)'}}>
                <td style={{padding:'16px 20px', fontWeight:700}}>{p.id}</td>
                <td style={{padding:'16px 20px', fontWeight:600}}>{p.name}</td>
                <td style={{padding:'16px 20px'}}>{p.age} · {p.gender}</td>
                <td style={{padding:'16px 20px'}}>{p.diagnosis}</td>
                <td style={{padding:'16px 20px'}}><span className="badge-xs">{p.tag}</span></td>
                <td style={{padding:'16px 20px', textAlign:'right'}}>{p.lastVisit}</td>
                <td style={{padding:'16px 20px', textAlign:'center'}}>
                   <button className="btn btn-xs btn-ghost">Xem chi tiết</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
