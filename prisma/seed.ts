import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();
import * as crypto from 'crypto';


async function main() {
  console.log('Bắt đầu seed dữ liệu mẫu...');

  // 1. Seed Departments
  const deptGeneral = await prisma.department.upsert({
    where: { name: 'Khoa Nội Tổng Hợp' },
    update: {},
    create: { name: 'Khoa Nội Tổng Hợp' },
  });

  const deptCardio = await prisma.department.upsert({
    where: { name: 'Khoa Tim Mạch' },
    update: {},
    create: { name: 'Khoa Tim Mạch' },
  });

  console.log('Đã seed Departments.');

  // 2. Seed Users
  // Mật khẩu mẫu: 123456 (Trong thực tế phải băm bằng bcrypt, ở đây lưu plaintext tạm cho dev nếu auth đang mock, 
  // nhưng nếu auth dùng bcrypt thì phải băm. Giả định dùng bcrypt, băm sẵn "123456": $2b$10$EP...)
  // Để đơn giản, ta dùng chuỗi hash sẵn hoặc plaintext tùy hệ thống hiện tại.
  const passwordHash = "123456"; 

  const admin = await prisma.user.upsert({
    where: { username: 'admin' },
    update: {},
    create: {
      username: 'admin',
      password: passwordHash,
      role: 'ADMIN',
      departmentId: deptGeneral.id,
    },
  });

  const doctor1 = await prisma.user.upsert({
    where: { username: 'doctor1' },
    update: {},
    create: {
      username: 'doctor1',
      password: passwordHash,
      role: 'DOCTOR',
      departmentId: deptCardio.id,
    },
  });

  const nurse1 = await prisma.user.upsert({
    where: { username: 'nurse1' },
    update: {},
    create: {
      username: 'nurse1',
      password: passwordHash,
      role: 'NURSE',
      departmentId: deptGeneral.id,
    },
  });

  console.log('Đã seed Users.');

  // 3. Seed Medical Records
  const patientHash1 = crypto.createHash('sha256').update('BN001').digest('hex');
  
  const record1 = await prisma.medicalRecord.upsert({
    where: { id: 'REC-001' },
    update: {},
    create: {
      id: 'REC-001',
      rawContent: 'Bệnh nhân Nguyễn Văn A, sinh năm 1980. Vào viện vì đau ngực trái.',
      deidentifiedContent: 'Bệnh nhân [NAME_1], sinh năm [DATE_1]. Vào viện vì đau ngực trái.',
      patientIdHash: patientHash1,
      status: 'PROCESSED',
    },
  });

  const record2 = await prisma.medicalRecord.upsert({
    where: { id: 'REC-002' },
    update: {},
    create: {
      id: 'REC-002',
      rawContent: 'Bệnh nhân Trần Thị B, 45 tuổi. Tiền sử tăng huyết áp.',
      deidentifiedContent: 'Bệnh nhân [NAME_2], [AGE_1] tuổi. Tiền sử tăng huyết áp.',
      patientIdHash: crypto.createHash('sha256').update('BN002').digest('hex'),
      status: 'PENDING',
    },
  });

  console.log('Đã seed MedicalRecords.');

  // 4. Seed AIDraft
  // Tìm AIDraft hiện có để không lỗi duplicate (nếu tạo bằng id)
  const existingDraft = await prisma.aIDraft.findFirst({
    where: { recordId: record1.id }
  });

  if (!existingDraft) {
    await prisma.aIDraft.create({
      data: {
        recordId: record1.id,
        doctorId: doctor1.id,
        status: 'DRAFT',
        version: 1,
        content: {
            "title": "TÓM TẮT HỒ SƠ BỆNH ÁN TIM MẠCH",
            "patientName": "[NAME_1]",
            "symptoms": ["đau ngực trái"],
            "diagnosis": "Theo dõi nhồi máu cơ tim [UNCERTAIN]"
        }
      }
    });
    console.log('Đã seed AIDraft.');
  }

  // 5. Seed ReportTemplate
  const templateCardio = await prisma.reportTemplate.upsert({
    where: { id: 'TMP-CARDIO-01' },
    update: {},
    create: {
      id: 'TMP-CARDIO-01',
      name: 'Tóm tắt bệnh án Tim Mạch',
      requiredKeys: ['HÀNH CHÍNH', 'LÝ DO VÀO VIỆN', 'BỆNH SỬ', 'CẬN LÂM SÀNG', 'CHẨN ĐOÁN', 'KẾ HOẠCH ĐIỀU TRỊ'],
      content: 'Mẫu báo cáo chuẩn cho khoa Tim Mạch...',
      departmentId: deptCardio.id,
    },
  });
  console.log('Đã seed ReportTemplate.');

  console.log('Quá trình seed hoàn tất!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
