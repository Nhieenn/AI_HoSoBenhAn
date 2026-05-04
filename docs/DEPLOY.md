# Hướng Dẫn Deploy — AI_HoSoBenhAn

## 1. Yêu Cầu Hệ Thống
- OS: Ubuntu 22.04 LTS (Khuyên dùng)
- Node.js: v18.x trở lên
- Database: PostgreSQL 15+
- Web Server: Nginx
- Process Manager: PM2

## 2. Chuẩn Bị Server (Lần đầu)
### Cài đặt Node.js & PM2
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install pm2 -g
```

### Cài đặt Nginx & SSL (Certbot)
```bash
sudo apt install nginx
sudo apt install certbot python3-certbot-nginx
```

## 3. Quy Trình Deploy (CI/CD hoặc Thủ công)

### Bước 1: Clone & Cài đặt
```bash
git clone https://github.com/your-repo/AI_HoSoBenhAn.git
cd AI_HoSoBenhAn
npm install
```

### Bước 2: Cấu hình Environment
Tạo file `.env` từ mẫu `.env.example` và điền các tham số thực tế (Database URL, JWT Secret, v.v.)

### Bước 3: Build dự án
```bash
npx prisma generate
npm run build
```

### Bước 4: Chạy Migration (Database)
```bash
npx prisma migrate deploy
```

### Bước 5: Khởi chạy với PM2
```bash
pm2 start npm --name "ai-hoso-benhan" -- start
pm2 save
```

## 4. Cấu Hình Nginx (Reverse Proxy)
Tạo file `/etc/nginx/sites-available/ai-hoso-benhan`:
```nginx
server {
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
Kích hoạt config và cài SSL:
```bash
sudo ln -s /etc/nginx/sites-available/ai-hoso-benhan /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d yourdomain.com
```

## 5. Bảo Trì & Monitor
- **Xem log:** `pm2 logs ai-hoso-benhan`
- **Restart app:** `pm2 restart ai-hoso-benhan`
- **Backup DB:** Sử dụng `pg_dump` định kỳ hàng ngày (theo quy tắc trong SECURITY.md)
