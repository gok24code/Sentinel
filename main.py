import psutil
import time
import json
from datetime import datetime

known_pids = set()

print("Monitoring process creation. Press Ctrl+C to stop.")
print("===========================================================")

def get_process_info(pid):
    try:
        proc = psutil.Process(pid)
        
        # Kernel Thread Kontrolü:
        # Kernel işlemleri genellikle argümansızdır (cmdline boştur)
        try:
            cmdline = proc.cmdline()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            cmdline = []

        # Eğer cmdline boşsa, bu muhtemelen bir Kernel işlemidir. Atla.
        if not cmdline:
            return None
        # Verileri tek tek, hata korumalı (Safe Mode) alalım
        p_name = proc.name()
        
        try:
            p_exe = proc.exe()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            p_exe = "" # Erişim izni yoksa boş bırak
            
        try:
            
            p_user = proc.username()
        except Exception: 
            p_user = "unknown"

        return {
            "pid": pid,
            "name": p_name,
            "exe": p_exe,
            "user": p_user,
            "create_time": datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None    
while True: 
    current_pids = set(psutil.pids())
    new_pids = current_pids - known_pids

    for pid in new_pids:
        info = get_process_info(pid)
        
        if info:
            risk_level = "NORMAL"
            
            if info['exe'] and ("/tmp" in info['exe'] or "/dev/shm" in info['exe']):
                risk_level = "CRITICAL RISK"
            
            if info['user'] == 'root' and "sudo" not in info['name']:
                risk_level = "WARNING"


            #json formatında loglama -> veritabanına veya dosyaya kaydetmek için kullanılabilir
            log_message = {
                "Zaman": datetime.now().strftime('%H:%M:%S'),
                "Risk": risk_level,
                "Process": info['name'],
                "PID": info['pid'],
                "Yol": info['exe'],
                "Kullanıcı": info['user']
            }
            
            if risk_level == "CRITICAL RISK":
                print(f"\n🚨 [ALARM] {json.dumps(log_message, indent=2)}")
            else:
                print(f"Checking... {info['name']} (PID: {info['pid']}) -> {risk_level}")

    known_pids = current_pids
    time.sleep(1)