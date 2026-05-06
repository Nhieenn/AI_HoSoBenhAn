'use client';

import React, { useState, useEffect } from 'react';
import * as api from '../../services/api';

export default function TrainingCenter() {
  const [modelCard, setModelCard] = useState<any>(null);
  const [isTraining, setIsTraining] = useState(false);

  useEffect(() => {
    api.getModelCard().then(setModelCard);
  }, []);

  const startFineTuning = async () => {
    setIsTraining(true);
    // Giả lập quá trình Fine-tuning dựa trên các bản phê duyệt
    setTimeout(() => {
      setIsTraining(false);
      alert("Đã cập nhật trọng số mô hình dựa trên các dữ liệu phê duyệt mới nhất!");
    }, 5000);
  };

  return (
    <main className="main">
      <div className="page-head">
        <h1 className="page-title">Trung tâm Đào tạo AI (Module 8)</h1>
        <button className="btn btn-accent btn-sm" onClick={startFineTuning} disabled={isTraining}>
          {isTraining ? 'Đang huấn luyện...' : 'Bắt đầu Fine-tuning'}
        </button>
      </div>

      <div className="dashboard-grid">
        <div className="panel" style={{ gridColumn: 'span 2' }}>
          <div className="panel-h"><div className="lbl">Thông tin Mô hình (Model Card)</div></div>
          <div className="panel-b" style={{ padding: '20px' }}>
            <div className="fact-grid">
              <div className="fact">
                <div className="fact-k">Phiên bản</div>
                <div className="fact-v">{modelCard?.model_info?.version || "1.0.2-stable"}</div>
              </div>
              <div className="fact">
                <div className="fact-k">Ngày cập nhật cuối</div>
                <div className="fact-v">05/05/2026</div>
              </div>
              <div className="fact">
                <div className="fact-k">Dữ liệu huấn luyện</div>
                <div className="fact-v">12,400 hồ sơ bệnh án</div>
              </div>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-h"><div className="lbl">Kiến thức đã học (RAG Index)</div></div>
          <div className="panel-b" style={{ padding: '20px' }}>
             <ul style={{ listStyle: 'none', padding: 0 }}>
                <li style={{ marginBottom: '10px', fontSize: '13px' }}>✓ Phác đồ Sốt xuất huyết (BYT 2023)</li>
                <li style={{ marginBottom: '10px', fontSize: '13px' }}>✓ Hướng dẫn Nội khoa (BV Bạch Mai)</li>
                <li style={{ marginBottom: '10px', fontSize: '13px' }}>✓ Quy chuẩn CĐHA (Quân Y 108)</li>
             </ul>
          </div>
        </div>
      </div>
    </main>
  );
}
