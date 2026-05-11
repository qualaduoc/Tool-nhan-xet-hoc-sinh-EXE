# license_ui.py - Màn hình kích hoạt bản quyền
import customtkinter as ctk
from tkinter import messagebox
from license_manager import get_machine_id, verify_serial, save_license, check_license, deactivate_license


class ActivationScreen(ctk.CTkFrame):
    """Màn hình kích hoạt hiển thị trước khi vào app"""

    def __init__(self, parent, on_success):
        super().__init__(parent, fg_color="#1A1A2E")
        self.parent = parent
        self.on_success = on_success
        self.machine_id = get_machine_id()
        self._build()

    def _build(self):
        # Center container
        center = ctk.CTkFrame(self, fg_color="#16213E", corner_radius=16,
                              border_width=2, border_color="#E67E22", width=520, height=520)
        center.place(relx=0.5, rely=0.5, anchor="center")
        center.pack_propagate(False)

        # Logo / Title
        ctk.CTkLabel(center, text="📝", font=("Arial", 48)).pack(pady=(30, 5))
        ctk.CTkLabel(center, text="ETA CONNECT", font=("Arial", 22, "bold"),
                     text_color="#E67E22").pack()
        ctk.CTkLabel(center, text="Nhận Xét Học Sinh Tự Động", font=("Arial", 13),
                     text_color="#AAB7C4").pack(pady=(0, 20))

        # Separator
        ctk.CTkFrame(center, height=1, fg_color="#0F3460").pack(fill="x", padx=40)

        # Mã máy
        ctk.CTkLabel(center, text="MÃ MÁY CỦA BẠN", font=("Arial", 11, "bold"),
                     text_color="#AAB7C4").pack(pady=(20, 5))

        mid_frame = ctk.CTkFrame(center, fg_color="#0F3460", corner_radius=8)
        mid_frame.pack(padx=40, fill="x")

        mid_row = ctk.CTkFrame(mid_frame, fg_color="transparent")
        mid_row.pack(fill="x", padx=10, pady=8)

        self.mid_label = ctk.CTkLabel(mid_row, text=self.machine_id,
                                       font=("Consolas", 20, "bold"), text_color="#2ECC71")
        self.mid_label.pack(side="left", expand=True)

        ctk.CTkButton(mid_row, text="📋 Copy", width=70, height=30,
                       fg_color="#E67E22", hover_color="#F39C12",
                       font=("Arial", 11), command=self._copy_mid).pack(side="right")

        # Hướng dẫn
        ctk.CTkLabel(center, text="📱 Hãy copy Mã Máy này gửi tới thầy Được\nđể kích hoạt phần mềm",
                     font=("Arial", 11), text_color="#F39C12",
                     justify="center").pack(pady=(8, 15))

        # Separator
        ctk.CTkFrame(center, height=1, fg_color="#0F3460").pack(fill="x", padx=40)

        # Nhập Serial
        ctk.CTkLabel(center, text="NHẬP SERIAL KEY", font=("Arial", 11, "bold"),
                     text_color="#AAB7C4").pack(pady=(15, 5))

        self.serial_entry = ctk.CTkEntry(center, placeholder_text="Nhập Serial Key nhận được...",
                                          font=("Consolas", 14), height=42,
                                          justify="center")
        self.serial_entry.pack(fill="x", padx=40)

        # Nút kích hoạt
        ctk.CTkButton(center, text="🔓 KÍCH HOẠT BẢN QUYỀN",
                       fg_color="#27AE60", hover_color="#2ECC71",
                       font=("Arial", 14, "bold"), height=42,
                       command=self._activate).pack(fill="x", padx=40, pady=(12, 5))

        # Trạng thái
        self.status_label = ctk.CTkLabel(center, text="", font=("Arial", 11),
                                          text_color="#E74C3C")
        self.status_label.pack(pady=(0, 5))

        # Footer
        ctk.CTkLabel(center, text="Liên hệ: 0904059866 — N.T.Được — ETA GROUP",
                     font=("Arial", 10), text_color="#7F8C8D").pack(pady=(5, 15))

    def _copy_mid(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.machine_id)
        self.status_label.configure(text="✅ Đã copy Mã Máy!", text_color="#2ECC71")
        self.after(2000, lambda: self.status_label.configure(text=""))

    def _activate(self):
        serial = self.serial_entry.get().strip()
        if not serial:
            self.status_label.configure(text="⚠ Vui lòng nhập Serial Key!", text_color="#F39C12")
            return

        valid, message, expiry = verify_serial(serial, self.machine_id)

        if valid:
            save_license(serial, self.machine_id)
            self.status_label.configure(text=f"✅ {message}", text_color="#2ECC71")
            messagebox.showinfo("Kích hoạt thành công!",
                                f"Chúc mừng! Phần mềm đã được kích hoạt.\n\n{message}")
            self.on_success()
        else:
            self.status_label.configure(text=f"❌ {message}", text_color="#E74C3C")


class LicenseInfoBar(ctk.CTkFrame):
    """Thanh hiển thị trạng thái license trong app chính"""

    def __init__(self, parent, on_deactivate=None):
        super().__init__(parent, height=28, fg_color="#1A5E1A", corner_radius=0)
        self.pack_propagate(False)
        self.on_deactivate = on_deactivate

        activated, msg, expiry = check_license()
        machine_id = get_machine_id()

        if activated:
            status = f"✅ Bản quyền: {expiry if expiry else 'Đã kích hoạt'}"
            ctk.CTkLabel(self, text=status, font=("Arial", 10, "bold"),
                         text_color="#82E0AA").pack(side="left", padx=10)
            ctk.CTkLabel(self, text=f"🖥 {machine_id}", font=("Consolas", 9),
                         text_color="#A9DFBF").pack(side="left", padx=10)

            if on_deactivate:
                ctk.CTkButton(self, text="Hủy kích hoạt", width=90, height=20,
                              font=("Arial", 9), fg_color="#C0392B", hover_color="#E74C3C",
                              command=self._deactivate).pack(side="right", padx=10)

    def _deactivate(self):
        if messagebox.askyesno("Xác nhận", "Hủy kích hoạt bản quyền?\nBạn sẽ cần nhập Serial mới."):
            deactivate_license()
            if self.on_deactivate:
                self.on_deactivate()
