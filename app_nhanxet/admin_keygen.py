# admin_keygen.py - Tool tạo Serial Key (CHỈ DÀNH CHO ADMIN - Khầy Được)
# Chạy: python admin_keygen.py
import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
from license_manager import generate_serial, verify_serial

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

KEYS_FILE = "admin_keys_db.json"

class KeyGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔑 ETA Connect — Quản Lý Bản Quyền (ADMIN)")
        self.geometry("900x650")
        self.minsize(750, 550)
        self.configure(fg_color="#1A1A2E")
        self.keys_db = self._load_db()
        self._build_ui()

    def _load_db(self):
        if os.path.exists(KEYS_FILE):
            try:
                with open(KEYS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_db(self):
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.keys_db, f, ensure_ascii=False, indent=2)

    def _build_ui(self):
        # Header
        hdr = ctk.CTkFrame(self, height=50, fg_color="#E67E22", corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="🔑 QUẢN LÝ BẢN QUYỀN — ETA CONNECT",
                     font=("Arial", 16, "bold"), text_color="white").pack(side="left", padx=20)
        ctk.CTkLabel(hdr, text="⚠ CHỈ DÀNH CHO ADMIN",
                     font=("Arial", 11), text_color="#FFF3E0").pack(side="right", padx=20)

        # Main 2 columns
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=2)
        main.grid_columnconfigure(1, weight=3)
        main.grid_rowconfigure(0, weight=1)

        # === LEFT: Tạo Key ===
        left = ctk.CTkFrame(main, fg_color="#16213E", corner_radius=12,
                            border_width=1, border_color="#0F3460")
        left.grid(row=0, column=0, sticky="nsew", padx=(0,8))

        ctk.CTkLabel(left, text="TẠO SERIAL KEY MỚI", font=("Arial", 14, "bold"),
                     text_color="#E67E22").pack(pady=(20,15), padx=20)

        # Mã máy input
        ctk.CTkLabel(left, text="Mã Máy khách hàng:", font=("Arial", 12),
                     text_color="#AAB7C4").pack(anchor="w", padx=20)
        self.machine_entry = ctk.CTkEntry(left, placeholder_text="VD: A1B2-C3D4-E5F6",
                                           font=("Consolas", 13), height=40)
        self.machine_entry.pack(fill="x", padx=20, pady=(3,10))

        # Tên khách hàng
        ctk.CTkLabel(left, text="Tên giáo viên:", font=("Arial", 12),
                     text_color="#AAB7C4").pack(anchor="w", padx=20)
        self.name_entry = ctk.CTkEntry(left, placeholder_text="VD: Cô Nguyễn Thị A",
                                       font=("Arial", 12), height=38)
        self.name_entry.pack(fill="x", padx=20, pady=(3,10))

        # Ghi chú
        ctk.CTkLabel(left, text="Ghi chú:", font=("Arial", 12),
                     text_color="#AAB7C4").pack(anchor="w", padx=20)
        self.note_entry = ctk.CTkEntry(left, placeholder_text="VD: Trường TH ABC",
                                       font=("Arial", 12), height=38)
        self.note_entry.pack(fill="x", padx=20, pady=(3,15))

        # Thời hạn
        ctk.CTkLabel(left, text="Thời hạn sử dụng:", font=("Arial", 12),
                     text_color="#AAB7C4").pack(anchor="w", padx=20)
        self.duration_var = ctk.StringVar(value="Vĩnh viễn")
        dur_frame = ctk.CTkFrame(left, fg_color="transparent")
        dur_frame.pack(fill="x", padx=20, pady=(3,15))
        ctk.CTkRadioButton(dur_frame, text="Vĩnh viễn", variable=self.duration_var,
                           value="Vĩnh viễn", font=("Arial", 12),
                           text_color="white", fg_color="#E67E22").pack(side="left", padx=(0,20))
        ctk.CTkRadioButton(dur_frame, text="Một năm (365 ngày)", variable=self.duration_var,
                           value="Một năm", font=("Arial", 12),
                           text_color="white", fg_color="#E67E22").pack(side="left")

        # Nút tạo
        ctk.CTkButton(left, text="🔑 TẠO SERIAL KEY", fg_color="#E67E22",
                       hover_color="#F39C12", font=("Arial", 14, "bold"),
                       height=45, command=self._generate).pack(fill="x", padx=20, pady=(5,10))

        # Kết quả
        ctk.CTkLabel(left, text="Serial Key được tạo:", font=("Arial", 11),
                     text_color="#AAB7C4").pack(anchor="w", padx=20)
        self.result_box = ctk.CTkTextbox(left, height=60, fg_color="#0F3460",
                                          text_color="#2ECC71", font=("Consolas", 12),
                                          corner_radius=8)
        self.result_box.pack(fill="x", padx=20, pady=(3,5))

        ctk.CTkButton(left, text="📋 Copy Serial", fg_color="#27AE60",
                       hover_color="#2ECC71", height=32,
                       command=self._copy_serial).pack(fill="x", padx=20, pady=(0,20))

        # === RIGHT: Danh sách Key ===
        right = ctk.CTkFrame(main, fg_color="#16213E", corner_radius=12,
                             border_width=1, border_color="#0F3460")
        right.grid(row=0, column=1, sticky="nsew", padx=(8,0))

        right_hdr = ctk.CTkFrame(right, fg_color="transparent")
        right_hdr.pack(fill="x", padx=20, pady=(15,10))
        ctk.CTkLabel(right_hdr, text="📋 DANH SÁCH KEY ĐÃ CẤP",
                     font=("Arial", 14, "bold"), text_color="#E67E22").pack(side="left")
        self.count_lbl = ctk.CTkLabel(right_hdr, text=f"Tổng: {len(self.keys_db)}",
                                      font=("Arial", 11), text_color="#82E0AA")
        self.count_lbl.pack(side="right")

        # List
        self.list_frame = ctk.CTkScrollableFrame(right, fg_color="#0F3460", corner_radius=8)
        self.list_frame.pack(fill="both", expand=True, padx=15, pady=(0,10))

        # Bottom actions
        bot = ctk.CTkFrame(right, fg_color="transparent")
        bot.pack(fill="x", padx=15, pady=(0,15))
        ctk.CTkButton(bot, text="🗑 Xóa key đã chọn", fg_color="#E74C3C",
                       hover_color="#C0392B", height=32,
                       command=self._delete_selected).pack(side="right", padx=5)

        self._render_list()

    def _generate(self):
        machine_id = self.machine_entry.get().strip()
        if not machine_id or len(machine_id.replace("-", "")) < 8:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã Máy hợp lệ!")
            return

        duration = "1year" if self.duration_var.get() == "Một năm" else "forever"
        serial = generate_serial(machine_id, duration)

        # Lưu vào DB
        record = {
            "machine_id": machine_id.upper(),
            "serial": serial,
            "name": self.name_entry.get().strip() or "Chưa rõ",
            "note": self.note_entry.get().strip() or "",
            "duration": self.duration_var.get(),
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "status": "active",
        }
        self.keys_db.append(record)
        self._save_db()

        # Hiển thị
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", serial)

        self._render_list()
        messagebox.showinfo("Thành công", f"Đã tạo Serial Key!\n\n{serial}\n\nGửi key này cho giáo viên.")

    def _copy_serial(self):
        serial = self.result_box.get("1.0", "end").strip()
        if serial:
            self.clipboard_clear()
            self.clipboard_append(serial)
            messagebox.showinfo("Đã copy", "Serial Key đã được copy vào clipboard!")

    def _render_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        self.count_lbl.configure(text=f"Tổng: {len(self.keys_db)}")
        self._selected_idx = None

        if not self.keys_db:
            ctk.CTkLabel(self.list_frame, text="Chưa có key nào được tạo.",
                         font=("Arial", 12), text_color="#7F8C8D").pack(pady=30)
            return

        for i, rec in enumerate(reversed(self.keys_db)):
            idx = len(self.keys_db) - 1 - i
            dur_color = "#27AE60" if rec["duration"] == "Vĩnh viễn" else "#3498DB"
            status_text = "✅ Active" if rec.get("status") == "active" else "❌ Hủy"

            card = ctk.CTkFrame(self.list_frame, fg_color="#1A1A2E", corner_radius=6,
                                border_width=1, border_color="#2C3E50")
            card.pack(fill="x", pady=3)

            # Row 1: Name + Duration
            r1 = ctk.CTkFrame(card, fg_color="transparent")
            r1.pack(fill="x", padx=10, pady=(8,2))
            ctk.CTkLabel(r1, text=f"👤 {rec['name']}", font=("Arial", 11, "bold"),
                         text_color="white").pack(side="left")
            ctk.CTkLabel(r1, text=rec["duration"], font=("Arial", 10, "bold"),
                         text_color=dur_color).pack(side="right")

            # Row 2: Machine ID + Date
            r2 = ctk.CTkFrame(card, fg_color="transparent")
            r2.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(r2, text=f"🖥 {rec['machine_id']}", font=("Consolas", 10),
                         text_color="#AAB7C4").pack(side="left")
            ctk.CTkLabel(r2, text=rec["created_at"], font=("Arial", 9),
                         text_color="#7F8C8D").pack(side="right")

            # Row 3: Serial
            r3 = ctk.CTkFrame(card, fg_color="#0F3460", corner_radius=4)
            r3.pack(fill="x", padx=10, pady=(2,5))
            ctk.CTkLabel(r3, text=f"🔑 {rec['serial']}", font=("Consolas", 9),
                         text_color="#F39C12").pack(padx=8, pady=4, anchor="w")

            # Copy + Delete buttons
            r4 = ctk.CTkFrame(card, fg_color="transparent")
            r4.pack(fill="x", padx=10, pady=(0,6))
            ctk.CTkButton(r4, text="📋 Copy", width=60, height=24, font=("Arial", 10),
                          fg_color="#2C3E50", hover_color="#34495E",
                          command=lambda s=rec["serial"]: self._copy_key(s)).pack(side="left", padx=(0,5))
            ctk.CTkButton(r4, text="🗑 Xóa", width=60, height=24, font=("Arial", 10),
                          fg_color="#E74C3C", hover_color="#C0392B",
                          command=lambda i=idx: self._delete_key(i)).pack(side="left")

    def _copy_key(self, serial):
        self.clipboard_clear()
        self.clipboard_append(serial)

    def _delete_key(self, idx):
        if messagebox.askyesno("Xác nhận", "Xóa key này khỏi danh sách?"):
            self.keys_db.pop(idx)
            self._save_db()
            self._render_list()

    def _delete_selected(self):
        pass  # Handled per-item


if __name__ == "__main__":
    app = KeyGenApp()
    app.mainloop()
