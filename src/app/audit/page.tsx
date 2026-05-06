'use client';

import React from 'react';

const auditLogs = [
  { time: '09:20:15', user: 'BS. Hùng', action: 'ENRICH_CONTEXT', target: 'BN-2408', detail: 'Bổ sung triệu chứng: Đau lan lên vai trái' },
  { time: '09:18:42', user: 'System AI', action: 'GENERATE_DRAFT', target: 'BN-2408', detail: 'Sinh nháp chẩn đoán NMCT cấp' },
  { time: '08:45:10', user: 'BS. Tuấn', action: 'APPROVE_REPORT', target: 'BN-2410', detail: 'Phê duyệt báo cáo CT ngực' },
  { time: '08:30:05', user: 'System AI', action: 'PHI_MASKING', target: 'BN-2410', detail: 'Ẩn danh 3 thực thể dữ liệu nhạy cảm' },
];

export default function AuditPage() {
  return (
    <main className="main">
      <div className="page-head">
        <div className="page-head-left">
          <div className="crumb">
            <span>Hệ thống</span>
            <span className="crumb-sep">/</span>
            <span>Audit log</span>
          </div>
          <h1 className="page-title">Nhật ký Hệ thống (Audit Log)</h1>
        </div>
        <button className="btn btn-ghost btn-sm">Xuất báo cáo CSV</button>
      </div>

      <div className="card" style={{padding:0}}>
        <table style={{width:'100%', borderCollapse:'collapse', fontSize:'12px'}}>
          <thead style={{background:'var(--navy-50)', borderBottom:'1px solid var(--border)'}}>
            <tr>
              <th style={{padding:'12px 20px', textAlign:'left'}}>THỜI GIAN</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>NGƯỜI DÙNG</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>HÀNH ĐỘNG</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>ĐỐI TƯỢNG</th>
              <th style={{padding:'12px 20px', textAlign:'left'}}>CHI TIẾT</th>
            </tr>
          </thead>
          <tbody>
            {auditLogs.map((log, i) => (
              <tr key={i} style={{borderBottom:'1px solid var(--border)'}}>
                <td style={{padding:'14px 20px', fontFamily:'mono', color:'var(--text-tertiary)'}}>{log.time}</td>
                <td style={{padding:'14px 20px', fontWeight:700}}>{log.user}</td>
                <td style={{padding:'14px 20px'}}>
                   <span className="badge-xs" style={{
                     background: log.action.includes('APPROVE') ? 'rgba(16,185,129,0.1)' : 
                                 log.action.includes('AI') ? 'rgba(59,130,246,0.1)' : 'var(--navy-100)',
                     color: log.action.includes('APPROVE') ? 'var(--success)' :
                            log.action.includes('AI') ? '#3b82f6' : 'var(--navy-900)'
                   }}>
                     {log.action}
                   </span>
                </td>
                <td style={{padding:'14px 20px', fontWeight:600}}>{log.target}</td>
                <td style={{padding:'14px 20px', color:'var(--text-secondary)'}}>{log.detail}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
