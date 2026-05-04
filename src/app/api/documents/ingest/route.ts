import { NextRequest, NextResponse } from 'next/server';
import { RecordService, IngestPayload } from '@/services/recordService';

/**
 * POST /api/documents/ingest
 * Description: API nhận hồ sơ từ HIS và khởi chạy pipeline AI (Bất đồng bộ).
 */
export async function POST(req: NextRequest) {
  try {
    const data: Partial<IngestPayload> = await req.json();

    // 1. Input Validation cơ bản
    if (!data.externalId || !data.patientId || !data.content || !data.type) {
      return NextResponse.json(
        { error: 'Missing required fields: externalId, patientId, content, type' },
        { status: 400 }
      );
    }

    if (data.type !== 'RADIOLOGY' && data.type !== 'DISCHARGE') {
      return NextResponse.json(
        { error: 'Invalid document type. Must be RADIOLOGY or DISCHARGE.' },
        { status: 400 }
      );
    }

    // 2. Chạy Ingest Pipeline
    const jobId = await RecordService.ingestDocument(data as IngestPayload);

    // 3. Phản hồi lập tức theo API Contracts
    return NextResponse.json(
      { jobId: jobId, status: 'PROCESSING' },
      { status: 202 } // 202 Accepted
    );

  } catch (error: any) {
    console.error('Ingest API Error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal Server Error' },
      { status: 500 }
    );
  }
}
