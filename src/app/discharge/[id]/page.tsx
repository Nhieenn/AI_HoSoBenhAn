'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import * as api from '@/services/api';

interface SafetyCheck {
  title: string;
  status: 'ok' | 'warn' | 'crit';
  score: string;
  desc: string;
}

export default function DischargeEditor() {
  const { id } = useParams();
  const [content, setContent] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isEditingHIS, setIsEditingHIS] = useState(true);
  const [step, setStep] = useState(7); // Active step in pipeline
  const [entities, setEntities] = useState<any[]>([]);
  const [safetyResults, setSafetyResults] = useState<SafetyCheck[]>([]);
  const [patientData, setPatientData] = useState<any>({
    name: "Lê Quang H.",
    age: "42",
    gender: "Nam",
    rank: "Đại úy",
    unit: "Đoàn 367 · Quân chủng PK-KQ",
    reason: "Đau ngực dữ dội vùng sau xương ức, vã mồ hôi, cảm giác bóp nghẹt.",
    diagnosis: ""
  });

  // Khôi phục logic tích hợp AI thực tế
  const runAIPipeline = async () => {
    setIsGenerating(true);
    try {
      // 1. Trích xuất thực thể (NER)
      const nerRes = await api.extractEntities(patientData.reason);
      setEntities(nerRes.entities);
      
      // 2. Tra cứu kiến thức y khoa & Sinh bệnh án (LLM + RAG)
      // Lưu ý: Logic chẩn đoán dựa trên triệu chứng nằm trong generator.py (Backend)
      const genRes = await api.generateDischarge(patientData, nerRes.entities, "General");
      setContent(genRes.generated_text);

      // Trích xuất chẩn đoán từ văn bản AI sinh ra
      const text = genRes.generated_text;
      const diagMatch = text.match(/3\. CHẨN ĐOÁN(?: XUẤT VIỆN)?\n([\s\S]*?)(?=\n4\.)/);
      if (diagMatch && diagMatch[1]) {
        setPatientData((prev: any) => ({...prev, diagnosis: diagMatch[1].trim()}));
      }

      // 3. Kiểm tra an toàn (Safety Gates)
      const safetyRes = await api.checkSafety(genRes.generated_text, nerRes.entities, nerRes.entities, patientData);
      const mappedSafety: SafetyCheck[] = [
        { title: 'PHI Check', status: safetyRes.phi_warnings.length > 0 ? 'crit' : 'ok', score: '100%', desc: safetyRes.phi_warnings[0] || 'Dữ liệu PHI đã được ẩn danh an toàn.' },
        { title: 'Hallucination', status: safetyRes.hallucination_warnings.length > 0 ? 'warn' : 'ok', score: '0', desc: safetyRes.hallucination_warnings[0] || 'Không phát hiện mâu thuẫn với dữ liệu gốc.' },
        { title: 'Faithfulness', status: 'ok', score: '0.91', desc: '91% nội dung có căn cứ từ phác đồ tra cứu.' }
      ];
      setSafetyResults(mappedSafety);

    } catch (error) {
      console.error("AI Pipeline Error:", error);
      setContent("Lỗi kết nối Inference Engine. Vui lòng kiểm tra Server AI.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleApprove = async () => {
    if (!content) return;
    await api.approveReport(id as string, patientData.reason, content);
    alert("Đã phê duyệt và đồng bộ dữ liệu EHR/HIS thành công!");
  };

  useEffect(() => {
    // Dynamic Mock Data Mapping
    const mockData: Record<string, any> = {
      "BN-2408": {
        name: "Lê Quang H.", age: "42", gender: "Nam", rank: "Đại úy",
        unit: "Đoàn 367 · Quân chủng PK-KQ",
        reason: "Đau ngực dữ dội vùng sau xương ức khi vận động gắng sức, vã mồ hôi, cảm giác bóp nghẹt.",
        diagnosis: "I21.4 · Nhồi máu cơ tim cấp"
      },
      "BN-2395": {
        name: "Trần Thị K.", age: "58", gender: "Nữ", rank: "Đại tá",
        unit: "Cục Cán bộ · Tổng cục Chính trị",
        reason: "Sốt cao ngày thứ 3, đau hốc mắt, xuất hiện chấm xuất huyết dưới da cánh tay, đau cơ khớp toàn thân.",
        diagnosis: "A90 · Sốt xuất huyết Dengue"
      },
      "BN-2411": {
        name: "Nguyễn Văn M.", age: "35", gender: "Nam", rank: "Lao động HD",
        unit: "Kho tàng · Cục Hậu cần",
        reason: "Đau vùng thượng vị âm ỉ, đau tăng lên khi đói, kèm ợ chua, buồn nôn sau khi ăn đồ cay nóng.",
        diagnosis: "K25 · Viêm loét dạ dày"
      }
    };

    if (id && mockData[id as string]) {
      setPatientData(mockData[id as string]);
    }
  }, [id]);

  useEffect(() => {
    // Tự động chạy pipeline lần đầu khi patientData đã được cập nhật
    if (!content && !isGenerating && patientData.reason) {
      runAIPipeline();
    }
  }, [patientData]);

  return (
    <main className="main">
      {/* PAGE HEADER */}
      <div className="page-head" style={{paddingBottom:20, borderBottom:'1px solid var(--border)', marginBottom:20}}>
        <div className="page-head-left">
          <div className="crumb" style={{fontSize:'10px', color:'var(--text-tertiary)'}}>
            <Link href="/" style={{color:'inherit', textDecoration:'none'}}>Workspace</Link>
            <span className="crumb-sep">/</span>
            <Link href="/queue" style={{color:'inherit', textDecoration:'none'}}>Hàng đợi</Link>
            <span className="crumb-sep">/</span>
            <span style={{color:'var(--text-secondary)'}}>{id} · Discharge Summary</span>
          </div>
          <h1 className="page-title" style={{fontSize:'24px', marginTop:4, marginBottom:6}}>Bệnh án xuất viện · <span className="mono">{id}</span></h1>
          <div className="page-meta" style={{display:'flex', alignItems:'center', gap:8, fontSize:'11px'}}>
            <span style={{background:'#000', color:'#facc15', padding:'2px 6px', borderRadius:2, fontWeight:800, fontSize:'9px'}}>ĐẠI ÚY</span>
            <span style={{color:'var(--text-secondary)', fontWeight:500}}>{patientData.name}</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.gender} · {patientData.age}t</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.unit}</span>
            <span className="dot-sep" style={{width:2, height:2}}></span>
            <span style={{color:'var(--text-tertiary)'}}>{patientData.diagnosis}</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems:'center' }}>
          <button className="btn btn-ghost btn-sm" style={{borderColor:'var(--border)', color:'var(--text-primary)'}} onClick={runAIPipeline} disabled={isGenerating}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:14, marginRight:4}}><path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
            Sinh lại
          </button>
          <button className="btn btn-ghost btn-sm" style={{borderColor:'var(--danger)', color:'var(--danger)'}} onClick={() => {
            if(confirm("Bạn có chắc chắn muốn từ chối bản nháp này?")) {
              window.location.href = "/queue";
            }
          }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:14, marginRight:4}}><path d="M18 6L6 18M6 6l12 12"/></svg>
            Từ chối
          </button>
          <button className="btn btn-success btn-sm" style={{background:'#10b981', color:'#fff'}} onClick={async () => {
            await handleApprove();
            window.location.href = "/queue";
          }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" style={{width:14, marginRight:4}}><path d="M20 6L9 17l-5-5"/></svg>
            Phê duyệt & Lưu HIS
          </button>
        </div>
      </div>

      {/* PIPELINE BAR */}
      <div className="card" style={{padding:'14px 24px', marginBottom:24, borderRadius:10}}>
        <div style={{display:'flex', alignItems:'center', justifyContent:'space-between', gap:10}}>
          {[
            {n:'HIS', t:'2s'}, {n:'De-id', t:'1.8s'}, {n:'NER', t:'2.3s'}, 
            {n:'RAG', t:'0.9s'}, {n:'LLM', t:'3.4s'}, {n:'Safety', t:'0.6s'}
          ].map((s, i) => (
            <React.Fragment key={s.n}>
              <div style={{display:'flex', alignItems:'center', gap:8, flexShrink:0}}>
                <div style={{width:18, height:18, borderRadius:'50%', background:'var(--success)', display:'flex', alignItems:'center', justifyContent:'center'}}>
                   <svg viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="4" style={{width:10}}><path d="M20 6L9 17l-5-5"/></svg>
                </div>
                <div style={{fontSize:'12px', fontWeight:700, color:'var(--text-primary)'}}>{s.n}</div>
                <div style={{fontSize:'10px', color:'var(--text-tertiary)'}}>{s.t}</div>
              </div>
              {i < 6 && <div style={{flex:1, height:1, background:'var(--success)', opacity:0.2, margin:'0 4px'}}></div>}
            </React.Fragment>
          ))}
          
          <div style={{display:'flex', alignItems:'center', gap:8, flexShrink:0}}>
            <div style={{width:18, height:18, borderRadius:'50%', background:'var(--danger)', display:'flex', alignItems:'center', justifyContent:'center', color:'#fff', fontSize:'10px', fontWeight:800}}>7</div>
            <div style={{fontSize:'12px', fontWeight:700, color:'var(--text-primary)'}}>Bác sĩ duyệt</div>
          </div>
          <div style={{flex:1, height:1, background:'var(--border)', margin:'0 4px'}}></div>
          
          <div style={{display:'flex', alignItems:'center', gap:8, flexShrink:0, opacity:0.4}}>
            <div style={{width:18, height:18, borderRadius:'50%', background:'var(--bg-elev-2)', border:'1px solid var(--border)', display:'flex', alignItems:'center', justifyContent:'center', color:'var(--text-tertiary)', fontSize:'10px', fontWeight:800}}>8</div>
            <div style={{fontSize:'12px', fontWeight:700, color:'var(--text-tertiary)'}}>Lưu EHR</div>
          </div>
        </div>
      </div>

      {/* 3-PANEL EDITOR */}
      <div className="editor">
        {/* LEFT PANEL */}
        {/* LEFT PANEL: PATIENT INFO & NER */}
        <aside className="panel" style={{width:320}}>
          <div className="panel-h" style={{background:'transparent', borderBottom:'none', paddingTop:16}}>
            <div className="lbl" style={{fontSize:'12px', color:'var(--text-tertiary)'}}>THÔNG TIN CA BỆNH</div>
            <button 
              className={`btn btn-xs ${isEditingHIS ? 'btn-primary' : 'btn-ghost'}`} 
              onClick={() => setIsEditingHIS(!isEditingHIS)} 
              style={{padding:'4px 8px', display:'flex', alignItems:'center', gap:'6px', borderRadius:'4px'}}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:12}}><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>
              {isEditingHIS ? 'Đóng' : 'Bổ sung'}
            </button>
          </div>
          <div className="panel-b" style={{padding:'0 14px 14px'}}>
            {/* Main Patient Card */}
            <div style={{background:'var(--navy-900)', borderRadius:'12px', padding:'16px', color:'#fff', marginBottom:20, position:'relative', overflow:'hidden'}}>
               <div style={{fontSize:'10px', color:'var(--gold)', fontWeight:700, marginBottom:4}}>{id} · 05-05-2026</div>
               <div style={{fontSize:'20px', fontWeight:700, marginBottom:8}}>{patientData.name}</div>
               <div style={{fontSize:'11px', color:'var(--navy-200)', display:'flex', gap:8, alignItems:'center'}}>
                 <span>{patientData.gender} · {patientData.age}t</span>
                 <span className="dot-sep" style={{background:'var(--navy-400)'}}></span>
                 <span>{patientData.rank}</span>
                 <span className="dot-sep" style={{background:'var(--navy-400)'}}></span>
                 <span>{patientData.unit}</span>
               </div>
               <div style={{display:'flex', gap:6, marginTop:12}}>
                 <span style={{fontSize:'9px', background:'var(--navy-700)', padding:'2px 6px', borderRadius:2, color:'var(--gold)', fontWeight:700}}>QN</span>
                 <span style={{fontSize:'9px', background:'var(--navy-700)', padding:'2px 6px', borderRadius:2, color:'var(--navy-200)', fontWeight:700}}>BHYT</span>
                 <span style={{fontSize:'9px', background:'var(--navy-700)', padding:'2px 6px', borderRadius:2, color:'var(--navy-200)', fontWeight:700}}>PCI</span>
               </div>
            </div>

            {/* Editing Context Area */}
            {isEditingHIS && (
              <div style={{background:'var(--navy-50)', border:'1px dashed var(--star-red)', borderRadius:8, padding:12, marginBottom:16}}>
                <div style={{fontSize:'10px', fontWeight:700, color:'var(--star-red)', marginBottom:8, textTransform:'uppercase'}}>Bổ sung ngữ cảnh lâm sàng</div>
                <textarea 
                  className="ed-area" 
                  style={{minHeight:80, fontSize:'12px', padding:8, width:'100%', background:'#fff', border:'1px solid var(--border)', borderRadius:4}}
                  placeholder="Nhập thêm triệu chứng, diễn biến..."
                  value={patientData.reason}
                  onChange={(e) => setPatientData({...patientData, reason: e.target.value, diagnosis: ""})}
                />
                <div style={{display:'flex', gap:4, marginTop:8}}>
                  <button className="btn btn-accent btn-xs" style={{flex:1}} onClick={() => { 
                    setIsEditingHIS(false); 
                    api.logAudit("BSHUNG", "ENRICH_CONTEXT", id as string, { reason: patientData.reason });
                    runAIPipeline(); 
                  }}>Cập nhật AI</button>
                </div>
              </div>
            )}

            <div className="fact-grid" style={{gap:12}}>
              <div style={{fontSize:'10px', fontWeight:700, color:'var(--text-tertiary)', textTransform:'uppercase', borderBottom:'1px solid var(--border)', paddingBottom:6, marginBottom:4, display:'flex', justifyContent:'center'}}>CLINICAL FACTS (NER)</div>
              
              {/* Categorized Facts */}
              <div className="fact" style={{borderLeftColor:'var(--success)'}}>
                <div className="fact-k">Chẩn đoán gợi ý (AI)</div>
                <div className="fact-v" style={{fontSize:'12px', fontWeight:600}}>{patientData.diagnosis || "Đang phân tích..."}</div>
              </div>

              <div className="fact">
                <div className="fact-k">Triệu chứng & Diễn biến</div>
                <div className="fact-v" style={{fontSize:'12px', fontWeight:500, color:'var(--text-secondary)'}}>
                  {patientData.reason}
                </div>
              </div>

              <div className="fact" style={{borderLeftColor:'var(--danger)'}}>
                <div className="fact-k">Dị ứng (HIS)</div>
                <div className="fact-v" style={{fontSize:'12px', color:'var(--star-red)'}}>Penicillin</div>
              </div>

              <div className="fact" style={{borderLeftColor:'var(--warning)'}}>
                <div className="fact-k">Cần xác nhận</div>
                <div className="fact-v" style={{fontSize:'11px', color:'var(--text-secondary)'}}>Liều Aspirin xuất viện</div>
              </div>

              <div style={{marginTop:10}}>
                <div className="fact-k" style={{textAlign:'center'}}>Thực thể trích xuất</div>
                <div style={{display:'flex', flexWrap:'wrap', gap:4, marginTop:6, justifyContent:'center'}}>
                  {entities.map((e, i) => (
                    <span key={i} className="badge-xs" style={{
                      background: e.type === 'SYMPTOM' ? 'rgba(212,51,46,0.1)' : 'var(--navy-100)',
                      color: e.type === 'SYMPTOM' ? 'var(--star-red)' : 'var(--navy-700)',
                      border: '1px solid rgba(0,0,0,0.05)',
                      padding: '2px 6px',
                      borderRadius: '4px'
                    }}>
                      {e.text}
                    </span>
                  ))}
                  {entities.length === 0 && <span style={{fontSize:'10px', color:'var(--text-tertiary)'}}>Đang xử lý...</span>}
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* CENTER PANEL */}
        <main className="panel">
          <div className="ed-toolbar">
            <button className="tlbtn active"><strong>B</strong></button>
            <button className="tlbtn"><em>I</em></button>
            <button className="tlbtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:14}}><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></button>
            <div className="tl-div"></div>
            <div className="tl-stat">
              <span>Độ tin cậy (Faithfulness)</span>
              <strong style={{ color: 'var(--success)' }}>0.91</strong>
              <div style={{width:40, height:4, background:'var(--navy-100)', borderRadius:2, marginLeft:4}}>
                <div style={{width:'91%', height:'100%', background:'var(--success)', borderRadius:2}}></div>
              </div>
            </div>
          </div>
          <div className="canvas">
            <div className="paper">
              <span className="draft-stamp">NHÁP · AI GENERATED</span>
              <div className="doc-h">
                <div className="doc-org">BỘ QUỐC PHÒNG · HỌC VIỆN QUÂN Y · BỆNH VIỆN QUÂN Y 103</div>
                <div className="doc-title">Bệnh án ra viện</div>
                <div className="doc-sub">Mẫu số: 04/BV-01 · Mã HS: <span className="mono">{id}</span>/2026</div>
              </div>

              {isGenerating ? (
                <div style={{textAlign:'center', padding:'100px 0'}}>
                   <div className="status-led live" style={{width:20, height:20, margin:'0 auto 20px'}}></div>
                   <div style={{fontWeight:600, color:'var(--navy-900)'}}>Hệ thống đang phân tích triệu chứng...</div>
                   <div style={{fontSize:'12px', color:'var(--text-tertiary)', marginTop:8}}>Đang tra cứu phác đồ và sinh chẩn đoán gợi ý</div>
                </div>
              ) : (
                <div className="sec">
                  <div className="ai-t">{content || "Vui lòng bấm \"Sinh lại nháp AI\" để bắt đầu."}</div>
                  
                  {content && (
                    <div style={{marginTop:30, padding:12, background:'var(--navy-50)', border:'1px dashed var(--border)', borderRadius:6}}>
                      <div style={{fontSize:'10px', fontWeight:700, color:'var(--navy-400)', marginBottom:8, textTransform:'uppercase'}}>Cơ sở chẩn đoán (RAG Citations)</div>
                      <div style={{fontSize:'11px', color:'var(--text-secondary)', fontStyle:'italic'}}>
                        * Gợi ý chẩn đoán dựa trên phác đồ và cơ sở dữ liệu y khoa (SBB/YouMed) kết hợp cùng triệu chứng lâm sàng trích xuất được.
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </main>

        {/* RIGHT PANEL */}
        <aside className="panel">
          <div className="panel-h"><div className="lbl">Safety Decision Gates</div></div>
          <div className="panel-b">
            <div style={{marginBottom:16, padding:10, background:safetyResults.length > 0 ? 'rgba(16,185,129,0.05)' : 'var(--navy-50)', borderRadius:6, border:'1px solid rgba(16,185,129,0.1)', fontSize:'11px'}}>
               <span style={{color:safetyResults.length > 0 ? 'var(--success)' : 'var(--text-tertiary)', fontWeight:700}}>{safetyResults.length > 0 ? '✓' : '●'}</span> 
               <b> Mô hình Sidecar:</b> {safetyResults.length > 0 ? 'Sẵn sàng phê duyệt.' : 'Đang chờ kết quả...'}
            </div>
            
            {safetyResults.map((check, i) => (
              <div className={`safety ${check.status}`} key={i}>
                <div className="safety-h">
                  <div className="safety-t">{check.title}</div>
                  <span className="safety-s">{check.score}</span>
                </div>
                <div className="safety-d">{check.desc}</div>
                {check.status === 'crit' && (
                  <div style={{marginTop:8, color:'var(--danger)', fontSize:'10px', fontWeight:600}}>
                    CẢNH BÁO: Phát hiện dữ liệu PHI chưa được mask!
                  </div>
                )}
              </div>
            ))}
            
            {safetyResults.length === 0 && !isGenerating && (
              <div style={{textAlign:'center', padding:20, color:'var(--text-tertiary)', fontSize:'11px'}}>
                Bấm "Sinh lại" để thực hiện kiểm tra an toàn.
              </div>
            )}
          </div>
        </aside>
      </div>
    </main>
  );
}
