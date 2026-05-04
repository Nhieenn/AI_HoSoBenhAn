import { NextRequest, NextResponse } from 'next/server';
import { AIService } from '@/services/aiService';

/**
 * API Route: /api/ai/normalize
 * Description: Internal endpoint to handle medical text normalization.
 */
export async function POST(req: NextRequest) {
  try {
    const { text, dictionary } = await req.json();

    if (!text) {
      return NextResponse.json({ error: 'Text is required' }, { status: 400 });
    }

    const result = await AIService.normalize(text, dictionary);
    
    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal Server Error' },
      { status: 500 }
    );
  }
}
