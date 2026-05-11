# auto_updater.py - Hệ thống tự động cập nhật từ GitHub Releases
import urllib.request
import urllib.error
import json
import os
import sys
import subprocess
import threading
import tempfile

# Cấu hình
CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "qualaduoc/Tool-nhan-xet-hoc-sinh-EXE"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
EXE_NAME = "ETA_Connect_NhanXet.exe"


def get_current_version():
    """Trả về phiên bản hiện tại"""
    return CURRENT_VERSION


def _parse_version(v_str):
    """Chuyển '1.2.3' thành tuple (1, 2, 3) để so sánh"""
    clean = v_str.strip().lstrip("vV")
    parts = clean.split(".")
    return tuple(int(p) for p in parts if p.isdigit())


def check_for_update():
    """
    Kiểm tra phiên bản mới trên GitHub Releases.
    Trả về: (has_update: bool, info: dict|None)
    info chứa: version, download_url, release_notes, published_at
    """
    try:
        req = urllib.request.Request(GITHUB_API, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ETA-Connect-Updater"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        latest_tag = data.get("tag_name", "")
        latest_ver = _parse_version(latest_tag)
        current_ver = _parse_version(CURRENT_VERSION)

        if latest_ver <= current_ver:
            return False, None

        # Tìm file .exe trong assets
        download_url = None
        file_size = 0
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith(".exe") and "KeyGen" not in name:
                download_url = asset.get("browser_download_url")
                file_size = asset.get("size", 0)
                break

        if not download_url:
            return False, None

        info = {
            "version": latest_tag,
            "download_url": download_url,
            "release_notes": data.get("body", "Không có ghi chú."),
            "published_at": data.get("published_at", ""),
            "file_size": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 1) if file_size else 0,
        }
        return True, info

    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        return False, None


def check_for_update_async(callback):
    """
    Kiểm tra bản mới trong background thread.
    callback(has_update, info) sẽ được gọi khi hoàn tất.
    """
    def _worker():
        result = check_for_update()
        callback(*result)
    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def download_update(download_url, progress_callback=None):
    """
    Tải file .exe mới về thư mục tạm.
    progress_callback(downloaded_bytes, total_bytes) để báo tiến trình.
    Trả về: đường dẫn file đã tải hoặc None nếu lỗi.
    """
    try:
        req = urllib.request.Request(download_url, headers={
            "User-Agent": "ETA-Connect-Updater"
        })
        resp = urllib.request.urlopen(req, timeout=120)
        total = int(resp.headers.get("Content-Length", 0))

        # Lưu vào thư mục tạm cạnh file .exe hiện tại
        app_dir = get_app_dir()
        temp_path = os.path.join(app_dir, f"_update_{EXE_NAME}")

        downloaded = 0
        chunk_size = 65536  # 64KB

        with open(temp_path, "wb") as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback and total > 0:
                    progress_callback(downloaded, total)

        return temp_path

    except Exception:
        return None


def download_update_async(download_url, progress_callback=None, done_callback=None):
    """Tải file trong background thread"""
    def _worker():
        path = download_update(download_url, progress_callback)
        if done_callback:
            done_callback(path)
    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def get_app_dir():
    """Lấy thư mục chứa file .exe đang chạy"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_current_exe():
    """Lấy đường dẫn file .exe đang chạy"""
    if getattr(sys, 'frozen', False):
        return sys.executable
    return None


def apply_update(new_exe_path):
    """
    Áp dụng cập nhật: đổi tên file cũ, chép file mới, khởi động lại.
    Sử dụng một batch script trung gian để tráo đổi file.
    """
    current_exe = get_current_exe()
    if not current_exe:
        # Đang chạy từ Python script, không phải .exe
        return False

    app_dir = get_app_dir()
    old_exe = os.path.join(app_dir, f"_old_{EXE_NAME}")
    batch_path = os.path.join(app_dir, "_updater.bat")

    # Tạo batch script để thực hiện tráo đổi sau khi app tắt
    batch_content = f'''@echo off
echo Dang cap nhat ETA Connect...
timeout /t 2 /nobreak > nul

REM Xoa file cu neu con ton tai
if exist "{old_exe}" del /f "{old_exe}"

REM Doi ten file hien tai thanh _old
rename "{current_exe}" "_old_{EXE_NAME}"

REM Di chuyen file moi thanh ten chinh
move /y "{new_exe_path}" "{current_exe}"

REM Khoi dong lai app
start "" "{current_exe}"

REM Xoa file cu va chinh batch nay
timeout /t 3 /nobreak > nul
if exist "{old_exe}" del /f "{old_exe}"
del /f "%~f0"
'''
    with open(batch_path, "w", encoding="utf-8") as f:
        f.write(batch_content)

    # Chạy batch script và thoát app
    subprocess.Popen(
        ["cmd", "/c", batch_path],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    sys.exit(0)
