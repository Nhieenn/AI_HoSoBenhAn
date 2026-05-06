# ViMedAI Production Setup Script
# Run this to initialize a real AI environment on Drive D:

Write-Host "--- ViMedAI: Bat dau thiet lap moi truong san xuat (D:) ---" -ForegroundColor Cyan

# 1. Thiet lap bien moi truong de Model AI khong luu vao o C
$env:HF_HOME = "D:\AI_HoSoBenhAn\.cache\huggingface"
if (!(Test-Path "D:\AI_HoSoBenhAn\.cache")) { New-Item -ItemType Directory -Path "D:\AI_HoSoBenhAn\.cache\huggingface" -Force }
Write-Host "[1/3] Da chuyen huong vung nho dem AI sang o D." -ForegroundColor Green

# 2. Tao moi truong ao Python tren o D
if (!(Test-Path "D:\AI_HoSoBenhAn\venv_prod")) {
    Write-Host "[2/3] Dang tao moi truong ao Python (Venv) tren o D... (Co the mat 1-2 phut)" -ForegroundColor Yellow
    python -m venv D:\AI_HoSoBenhAn\venv_prod
} else {
    Write-Host "[2/3] Moi truong ao da ton tai." -ForegroundColor Green
}

# 3. Cai dat thu vien
Write-Host "[3/3] Dang cai dat cac thu vien AI (Torch, Transformers...)..." -ForegroundColor Yellow
& D:\AI_HoSoBenhAn\venv_prod\Scripts\pip install -r d:\AI_HoSoBenhAn\requirements_prod.txt

Write-Host "--- THIET LAP HOAN TAT ---" -ForegroundColor Cyan
Write-Host "De bat dau chay he thong that, hay dung lenh:" -ForegroundColor White
Write-Host "D:\AI_HoSoBenhAn\venv_prod\Scripts\python ai_engine/main.py" -ForegroundColor Gold
