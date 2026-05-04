# Kiến Trúc Hệ Thống — AI_HoSoBenhAn
# Cập nhật: 04/05/2026

## Tech Stack
- Frontend: Next.js 14 (App Router)
- Backend: Next.js API Routes
- Database: PostgreSQL
- ORM: Prisma
- Auth: NextAuth / JWT custom
- Deploy: VPS Ubuntu / Docker / Vercel

## Cấu Trúc Thư Mục
src/
├── app/           ← Pages & API Routes
├── components/    ← UI Components
├── lib/           ← Utils, DB client, Auth
├── types/         ← TypeScript interfaces
└── middleware.ts  ← Auth & Security middleware

## Sơ Đồ Hệ Thống
[Client Browser]
    ↓ HTTPS
[Nginx Reverse Proxy] (SSL termination, rate limiting)
    ↓
[Next.js App] (PM2 managed)
    ↓
[PostgreSQL Database]
    ↓
[External Services: PayOS, Telegram, Email]

## Environment Variables
DATABASE_URL       ← PostgreSQL connection string
NEXTAUTH_SECRET    ← JWT signing key
NEXTAUTH_URL       ← Base URL
PAYOS_API_KEY      ← Payment gateway (if applicable)
