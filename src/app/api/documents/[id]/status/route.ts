import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

/**
 * GET /api/documents/[id]/status
 * Description: API kiểm tra trạng thái xử lý AI của hồ sơ.
 */
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;

    if (!id) {
      return NextResponse.json({ error: 'Missing document ID' }, { status: 400 });
    }

    // Try to find the record in DB
    try {
      const record = await prisma.medicalRecord.findUnique({
        where: { id },
        select: {
          id: true,
          status: true,
          drafts: {
            select: { id: true },
            take: 1
          }
        }
      });

      if (!record) {
        return NextResponse.json({ error: 'Document not found' }, { status: 404 });
      }

      return NextResponse.json({
        jobId: record.id,
        status: record.status,
        draftId: record.drafts.length > 0 ? record.drafts[0].id : null,
      });

    } catch (dbError) {
       // Fallback for dev environment without DB
       console.warn('DB not connected, returning mock status for ID:', id);
       return NextResponse.json({
         jobId: id,
         status: 'MOCK_PROCESSING (DB Unavailable)',
       });
    }

  } catch (error: any) {
    console.error('Status API Error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal Server Error' },
      { status: 500 }
    );
  }
}
