# API Contracts — AI_HoSoBenhAn

## Auth
### POST /api/auth/login
- Auth: Public
- Body: { email: string, password: string }
- Response 200: { token: string, user: { id, name, role } }
- Response 401: { error: "Invalid credentials" }

## Partners
### GET /api/partners
- Auth: Required (Admin, Manager)
- Query: ?page=1&limit=20&search=keyword&status=ACTIVE
- Response 200: { data: Partner[], total: number, page: number }

### POST /api/partners
- Auth: Required (Admin)
- Body: { name: string, email: string, phone: string }
- Validation: Zod schema (name: min 1, email: valid, phone: regex)
- Response 201: { data: Partner }
- Response 400: { error: "Validation failed", details: [...] }

### PUT /api/partners/:id
- Auth: Required (Admin)
- Body: Partial<Partner>
- Response 200: { data: Partner }
- Response 404: { error: "Partner not found" }
