import { PrismaClient, DictCategory } from '@prisma/client';

const prisma = new PrismaClient();

export interface DictEntry {
  abbr: string;
  fullText: string;
  category: DictCategory;
  departmentId?: string;
}

export class DictionaryService {
  /**
   * UC-NORM-05: Create or update a dictionary entry.
   */
  static async upsertEntry(data: DictEntry) {
    return prisma.normalizationDict.upsert({
      where: {
        // Note: For simplicity, using abbr as unique in this example logic.
        // In reality, it might be unique per department.
        id: await this.findIdByAbbrAndDept(data.abbr, data.departmentId) || '',
      },
      update: {
        fullText: data.fullText,
        category: data.category,
      },
      create: {
        abbr: data.abbr,
        fullText: data.fullText,
        category: data.category,
        departmentId: data.departmentId,
      },
    });
  }

  private static async findIdByAbbrAndDept(abbr: string, deptId?: string) {
    const entry = await prisma.normalizationDict.findFirst({
      where: { abbr, departmentId: deptId },
    });
    return entry?.id;
  }

  /**
   * UC-NORM-05: Get all entries for a specific department.
   */
  static async getEntries(departmentId?: string) {
    return prisma.normalizationDict.findMany({
      where: departmentId ? { departmentId } : {},
      orderBy: { abbr: 'asc' },
    });
  }

  /**
   * Delete an entry.
   */
  static async deleteEntry(id: string) {
    return prisma.normalizationDict.delete({
      where: { id },
    });
  }

  /**
   * Convert DB entries to a simple Record for AI Engine.
   */
  static async getDictionaryForAI(departmentId?: string): Promise<Record<string, string>> {
    const entries = await this.getEntries(departmentId);
    const dict: Record<string, string> = {};
    entries.forEach(e => {
      dict[e.abbr.toUpperCase()] = e.fullText;
    });
    return dict;
  }
}
