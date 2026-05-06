import os
import zipfile

def create_backup():
    source_dir = r"d:\AI_HoSoBenhAn"
    # Lưu file backup ra thẳng ổ D để tránh đầy ổ C
    output_filename = r"d:\ViMedAI_Phase1_POC_Backup.zip"
    
    # Các thư mục cực nặng (thư viện, cache) không cần thiết đưa vào file nộp báo cáo
    excludes = ['node_modules', '.next', '.git', 'venv_prod', '__pycache__', 'cache', '.cache']
    
    print(f"Đang tiến hành nén dự án ViMedAI Phase 1...")
    print(f"Bỏ qua các thư mục nặng: {', '.join(excludes)}")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Lọc bỏ các thư mục rác/nặng
            dirs[:] = [d for d in dirs if d not in excludes]
            
            for file in files:
                # Bỏ qua chính file zip và file script này
                if file.endswith('.zip') or file == 'backup.py':
                    continue
                
                file_path = os.path.join(root, file)
                # Đường dẫn tương đối để giữ cấu trúc thư mục khi giải nén
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                
    print("\n" + "="*50)
    print(f"✅ HOÀN TẤT SAO LƯU DỰ ÁN PHASE 1")
    print(f"📁 File backup được lưu tại: {output_filename}")
    print(f"🔥 Bạn có thể copy file zip này để nộp báo cáo hoặc cất giữ an toàn!")
    print("="*50)

if __name__ == "__main__":
    create_backup()
