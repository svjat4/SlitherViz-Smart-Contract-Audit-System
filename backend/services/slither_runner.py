import asyncio
import json
import os
import uuid
import traceback
import subprocess
from typing import Tuple, Optional

# Semaphore & Lock untuk Rate Limiting (250ms Token Bucket)
_rate_limit_lock = asyncio.Lock()

async def rate_limited_sleep(delay: float = 0.25):
    async with _rate_limit_lock:
        await asyncio.sleep(delay)

def execute_slither_sync(cmd: str) -> Tuple[bytes, bytes]:
    """
    Fungsi pembantu: Menjalankan subprocess secara sinkron.
    """
    process = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process.stdout, process.stderr

async def run_slither_audit(address: str, api_key: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    """
    Menjalankan Slither CLI dengan sistem Threading dan penanganan file aman untuk Windows.
    """
    await rate_limited_sleep(0.25)
    
    temp_filename = f"temp_slither_{address}_{uuid.uuid4().hex[:6]}.json"
    cmd = f"slither {address} --etherscan-apikey {api_key} --json {temp_filename}"
    print(f"\n[DEBUG] Menjalankan: {cmd}")
    
    output_data = None
    read_success = False
    
    try:
        stdout, stderr = await asyncio.to_thread(execute_slither_sync, cmd)
        
        # 1. Cek apakah file JSON berhasil dibuat
        if os.path.exists(temp_filename):
            size = os.path.getsize(temp_filename)
            print(f"[DEBUG] File JSON berhasil dibuat. Ukuran: {size} bytes")
            
            if size > 0:
                # BUKA DAN BACA FILE (Blok 'with' akan otomatis menutup file setelah selesai)
                with open(temp_filename, 'r', encoding='utf-8') as f:
                    try:
                        output_data = json.load(f)
                        if output_data.get('success', False) or 'results' in output_data:
                            read_success = True
                    except json.JSONDecodeError as e:
                        print(f"[DEBUG] Gagal membaca JSON: {e}")
            else:
                print(f"[DEBUG] File JSON kosong untuk {address}.")
        
        # 2. HAPUS FILE (Dipindah ke luar blok 'with' agar Windows tidak memblokirnya)
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except Exception as e:
                print(f"[DEBUG] Gagal menghapus file temp: {e}")

        # 3. Kembalikan hasil jika sukses
        if read_success and output_data:
            print(f"[DEBUG] Audit {address} SUKSES.")
            return True, output_data, None
                    
        # 4. Tangkap error dari terminal jika gagal
        err_str = stderr.decode('utf-8', errors='ignore') or stdout.decode('utf-8', errors='ignore')
        print(f"[DEBUG] Output Terminal Slither:\n{err_str[:500]}...") 
        
        if "not verified" in err_str.lower():
            return False, None, "Contract is not verified on Etherscan."
        
        error_msg = err_str.strip()[:200] + "..." if len(err_str) > 200 else err_str
        return False, None, error_msg or "Unknown compilation error."
        
    except Exception as e:
        print(f"[DEBUG] Terjadi Exception di Python:\n{traceback.format_exc()}")
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass
        return False, None, str(e)