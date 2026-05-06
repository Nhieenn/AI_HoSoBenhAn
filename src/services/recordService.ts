import { PrismaClient } from '@prisma/client';
import { AIService } from './aiService';
import crypto from 'crypto';

const prisma = new PrismaClient();

export interface IngestPayload {
  externalId: string;
  patientId: string;
  content: string;
  type: 'RADIOLOGY' | 'DISCHARGE';
}

export class RecordService {
  /**
   * Băm (hash) mã bệnh nhân bằng SHA-256 kèm theo Salt.
   */
  private static hashPatientId(patientId: string): string {
    const salt = process.env.HASH_SALT || 'vimedai-default-salt';
    return crypto
      .createHash('sha256')
      .update(patientId + salt)
      .digest('hex');
  }

  /**
   * Khởi chạy pipeline ingest (Đồng bộ tạo record gốc, Bất đồng bộ de-id).
   */
  static async ingestDocument(payload: IngestPayload): Promise<string> {
    const patientIdHash = this.hashPatientId(payload.patientId);
    
    // 1. Tạo MedicalRecord ban đầu với trạng thái PENDING
    // Note: We wrap in try-catch in case DB is not available during dev testing.
    try {
      await prisma.medicalRecord.upsert({
        where: { id: payload.externalId },
        update: {
          rawContent: payload.content,
          patientIdHash: patientIdHash,
          status: 'PENDING',
        },
        create: {
          id: payload.externalId,
          rawContent: payload.content,
          patientIdHash: patientIdHash,
          status: 'PENDING',
        },
      });
    } catch (dbError) {
      console.warn('DB not connected yet, skipping initial DB save for PENDING.', dbError);
    }

    // 2. Chạy ngầm tiến trình De-identification (Không await)
    // UC-DEID-01, 02, 03, 04, 05
    this.processDeidAsync(payload.externalId, payload.content).catch(console.error);

    // Trả về Job ID (trong trường hợp này dùng luôn externalId làm jobId)
    return payload.externalId;
  }

  /**
   * Tiến trình xử lý ngầm: Gọi AI Engine ẩn danh và lưu DB.
   */
  private static async processDeidAsync(recordId: string, content: string) {
    try {
      // Gọi AI Engine
      const result = await AIService.deidentify(content);

      // Cập nhật Database
      try {
        // Cập nhật MedicalRecord
        await prisma.medicalRecord.update({
          where: { id: recordId },
          data: {
            deidentifiedContent: result.masked_text,
            status: 'PROCESSED',
          },
        });

        // Ghi Audit Log cho từng thực thể bị mask
        if (result.audit_logs && result.audit_logs.length > 0) {
          const auditData = result.audit_logs.map((log) => ({
            recordId: recordId,
            entityType: log.entityType,
            originalValue: log.originalValue,
            maskedValue: log.maskedValue,
            startPos: log.startPos,
            endPos: log.endPos,
          }));

          await prisma.deidAuditLog.createMany({
            data: auditData,
          });
        }
        
        console.log(`[De-id Async] Successfully processed record ${recordId}`);
      } catch (dbError) {
        console.error(`[De-id Async] Database error while saving record ${recordId}:`, dbError);
        // Fallback update status to ERROR if possible
        try {
          await prisma.medicalRecord.update({
            where: { id: recordId },
            data: { status: 'ERROR' }
          });
        } catch (e) {}
      }

    } catch (aiError) {
      console.error(`[De-id Async] AI Engine error for record ${recordId}:`, aiError);
      
      try {
        await prisma.medicalRecord.update({
          where: { id: recordId },
          data: { status: 'ERROR' }
        });
      } catch (e) {}
    }
  }
}
