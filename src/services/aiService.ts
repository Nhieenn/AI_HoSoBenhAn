export interface NormalizeResponse {
  full_text: string;
  sections: Record<string, string>;
  unknown_abbreviations: string[];
}

export interface DeidentifyResponse {
  masked_text: string;
  audit_logs: Array<{
    entityType: string;
    originalValue: string;
    maskedValue: string;
    startPos: number;
    endPos: number;
  }>;
}

export class AIService {
  private static AI_ENGINE_URL = process.env.AI_ENGINE_URL || 'http://localhost:8000';

  static async normalize(text: string, dictionary?: Record<string, string>): Promise<NormalizeResponse> {
    try {
      const response = await fetch(`${this.AI_ENGINE_URL}/normalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, dictionary }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to normalize text');
      }

      return await response.json();
    } catch (error) {
      console.error('AIService.normalize error:', error);
      throw error;
    }
  }

  static async deidentify(text: string): Promise<DeidentifyResponse> {
    try {
      const response = await fetch(`${this.AI_ENGINE_URL}/deidentify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to deidentify text');
      }

      return await response.json();
    } catch (error) {
      console.error('AIService.deidentify error:', error);
      throw error;
    }
  }
}
