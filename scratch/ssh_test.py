import paramiko
import sys

def check_vps():
    host = "45.119.83.233"
    username = "root"
    password = "nSmaPGEY39"
    
    print(f"Đang kết nối SSH tới {host}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=10)
        print("✅ Kết nối thành công!")
        
        commands = [
            "uname -a",
            "cat /etc/os-release | grep PRETTY_NAME",
            "docker --version || echo 'Docker not installed'",
            "docker-compose --version || echo 'Docker-compose not installed'",
            "nginx -v || echo 'Nginx not installed'"
        ]
        
        for cmd in commands:
            print(f"\n> {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            if out: print(out)
            if err: print(err)
            
        ssh.close()
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    check_vps()
