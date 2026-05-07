'use client';

import React from 'react';
import Link from 'next/link';

const queueData = [
  { id: 'BN-2408', name: 'Lê Quang H.', rank: 'Đại úy', unit: 'Đoàn 367', dept: 'Nội A1', status: 'READY', time: '10 phút trước' },
  { id: 'BN-2410', name: 'Phạm Thị L.', rank: 'Quân nhân', unit: 'Khoa CĐHA', dept: 'CĐHA', status: 'PROCESSING', time: '2 phút trước' },
  { id: 'BN-2411', name: 'Nguyễn Văn M.', rank: 'Lao động HĐ', unit: 'BV 103', dept: 'Ngoại B1', status: 'WAITING', time: 'Vừa xong' },
  { id: 'BN-2395', name: 'Trần Thị K.', rank: 'Đại tá', unit: 'HVQY', dept: 'Nội A1', status: 'COMPLETED', time: '1 giờ trước' },
];

export default function InputQueue() {
  return (
    <main className="main">
      <div className="page-head">
        <div className="page-head-left">
          <div className="crumb">
            <span>Workspace</span>
            <span className="crumb-sep">/</span>
            <span>Hàng đợi nhập</span>
          </div>
          <h1 className="page-title">Hàng đợi xử lý hồ sơ</h1>
          <div style={{fontSize:'12px', color:'var(--text-tertiary)'}}>Dữ liệu được đồng bộ thời gian thực từ hệ thống HIS</div>
        </div>
        <div style={{display:'flex', gap:8, flexWrap:'wrap', marginTop:'10px'}}>
           <button className="btn btn-ghost btn-sm">Lọc danh sách</button>
           <button className="btn btn-accent btn-sm">Đồng bộ HIS</button>
        </div>
      </div>

      <div className="card" style={{padding:0, overflow:'hidden'}}>
        <table style={{width:'100%', borderCollapse:'collapse', fontSize:'13px'}}>
          <thead style={{background:'var(--navy-50)', borderBottom:'1px solid var(--border)'}}>
            <tr>
              <th style={{padding:'12px 20px', textAlign:'left', color:'var(--text-tertiary)', fontWeight:600}}>MÃ BỆNH NHÂN</th>
              <th style={{padding:'12px 20px', textAlign:'left', color:'var(--text-tertiary)', fontWeight:600}}>HỌ VÀ TÊN</th>
              <th style={{padding:'12px 20px', textAlign:'left', color:'var(--text-tertiary)', fontWeight:600}}>ĐỐI TƯỢNG</th>
              <th style={{padding:'12px 20px', textAlign:'left', color:'var(--text-tertiary)', fontWeight:600}}>KHOA ĐIỀU TRỊ</th>
              <th style={{padding:'12px 20px', textAlign:'left', color:'var(--text-tertiary)', fontWeight:600}}>TRẠNG THÁI AI</th>
              <th style={{padding:'12px 20px', textAlign:'right', color:'var(--text-tertiary)', fontWeight:600}}>THỜI GIAN</th>
              <th style={{padding:'12px 20px', textAlign:'center', color:'var(--text-tertiary)', fontWeight:600}}>THAO TÁC</th>
            </tr>
          </thead>
          <tbody>
            {queueData.map((item, i) => (
              <tr key={i} style={{borderBottom:'1px solid var(--border)', background: i % 2 === 0 ? 'transparent' : 'rgba(0,0,0,0.01)'}}>
                <td style={{padding:'16px 20px', fontWeight:700, fontFamily:'mono', color:'var(--navy-900)'}}>{item.id}</td>
                <td style={{padding:'16px 20px', fontWeight:600}}>{item.name}</td>
                <td style={{padding:'16px 20px'}}><span className="badge-xs" style={{background:'var(--navy-100)', color:'var(--navy-900)'}}>{item.rank}</span></td>
                <td style={{padding:'16px 20px'}}>{item.dept}</td>
                <td style={{padding:'16px 20px'}}>
                  <div style={{display:'flex', alignItems:'center', gap:6}}>
                    <div className={`status-led ${item.status.toLowerCase()}`} style={{width:8, height:8}}></div>
                    <span style={{
                      fontSize:'11px', 
                      fontWeight:700,
                      color: item.status === 'READY' ? 'var(--success)' : 
                             item.status === 'PROCESSING' ? 'var(--warning)' : 
                             item.status === 'COMPLETED' ? 'var(--navy-400)' : 'var(--text-tertiary)'
                    }}>
                      {item.status}
                    </span>
                  </div>
                </td>
                <td style={{padding:'16px 20px', textAlign:'right', color:'var(--text-tertiary)'}}>{item.time}</td>
                <td style={{padding:'16px 20px', textAlign:'center'}}>
                   <Link href={`/${item.dept === 'CĐHA' ? 'radiology' : 'discharge'}/${item.id}`} className="btn btn-xs btn-accent" style={{padding:'4px 12px', borderRadius:4, textDecoration:'none', display:'inline-block'}}>
                     Xử lý
                   </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
