import { NextRequest, NextResponse } from 'next/server';
import { DictionaryService } from '@/services/dictionaryService';

/**
 * UC-NORM-05: CRUD API for Normalization Dictionary
 */
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const deptId = searchParams.get('deptId') || undefined;
    
    const entries = await DictionaryService.getEntries(deptId);
    return NextResponse.json(entries);
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const data = await req.json();
    
    if (!data.abbr || !data.fullText) {
      return NextResponse.json({ error: 'Abbr and FullText are required' }, { status: 400 });
    }
    
    const result = await DictionaryService.upsertEntry(data);
    return NextResponse.json(result, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function DELETE(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('id');
    
    if (!id) {
      return NextResponse.json({ error: 'ID is required' }, { status: 400 });
    }
    
    await DictionaryService.deleteEntry(id);
    return NextResponse.json({ success: true });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
