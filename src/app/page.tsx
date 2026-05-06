'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import * as api from '../services/api';

export default function Dashboard() {
  const [modelCard, setModelCard] = useState<any>(null);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [isAiOnline, setIsAiOnline] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const mc = await api.getModelCard();
        setModelCard(mc);
        const logs = await api.getAuditLogs();
        setAuditLogs(logs.logs || []);
        setIsAiOnline(true);
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
        setIsAiOnline(false);
      }
    }
    fetchData();
  }, []);

  return (
    <main className="main">
      {/* Page header */}
      <div className="page-head">
        <div className="page-head-left">
          <div className="crumb">
            <span>Workspace</span>
            <span className="crumb-sep">/</span>
            <span>Tổng quan</span>
          </div>
          <h1 className="page-title">
            Tổng quan ca trực
          </h1>
          <div className="page-meta">
            <span>05/05/2026</span>
            <span className="dot-sep"></span>
            <span>Ca ngày · 06:00 — 18:00</span>
            <span className="dot-sep"></span>
            <span>Khoa Nội A1 · BV 103</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '6px' }}>
          <button className="btn btn-ghost btn-sm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'12px'}}><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" /></svg>
            Làm mới
          </button>
          <button className="btn btn-ghost btn-sm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'12px'}}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" /></svg>
            Xuất báo cáo
          </button>
          <Link href="/queue">
            <button className="btn btn-accent btn-sm">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{width:'12px'}}><path d="M12 5v14M5 12h14" /></svg>
              Tạo nháp
            </button>
          </Link>
        </div>
      </div>

      {/* KPI ROW */}
      <div className="kpi-grid">
        <div className="kpi">
          <div className="kpi-top">
            <span className="kpi-label">Đã duyệt hôm nay</span>
            <span className="kpi-icon" style={{color:'var(--success)'}}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4L12 14.01l-3-3"/></svg>
            </span>
          </div>
          <div className="kpi-value">14<span className="kpi-unit">/18</span></div>
          <div className="kpi-foot">
            <span className="kpi-trend up">↑ +22%</span>
            <div className="kpi-spark">
              <span style={{height:'30%',background:'var(--success)'}}></span><span style={{height:'45%',background:'var(--success)'}}></span><span style={{height:'38%',background:'var(--success)'}}></span>
              <span style={{height:'60%',background:'var(--success)'}}></span><span style={{height:'55%',background:'var(--success)'}}></span><span style={{height:'75%',background:'var(--success)'}}></span>
              <span style={{height:'85%',background:'var(--success)'}}></span>
            </div>
          </div>
        </div>

        <div className="kpi">
          <div className="kpi-top">
            <span className="kpi-label">LATENCY P95</span>
            <span className="kpi-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </span>
          </div>
          <div className="kpi-value">8.4<span className="kpi-unit">giây</span></div>
          <div className="kpi-foot">
            <span className="kpi-trend up" style={{color:'var(--success)'}}>↓ -28%</span>
            <div className="kpi-spark">
              <span style={{height:'80%'}}></span><span style={{height:'75%'}}></span><span style={{height:'70%'}}></span>
              <span style={{height:'60%'}}></span><span style={{height:'50%'}}></span><span style={{height:'40%'}}></span>
              <span style={{height:'35%'}}></span>
            </div>
          </div>
        </div>

        <div className="kpi">
          <div className="kpi-top">
            <span className="kpi-label">Đang chờ duyệt</span>
            <span className="kpi-icon" style={{color:'var(--warning)'}}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8"/></svg>
            </span>
          </div>
          <div className="kpi-value">12<span className="kpi-unit">nháp</span></div>
          <div className="kpi-foot">
            <span className="kpi-trend" style={{color:'var(--text-tertiary)'}}>→ 3 ưu tiên</span>
            <div className="kpi-spark">
              <span style={{height:'40%',background:'var(--warning)'}}></span><span style={{height:'35%',background:'var(--warning)'}}></span><span style={{height:'50%',background:'var(--warning)'}}></span>
              <span style={{height:'45%',background:'var(--warning)'}}></span><span style={{height:'60%',background:'var(--warning)'}}></span><span style={{height:'55%',background:'var(--warning)'}}></span>
              <span style={{height:'70%',background:'var(--warning)'}}></span>
            </div>
          </div>
        </div>

        <div className="kpi" style={{borderColor:'rgba(239, 68, 68, 0.2)'}}>
          <div className="kpi-top">
            <span className="kpi-label">Cảnh báo an toàn</span>
            <span className="kpi-icon" style={{color:'var(--danger)'}}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/></svg>
            </span>
          </div>
          <div className="kpi-value">2<span className="kpi-unit">flag</span></div>
          <div className="kpi-foot">
            <span className="kpi-trend down">BN-2412</span>
            <div className="kpi-spark">
              <span style={{height:'20%',background:'var(--danger)'}}></span><span style={{height:'15%',background:'var(--danger)'}}></span><span style={{height:'30%',background:'var(--danger)'}}></span>
              <span style={{height:'25%',background:'var(--danger)'}}></span><span style={{height:'40%',background:'var(--danger)'}}></span><span style={{height:'55%',background:'var(--danger)'}}></span>
              <span style={{height:'70%',background:'var(--danger)'}}></span>
            </div>
          </div>
        </div>
      </div>

      {/* CHARTS ROW */}
      <div className="grid-2" style={{marginTop:'4px'}}>
        <div className="card">
          <div className="card-head">
            <div className="card-title"><span className="card-title-acc"></span>Hiệu năng mô hình · 8 tuần qua</div>
            <div style={{display:'flex',gap:'12px'}}>
              <div style={{display:'flex',alignItems:'center',gap:'4px',fontSize:'9px',color:'var(--text-secondary)'}}>
                <span style={{width:'8px',height:'8px',background:'var(--navy-900)',borderRadius:'2px'}}></span> F1 NER
              </div>
              <div style={{display:'flex',alignItems:'center',gap:'4px',fontSize:'9px',color:'var(--text-secondary)'}}>
                <span style={{width:'8px',height:'8px',background:'var(--gold)',borderRadius:'2px'}}></span> De-id Recall
              </div>
            </div>
          </div>
          {/* THE CHART */}
          <div style={{ padding: '24px 24px 0px', position: 'relative' }}>
            <div style={{ position: 'relative', height: '140px', marginLeft: '36px' }}>
              {/* Grid Lines */}
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
                {[1.00, 0.95, 0.90, 0.85].map((val, idx) => (
                  <div key={idx} style={{ 
                    position: 'absolute', 
                    bottom: `${((val - 0.85) / 0.15) * 100}%`, 
                    width: '100%', 
                    borderBottom: '2px dashed var(--border-strong)' 
                  }}>
                    <span style={{ 
                      position: 'absolute', 
                      left: '-36px', 
                      top: '-7px', 
                      fontSize: '10px', 
                      color: 'var(--text-tertiary)', 
                      fontFamily: 'JetBrains Mono',
                      fontWeight: 600
                    }}>
                      {val.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>

              {/* Bars */}
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', zIndex: 1 }}>
                {[
                  {ner: 94, deid: 99.2}, {ner: 95, deid: 99.4}, {ner: 96, deid: 99.6}, 
                  {ner: 96.8, deid: 99.8}, {ner: 97.5, deid: 100}, {ner: 98, deid: 100},
                  {ner: 98.8, deid: 100}, {ner: 99.2, deid: 100}
                ].map((data, i) => (
                  <div key={i} style={{ flex: 1, display: 'flex', alignItems: 'flex-end', height: '100%', padding: '0 4px' }}>
                    <div style={{
                      flex: 1, 
                      height: `${Math.max(0, ((data.ner/100 - 0.85) / 0.15) * 100)}%`,
                      background: 'var(--navy-900)'
                    }}></div>
                    <div style={{
                      flex: 1, 
                      height: `${Math.max(0, ((data.deid/100 - 0.85) / 0.15) * 100)}%`,
                      background: 'var(--gold)'
                    }}></div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* X-Axis Labels */}
            <div style={{ display: 'flex', marginLeft: '36px', marginTop: '4px' }}>
              {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                <div key={num} style={{ flex: 1, textAlign: 'center', fontSize: '10px', color: 'var(--text-tertiary)', fontFamily: 'JetBrains Mono' }}>
                  T{num}
                </div>
              ))}
            </div>
          </div>

          {/* Metrics */}
          <div className="card-body" style={{padding:'24px 24px 24px', marginTop:'4px'}}>
            <div className="metrics-row">
              <div className="metric-item">
                <span className="m-label" style={{textTransform:'uppercase'}}>F1 NER</span>
                <span className="m-val" style={{color:'var(--success)'}}>0.93</span>
                <span className="m-sub">≥ 0.90 <span style={{color:'var(--success)'}}>✓</span></span>
              </div>
              <div className="metric-item">
                <span className="m-label" style={{textTransform:'uppercase'}}>De-id Recall</span>
                <span className="m-val" style={{color:'var(--success)'}}>0.992</span>
                <span className="m-sub">≥ 0.99 <span style={{color:'var(--success)'}}>✓</span></span>
              </div>
              <div className="metric-item">
                <span className="m-label" style={{textTransform:'uppercase'}}>Acc Viết tắt</span>
                <span className="m-val" style={{color:'var(--success)'}}>0.96</span>
                <span className="m-sub">≥ 0.95 <span style={{color:'var(--success)'}}>✓</span></span>
              </div>
              <div className="metric-item">
                <span className="m-label" style={{textTransform:'uppercase'}}>Faithfulness</span>
                <span className="m-val" style={{color:'var(--success)'}}>0.91</span>
                <span className="m-sub">≥ 0.85 <span style={{color:'var(--success)'}}>✓</span></span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-head">
            <div className="card-title"><span className="card-title-acc"></span>Tỷ lệ chấp nhận</div>
            <span style={{fontSize:'10px',color:'var(--text-tertiary)'}}>N=247</span>
          </div>
          <div className="card-body" style={{display:'flex',alignItems:'center',gap:'20px',padding:'24px 18px'}}>
            <div className="donut-box">
              <svg className="donut-svg" width="100" height="100">
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="var(--navy-100)" strokeWidth="12" />
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="var(--success)" strokeWidth="12" strokeDasharray="196 251" strokeLinecap="round" />
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="var(--warning)" strokeWidth="12" strokeDasharray="35 251" strokeDashoffset="-196" strokeLinecap="round" />
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="var(--danger)" strokeWidth="12" strokeDasharray="20 251" strokeDashoffset="-231" strokeLinecap="round" />
              </svg>
              <div className="donut-text">
                <div className="donut-val">78%</div>
                <div className="donut-lbl">Chấp nhận</div>
              </div>
            </div>
            <div style={{flex:1,display:'flex',flexDirection:'column',gap:8}}>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:'11px'}}>
                <div style={{display:'flex',alignItems:'center',gap:6}}><span style={{width:8,height:8,background:'var(--success)',borderRadius:2}}></span> Chấp nhận</div>
                <span style={{fontWeight:600}}>78%</span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:'11px'}}>
                <div style={{display:'flex',alignItems:'center',gap:6}}><span style={{width:8,height:8,background:'var(--warning)',borderRadius:2}}></span> Sửa nhỏ</div>
                <span style={{fontWeight:600}}>14%</span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:'11px'}}>
                <div style={{display:'flex',alignItems:'center',gap:6}}><span style={{width:8,height:8,background:'var(--danger)',borderRadius:2}}></span> Từ chối</div>
                <span style={{fontWeight:600}}>8%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* DRAFT TABLE */}
      <div className="card">
        <div className="card-head">
          <div className="card-title"><span className="card-title-acc"></span>Hàng đợi nháp · Realtime</div>
          <div style={{display:'flex',gap:'6px'}}>
            <button className="btn btn-ghost btn-xs">Lọc danh sách</button>
            <button className="btn btn-ghost btn-xs">Ưu tiên cao</button>
          </div>
        </div>
        <div style={{overflowX:'auto'}}>
          <table className="tbl">
            <thead>
              <tr>
                <th>Mã ca</th>
                <th>Bệnh nhân</th>
                <th>Loại</th>
                <th>Khoa</th>
                <th>Trạng thái</th>
                <th>Faithfulness</th>
                <th>Đợi</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {[
                {id:'BN-2412', name:'Trần Văn M.', meta:'Nam · 67t · CCB', type:'Discharge', dept:'Tim mạch', status:'Khẩn', faith:0.71, wait:'2 phút', action:'Duyệt ngay →', pill:'pill-urgent'},
                {id:'BN-2410', name:'Phạm Thị L.', meta:'Nữ · 54t · QH', type:'Radiology', dept:'CĐHA', status:'Chờ', faith:0.94, wait:'8 phút', action:'Mở', pill:'pill-warn'},
                {id:'BN-2408', name:'Lê Quang H.', meta:'Nam · 42t · B.U', type:'Discharge', dept:'Nội A1', status:'Chờ', faith:0.91, wait:'12 phút', action:'Mở', pill:'pill-warn'},
              ].map((row, i) => (
                <tr key={i}>
                  <td className="mono" style={{fontWeight:600}}>{row.id}</td>
                  <td>
                    <div style={{fontWeight:600}}>{row.name}</div>
                    <div style={{fontSize:'9px',color:'var(--text-tertiary)',display:'flex',alignItems:'center',gap:4}}>
                      {row.meta} 
                    </div>
                  </td>
                  <td>{row.type}</td>
                  <td>{row.dept}</td>
                  <td><span className={`pill ${row.pill}`} style={{background:row.pill==='pill-urgent'?'var(--danger)':'var(--warning)',color:'#fff'}}>{row.status}</span></td>
                  <td style={{fontFamily:'JetBrains Mono',color:row.faith < 0.8 ? 'var(--danger)' : 'var(--success)',fontWeight:600}}>{row.faith}</td>
                  <td style={{color:'var(--text-tertiary)'}}>{row.wait}</td>
                  <td style={{textAlign:'right'}}>
                    <Link href={`/${row.id === 'BN-2410' ? 'radiology' : 'discharge'}/${row.id}`}>
                      <button className={`btn ${row.action.includes('→')?'btn-accent':'btn-ghost'} btn-xs`}>{row.action}</button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{padding:'8px 14px',borderTop:'1px solid var(--border)',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:'10px',color:'var(--text-tertiary)'}}>Hiển thị <b>6 {"/"} 18</b> mục · <span style={{color:'var(--danger)'}}>3 ưu tiên cao</span></div>
          <div style={{display:'flex',gap:4}}>
            <button className="btn btn-ghost btn-xs" style={{minWidth:24}}>‹</button>
            <button className="btn btn-primary btn-xs" style={{minWidth:24}}>1</button>
            <button className="btn btn-ghost btn-xs" style={{minWidth:24}}>2</button>
            <button className="btn btn-ghost btn-xs" style={{minWidth:24}}>3</button>
            <button className="btn btn-ghost btn-xs" style={{minWidth:24}}>›</button>
          </div>
        </div>
      </div>

      {/* BOTTOM GRID */}
      <div className="grid-2">
        {/* AUDIT LOG */}
        <div className="card" style={{borderTop: '2px solid var(--star-red)'}}>
          <div className="card-head">
            <div className="card-title">
              <span className="card-title-acc"></span>
              Nhật ký hệ thống · Thời gian thực
              <span style={{display:'flex',alignItems:'center',gap:'4px',marginLeft:'8px'}}>
                <span className="status-led live" style={{width:'5px',height:'5px',boxShadow:'0 0 4px var(--success)'}}></span>
                <span style={{fontSize:'9px',color:'var(--success)',fontWeight:600,letterSpacing:'.05em'}}>TRỰC TIẾP</span>
              </span>
            </div>
            <button className="btn btn-ghost btn-xs">Toàn bộ →</button>
          </div>
          <div className="card-body" style={{padding:'0 14px 14px'}}>
            <div className="log">
              {[
                {time:'14:32:18', tag:'APPROVE', msg:'BS. Nguyễn V. Hùng phê duyệt nhập discharge BN-2395 (3 sửa nhỏ)', user:'NH', cls:'t-app'},
                {time:'14:28:04', tag:'BLOCK', msg:'Hệ thống chặn output BN-2412 do hallucination ở liều thuốc', user:'SAFETY', cls:'t-blk'},
                {time:'14:21:55', tag:'REGEN', msg:'BS. Phạm M. Tuấn yêu cầu sinh lại nháp radiology BN-2389', user:'PMT', cls:'t-reg'},
                {time:'14:18:32', tag:'RAG', msg:'Truy hồi 3 phác đồ cho ca BN-2410 (Tim mạch)', user:'SYS', cls:'t-rag'},
                {time:'14:15:09', tag:'DE-ID', msg:'De-identification mask 8 PHI ở ca BN-2410', user:'SYS', cls:'t-deid'},
              ].map((log, i) => (
                <div className="log-row" key={i}>
                  <span style={{fontSize:'10px',color:'var(--text-tertiary)',fontFamily:'JetBrains Mono'}}>{log.time}</span>
                  <span className={`log-tag ${log.cls}`}>{log.tag}</span>
                  <span style={{fontSize:'11px',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{log.msg}</span>
                  <span style={{fontSize:'9px',fontWeight:700,color:'var(--text-tertiary)',textAlign:'right'}}>{log.user}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* DECISION GATES */}
        <div className="card">
          <div className="card-head">
            <div className="card-title"><span className="card-title-acc"></span>Cửa kiểm soát an toàn</div>
            <span style={{fontSize:'10px',color:'var(--text-tertiary)'}}>3/4 đạt chuẩn</span>
          </div>
          <div className="card-body" style={{padding:'0 18px 18px'}}>
            <div className="gate-list">
              {[
                {label:'Gate 1 · Dữ liệu nội bộ', val:'100%', status:'ok'},
                {label:'Gate 2 · Sidecar tin cậy', val:'100%', status:'ok'},
                {label:'Gate 3 · Silent Mode', val:'82%', status:'warn'},
                {label:'Gate 4 · Assisted Mode', val:'-', status:'off'},
              ].map((gate, i) => (
                <div key={i} className="gate-item">
                  <div className="gate-top">
                    <div className="gate-info">
                      <span style={{color:gate.status==='ok'?'var(--success)':gate.status==='warn'?'var(--danger)':'var(--text-tertiary)'}}>
                        {gate.status==='ok'?'✓':gate.status==='warn'?'●':'○'}
                      </span>
                      {gate.label}
                    </div>
                    <span style={{fontSize:'10px',fontWeight:700}}>{gate.val}</span>
                  </div>
                  <div className="gate-p-bg">
                    <div className="gate-p-fg" style={{width:gate.val==='-'?'0%':gate.val, background:gate.status==='warn'?'var(--danger)':'var(--success)'}}></div>
                  </div>
                </div>
              ))}
            </div>
            <div style={{marginTop:'8px',padding:'10px',background:'var(--navy-50)',borderRadius:4,fontSize:'10px',display:'flex',alignItems:'center',gap:8}}>
               <span style={{color:'var(--danger)'}}>●</span> <b>Hiện tại:</b> Silent mode đang chặn các ca có độ tin cậy &lt; 0.85
            </div>
          </div>
        </div>
      </div>

    </main>
  );
}
