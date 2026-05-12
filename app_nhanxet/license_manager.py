# license_manager.py - Hệ thống bản quyền dựa trên Mã Máy
import hashlib
import hmac
import json
import os
import platform
import subprocess
import base64
import time
from datetime import datetime, timedelta

# Secret key nội bộ (đổi trước khi build EXE!)
_SECRET = "ETA_CONNECT_2026_KHAY_DUOC_LICENSE"

# Đường dẫn cố định: thư mục chứa file EXE (không phải thư mục tạm _MEIxxx)
import sys
if getattr(sys, 'frozen', False):
    # Đang chạy từ EXE (PyInstaller) → dùng thư mục chứa EXE
    _APP_DIR = os.path.dirname(sys.executable)
else:
    # Đang chạy từ source code
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

_LICENSE_FILE = os.path.join(_APP_DIR, "license.dat")


def _run_wmic(cmd):
    """Chạy lệnh WMIC lấy thông tin phần cứng"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        )
        return result.stdout.strip()
    except Exception:
        return ""
_MACHINE_CACHE = os.path.join(_APP_DIR, "_machine_id.cache")


def get_machine_id():
    """Tạo Mã Máy duy nhất từ phần cứng (CPU + Motherboard + Disk)"""
    # Đọc cache trước (tránh chạy WMIC mỗi lần mở app)
    if os.path.exists(_MACHINE_CACHE):
        try:
            with open(_MACHINE_CACHE, "r") as f:
                cached = f.read().strip()
                if cached and len(cached) == 14:  # XXXX-XXXX-XXXX
                    return cached
        except Exception:
            pass

    parts = []

    # CPU ID
    cpu = _run_wmic(["wmic", "cpu", "get", "ProcessorId"])
    cpu_lines = [l.strip() for l in cpu.split("\n") if l.strip() and l.strip() != "ProcessorId"]
    if cpu_lines:
        parts.append(cpu_lines[0])

    # Motherboard Serial
    mb = _run_wmic(["wmic", "baseboard", "get", "SerialNumber"])
    mb_lines = [l.strip() for l in mb.split("\n") if l.strip() and l.strip() != "SerialNumber"]
    if mb_lines and mb_lines[0] not in ("", "To be filled by O.E.M.", "Default string"):
        parts.append(mb_lines[0])

    # Disk Serial (ổ cứng chính)
    disk = _run_wmic(["wmic", "diskdrive", "get", "SerialNumber"])
    disk_lines = [l.strip() for l in disk.split("\n") if l.strip() and l.strip() != "SerialNumber"]
    if disk_lines:
        parts.append(disk_lines[0])

    # Fallback: nếu không lấy được gì, dùng hostname + username
    if not parts:
        parts.append(platform.node())
        parts.append(os.getlogin())

    # Hash thành mã 12 ký tự dễ copy
    raw = "|".join(parts)
    h = hashlib.sha256((raw + _SECRET).encode()).hexdigest()
    machine_id = h[:12].upper()
    # Thêm dấu gạch ngang cho dễ đọc: XXXX-XXXX-XXXX
    result = f"{machine_id[:4]}-{machine_id[4:8]}-{machine_id[8:12]}"

    # Lưu cache
    try:
        with open(_MACHINE_CACHE, "w") as f:
            f.write(result)
    except Exception:
        pass

    return result


def generate_serial(machine_id, duration="forever"):
    """
    Tạo Serial Key cho 1 Mã Máy cụ thể.
    duration: "forever" hoặc "1year"
    Trả về serial dạng: XXXX-XXXX-XXXX-XXXX-XXXX
    """
    machine_id = machine_id.replace("-", "").strip().upper()

    if duration == "1year":
        expiry = (datetime.now() + timedelta(days=365)).strftime("%Y%m%d")
    else:
        expiry = "99991231"  # Vĩnh viễn

    # Payload: machine_id + expiry
    payload = f"{machine_id}:{expiry}"
    # HMAC signature
    sig = hmac.new(_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:8]
    # Encode payload + sig
    raw = f"{payload}:{sig}"
    encoded = base64.b32encode(raw.encode()).decode().replace("=", "")

    # Format thành nhóm 4 ký tự, dấu gạch ngang
    serial = "-".join([encoded[i:i+4] for i in range(0, len(encoded), 4)])
    return serial.upper()


def verify_serial(serial, machine_id):
    """
    Xác minh Serial Key có hợp lệ với Mã Máy hiện tại không.
    Trả về: (valid: bool, message: str, expiry_date: str|None)
    """
    try:
        machine_id_clean = machine_id.replace("-", "").strip().upper()
        serial_clean = serial.replace("-", "").strip().upper()

        # Thêm padding cho base32
        padding = (8 - len(serial_clean) % 8) % 8
        serial_padded = serial_clean + "=" * padding

        decoded = base64.b32decode(serial_padded).decode()
        parts = decoded.split(":")

        if len(parts) != 3:
            return False, "Serial không hợp lệ.", None

        s_machine, s_expiry, s_sig = parts

        # Kiểm tra mã máy
        if s_machine.upper() != machine_id_clean:
            return False, "Serial không khớp với Mã Máy này.\nSerial này thuộc về máy tính khác!", None

        # Kiểm tra chữ ký
        payload = f"{s_machine}:{s_expiry}"
        expected_sig = hmac.new(_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:8]
        if s_sig.lower() != expected_sig.lower():
            return False, "Serial bị giả mạo hoặc không hợp lệ.", None

        # Kiểm tra hạn sử dụng
        if s_expiry == "99991231":
            return True, "Bản quyền VĨNH VIỄN ✅", "Vĩnh viễn"
        else:
            expiry_date = datetime.strptime(s_expiry, "%Y%m%d")
            if datetime.now() > expiry_date:
                return False, f"Serial đã hết hạn từ {expiry_date.strftime('%d/%m/%Y')}.", None
            days_left = (expiry_date - datetime.now()).days
            return True, f"Bản quyền hợp lệ đến {expiry_date.strftime('%d/%m/%Y')} ({days_left} ngày còn lại) ✅", expiry_date.strftime('%d/%m/%Y')

    except Exception as e:
        return False, f"Lỗi xác minh: {str(e)}", None


def save_license(serial, machine_id):
    """Lưu license đã kích hoạt vào file mã hóa"""
    data = {
        "serial": serial,
        "machine_id": machine_id,
        "activated_at": datetime.now().isoformat(),
    }
    raw = json.dumps(data)
    # Mã hóa đơn giản bằng XOR + base64
    key = hashlib.sha256(_SECRET.encode()).digest()
    encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(raw.encode())])
    encoded = base64.b64encode(encrypted).decode()

    with open(_LICENSE_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)


def load_license():
    """Đọc license đã lưu. Trả về (serial, machine_id) hoặc (None, None)"""
    if not os.path.exists(_LICENSE_FILE):
        return None, None
    try:
        with open(_LICENSE_FILE, "r", encoding="utf-8") as f:
            encoded = f.read().strip()
        encrypted = base64.b64decode(encoded)
        key = hashlib.sha256(_SECRET.encode()).digest()
        decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted)])
        data = json.loads(decrypted.decode())
        return data.get("serial"), data.get("machine_id")
    except Exception:
        return None, None


def check_license():
    """
    Kiểm tra bản quyền tổng thể.
    Trả về: (activated: bool, message: str, expiry: str|None)
    """
    current_machine = get_machine_id()
    saved_serial, saved_machine = load_license()

    if not saved_serial:
        return False, "Chưa kích hoạt bản quyền.", None

    # Kiểm tra mã máy trong license có khớp máy hiện tại không
    if saved_machine != current_machine:
        return False, "License không khớp máy tính này.\nFile license thuộc về máy khác!", None

    return verify_serial(saved_serial, current_machine)


def deactivate_license():
    """Hủy kích hoạt (xóa file license)"""
    if os.path.exists(_LICENSE_FILE):
        os.remove(_LICENSE_FILE)
        return True
    return False
