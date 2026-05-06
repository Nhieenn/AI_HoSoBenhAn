'use client';

import React from 'react';

const protocols = [
  { title: 'Phác đồ Xử trí Nhồi máu cơ tim cấp (BYT 2023)', category: 'Tim mạch', version: 'v3.2', updated: '15/01/2026' },
  { title: 'Hướng dẫn chẩn đoán và điều trị THA', category: 'Nội khoa', version: 'v2.1', updated: '10/12/2025' },
  { title: 'Quy trình kỹ thuật nội soi can thiệp', category: 'Ngoại khoa', version: 'v1.5', updated: '05/03/2026' },
  { title: 'Danh mục thuốc y học cổ truyền quân đội', category: 'Dược lý', version: 'v4.0', updated: '20/02/2026' },
];

export default function KnowledgeBase() {
  return (
    <main className="main">
      <div className="page-head">
        <div className="page-head-left">
          <div className="crumb">
            <span>Tri thức</span>
            <span className="crumb-sep">/</span>
            <span>Phác đồ điều trị</span>
          </div>
          <h1 className="page-title">Thư viện Phác đồ Lâm sàng</h1>
        </div>
      </div>

      <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fill, minmax(300px, 1fr))', gap:20}}>
        {protocols.map((p, i) => (
          <div key={i} className="card" style={{padding:20, display:'flex', flexDirection:'column', gap:12, cursor:'pointer', border:'1px solid transparent'}} onMouseEnter={(e) => e.currentTarget.style.borderColor='var(--accent)'} onMouseLeave={(e) => e.currentTarget.style.borderColor='transparent'}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start'}}>
               <span className="badge-xs" style={{background:'var(--navy-100)', color:'var(--navy-900)'}}>{p.category}</span>
               <span style={{fontSize:'10px', color:'var(--text-tertiary)', fontWeight:600}}>{p.version}</span>
            </div>
            <h3 style={{fontSize:'15px', fontWeight:700, lineHeight:1.4, flex:1}}>{p.title}</h3>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginTop:10, paddingTop:10, borderTop:'1px solid var(--border)'}}>
               <span style={{fontSize:'11px', color:'var(--text-tertiary)'}}>Cập nhật: {p.updated}</span>
               <button className="btn btn-xs btn-ghost" style={{padding:'2px 8px'}}>Xem file PDF</button>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
