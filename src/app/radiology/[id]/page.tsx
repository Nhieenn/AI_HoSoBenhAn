'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import * as api from '@/services/api';

export default function RadiologyEditor() {
  const { id } = useParams();
  const [content, setContent] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
  
  const [patientData, setPatientData] = useState({
    name: "Phạm Thị L.",
    age: "54",
    gender: "Nữ",
    object: "QUÂN NHÂN",
    modality: "CT Thorax W/O",
    date: "30/04/2026",
    slices: "256 slices"
  });

  useEffect(() => {
    if (id === "BN-2410") {
      setPatientData({
        name: "Phạm Thị L.",
        age: "54",
        gender: "Nữ",
        object: "QUÂN NHÂN",
        modality: "CT Thorax W/O",
        date: "30/04/2026",
        slices: "256 slices"
      });
    }
  }, [id]);

  const [aiFindings] = useState({
    diameter: "14.2 x 13.1 mm",
    density: "32 HU",
    volume: "1.28 cm³",
    location: "RUL · S1",
    lungRads: "4A",
    confidence: "0.91"
  });

  return (
    <main className="main">
      {/* HEADER: Logic-driven Header */}
      <div className="page-head" style={{paddingBottom:20, borderBottom:'1px solid var(--border)', marginBottom:20}}>
        <div className="page-head-left">
          <div className="crumb" style={{fontSize:'10px', color:'var(--text-tertiary)'}}>
            <Link href="/" style={{color:'inherit', textDecoration:'none'}}>Workspace</Link>
            <span className="crumb-sep">/</span>
            <Link href="/queue" style={{color:'inherit', textDecoration:'none'}}>Hàng đợi nhập</Link>
            <span className="crumb-sep">/</span>
            <span style={{color:'var(--text-secondary)'}}>{id} · CT Scan Summary</span>
          </div>
          <h1 className="page-title" style={{fontSize:'24px', marginTop:4, marginBottom:6}}>Báo cáo CĐHA · <span className="mono">{id}</span></h1>
          <div className="page-meta" style={{display:'flex', alignItems:'center', gap:8, fontSize:'11px', flexWrap:'wrap'}}>
            <span style={{background:'#000', color:'#facc15', padding:'2px 6px', borderRadius:2, fontWeight:800, fontSize:'9px'}}>{patientData.object}</span>
            <span style={{color:'var(--text-secondary)', fontWeight:500}}>{patientData.name}</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.gender} · {patientData.age}t</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.modality}</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.date}</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems:'center', flexWrap:'wrap', marginTop:'12px' }}>
          <button className="btn btn-ghost btn-sm" style={{borderColor:'var(--border)'}}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:14, marginRight:4}}><path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
            Sinh lại
          </button>
          <button className="btn btn-ghost btn-sm" style={{borderColor:'var(--danger)', color:'var(--danger)'}} onClick={() => {
            if(confirm("Bạn có chắc chắn muốn từ chối bản ghi này?")) {
              window.location.href = "/queue";
            }
          }}>
            Từ chối
          </button>
          <button className="btn btn-success btn-sm" style={{background:'#10b981', color:'#fff'}} onClick={() => {
            alert("Đã phê duyệt và đồng bộ dữ liệu PACS thành công!");
            window.location.href = "/queue";
          }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" style={{width:14, marginRight:4}}><path d="M20 6L9 17l-5-5"/></svg>
            Phê duyệt & Lưu PACS
          </button>
        </div>
      </div>

      <div className="editor">
        {/* LEFT PANEL: DICOM & AI DETECTION */}
        <aside className="panel">
          <div className="panel-h"><div className="lbl">DICOM VIEWER</div></div>
          <div className="panel-b" style={{padding:12}}>
            {/* Simulated Viewer */}
            <div style={{width:'100%', aspectRatio:'1/1', background:'#000', borderRadius:8, position:'relative', marginBottom:16, display:'flex', alignItems:'center', justifyContent:'center', border:'1px solid var(--navy-800)'}}>
               <div style={{color:'rgba(255,255,255,0.2)', fontSize:'10px'}}>IMAGE_PREVIEW_MODALITY_CT</div>
               <div style={{position:'absolute', top:10, left:10, fontSize:'9px', color:'var(--gold)', fontFamily:'mono'}}>SE: 5<br/>IMG: 18/256</div>
               <div style={{position:'absolute', bottom:10, right:10, fontSize:'9px', color:'var(--gold)', textAlign:'right'}}>GE Optima 660<br/>Slice: 2.5mm</div>
               {/* AI Target Circle */}
               <div style={{width:40, height:40, border:'1px solid var(--danger)', borderRadius:'50%', position:'absolute', top:'40%', left:'45%'}}>
                 <span style={{position:'absolute', top:-12, left:12, fontSize:'8px', color:'var(--danger)', fontWeight:800}}>AI</span>
               </div>
            </div>

            <div className="fact-grid" style={{gap:10}}>
              <div style={{fontSize:'10px', fontWeight:700, color:'var(--text-tertiary)', textTransform:'uppercase', borderBottom:'1px solid var(--border)', paddingBottom:6, marginBottom:4}}>AI FINDINGS · LUNG NODULE</div>
              
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0'}}>
                <span style={{color:'var(--text-tertiary)'}}>DIAMETER</span>
                <span style={{fontWeight:700, fontFamily:'JetBrains Mono'}}>{aiFindings.diameter}</span>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0'}}>
                <span style={{color:'var(--text-tertiary)'}}>DENSITY</span>
                <span style={{fontWeight:700, fontFamily:'JetBrains Mono'}}>{aiFindings.density}</span>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0'}}>
                <span style={{color:'var(--text-tertiary)'}}>VOLUME</span>
                <span style={{fontWeight:700, fontFamily:'JetBrains Mono'}}>{aiFindings.volume}</span>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0'}}>
                <span style={{color:'var(--text-tertiary)'}}>LOCATION</span>
                <span style={{fontWeight:700}}>{aiFindings.location}</span>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0'}}>
                <span style={{color:'var(--text-tertiary)'}}>LUNG-RADS</span>
                <span style={{fontWeight:800, color:'var(--star-red)'}}>{aiFindings.lungRads}</span>
              </div>
              <div style={{display:'flex', justifyContent:'space-between', fontSize:'11px', padding:'4px 0', marginTop:4, borderTop:'1px solid var(--navy-50)', paddingTop:8}}>
                <span style={{color:'var(--text-tertiary)'}}>AI CONFIDENCE</span>
                <span style={{fontWeight:700, color:'var(--success)'}}>{aiFindings.confidence}</span>
              </div>
            </div>
          </div>
        </aside>

        {/* CENTER PANEL: STRUCTURED REPORT */}
        <main className="panel">
          <div className="panel-h" style={{padding:0, background:'#fff'}}>
             <div style={{display:'flex', borderBottom:'1px solid var(--border)', width:'100%', overflowX:'auto', whiteSpace:'nowrap'}}>
               <div style={{padding:'10px 20px', fontSize:'11px', fontWeight:700, borderBottom:'2px solid var(--star-red)', color:'var(--navy-900)'}}>BÁO CÁO CẤU TRÚC</div>
               <div style={{padding:'10px 20px', fontSize:'11px', fontWeight:500, color:'var(--text-tertiary)'}}>SO SÁNH PHIM CŨ</div>
               <div style={{padding:'10px 20px', fontSize:'11px', fontWeight:500, color:'var(--text-tertiary)'}}>AUDIT</div>
             </div>
          </div>
          <div className="canvas" style={{padding:20}}>
             <div className="paper" style={{padding:40, minHeight:'unset'}}>
                <div style={{textAlign:'center', borderBottom:'2px solid #000', paddingBottom:20, marginBottom:30}}>
                   <div style={{fontSize:'11px', fontWeight:700, marginBottom:10}}>BỘ QUỐC PHÒNG · HỌC VIỆN QUÂN Y · KHOA CĐHA</div>
                   <div style={{fontSize:'22px', fontWeight:800, textTransform:'uppercase'}}>Báo cáo Chụp Cắt Lớp Vi Tính</div>
                   <div style={{fontSize:'12px', color:'var(--text-tertiary)', marginTop:4}}>CT NGỰC KHÔNG TIÊM THUỐC · RAD-CT-001/2026</div>
                </div>

                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, fontSize:'12px', background:'var(--navy-50)', padding:15, borderRadius:8, marginBottom:25}}>
                   <div>Mã ca: <b>{id}</b></div>
                   <div style={{textAlign:'right'}}>Ngày chụp: <b>{patientData.date} 14:22</b></div>
                   <div>BS chỉ định: <b>BS. Trần Văn N.</b></div>
                   <div style={{textAlign:'right'}}>Kỹ thuật: <b>120kVp · 250mAs · 2.5mm</b></div>
                </div>

                <div className="sec">
                   <h3>I. CHỈ ĐỊNH</h3>
                   <p style={{fontSize:'13px', lineHeight:1.6}}>Bệnh nhân nữ 54 tuổi, ho khan kéo dài 3 tuần, đau ngực phải nhẹ. Khám lâm sàng nghi ngờ tổn thương khu trú phổi phải. Chỉ định CT ngực để đánh giá tổn thương.</p>
                </div>

                <div className="sec">
                   <h3>II. KỸ THUẬT</h3>
                   <p style={{fontSize:'13px', lineHeight:1.6}}>Chụp cắt lớp vi tính đa dãy lồng ngực không tiêm thuốc cản quang. Máy GE Optima CT 660. Độ dày lớp cắt 2.5mm, tái tạo độ dày 1.25mm theo ba mặt phẳng.</p>
                </div>

                <div className="sec">
                   <h3>III. FINDINGS</h3>
                   <ul style={{fontSize:'13px', lineHeight:1.8, paddingLeft:20}}>
                     <li><b>Phổi:</b> Phát hiện một nốt mờ tròn, bờ rõ, kích thước khoảng 14 x 13 mm, tỷ trọng đặc khoảng 32 HU tại phân thùy đỉnh (S1) phổi phải.</li>
                     <li><b>Phế quản:</b> Các phế quản gốc 2 bên thông thoáng, không hẹp.</li>
                     <li><b>Trung thất:</b> Không thấy hạch to, không thấy dịch màng tim.</li>
                   </ul>
                </div>

                <div style={{marginTop:40, textAlign:'right', paddingRight:40}}>
                   <div style={{fontSize:'12px', color:'var(--text-tertiary)'}}>Hà Nội, {patientData.date}</div>
                   <div style={{fontWeight:700, marginTop:10, fontSize:'14px'}}>Bác sĩ CĐHA</div>
                   <div style={{marginTop:60, fontWeight:700, color:'var(--navy-900)'}}>BS. Phạm Minh Tuấn</div>
                </div>
             </div>
          </div>
        </main>

        {/* RIGHT PANEL: SAFETY & VALIDATION */}
        <aside className="panel">
          <div className="panel-h"><div className="lbl">KIỂM TRA AN TOÀN</div></div>
          <div className="panel-b">
             <div className="safety ok">
                <div className="safety-h"><div className="safety-t">PHI CHECK</div><span className="safety-s">100%</span></div>
                <div className="safety-d">Dữ liệu bệnh nhân đã được ẩn danh trên ảnh DICOM.</div>
             </div>
             <div className="safety warn">
                <div className="safety-h"><div className="safety-t">UNCERTAINTY</div><span className="safety-s">3</span></div>
                <div className="safety-d">Cần xác nhận kích thước nốt mờ trên lát cắt S1.</div>
             </div>
             <div className="safety ok">
                <div className="safety-h"><div className="safety-t">FAITHFULNESS</div><span className="safety-s">0.94</span></div>
                <div className="safety-d">Báo cáo bám sát kết quả trích xuất từ AI Detection.</div>
             </div>

             <div style={{marginTop:20}}>
                <div style={{fontSize:'10px', fontWeight:700, color:'var(--text-tertiary)', textTransform:'uppercase', marginBottom:10}}>CITATIONS · MODULAR RAG</div>
                <div className="card" style={{padding:10, fontSize:'11px', background:'var(--navy-50)', border:'none', marginBottom:8}}>
                   <div style={{fontWeight:700, color:'var(--star-red)'}}>RAG-1 · Mẫu biểu CT ngực - BV103 v2.0</div>
                   <div style={{color:'var(--text-tertiary)', marginTop:2}}>Score: 0.96</div>
                </div>
                <div className="card" style={{padding:10, fontSize:'11px', background:'var(--navy-50)', border:'none'}}>
                   <div style={{fontWeight:700, color:'var(--navy-900)'}}>RAG-2 · ACR Lung-RADS 2022</div>
                   <div style={{color:'var(--text-tertiary)', marginTop:2}}>Phân loại nốt phổi · Score: 0.93</div>
                </div>
             </div>
          </div>
        </aside>
      </div>
    </main>
  );
}
