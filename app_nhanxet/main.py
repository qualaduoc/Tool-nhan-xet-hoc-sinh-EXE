# main.py - Giao diện chính App Nhận Xét Học Sinh ETA Connect
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from comment_data import CommentBank
from excel_processor import ExcelProcessor
from config_ui import ConfigWindow
from license_manager import check_license
from license_ui import ActivationScreen, LicenseInfoBar
from auto_updater import check_for_update_async, download_update_async, apply_update, get_current_version
from vnedu_processor import VneduProcessor, load_settings as vnedu_load_settings, save_settings as vnedu_save_settings, score_to_level

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Mapping hiển thị tiếng Việt
CAP_DISPLAY = {"tieu_hoc": "Tiểu Học", "thcs": "Trung Học Cơ Sở"}
CAP_REVERSE = {"Tiểu Học": "tieu_hoc", "Trung Học Cơ Sở": "thcs"}

ACCENT = "#E67E22"
ACCENT_HOVER = "#F39C12"
BG_MAIN = "#F5F0E8"
BG_CARD = "#FFFFFF"
BG_SIDEBAR = "#FFF0E0"
TEXT_DARK = "#2C3E50"
TEXT_MID = "#666666"
SUCCESS = "#27AE60"
DANGER = "#E74C3C"


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"[ ETA Connect — Nhận Xét Học Sinh Tự Động v{get_current_version()} ]")
        self.geometry("1050x700")
        self.minsize(800, 550)
        self.configure(fg_color=BG_MAIN)

        self.cb = CommentBank()
        self.processor = ExcelProcessor()
        self.vnedu = VneduProcessor()
        self.loaded_file = None
        self.vnedu_loaded_file = None
        self.config_win = None

        # Thiết lập style hiện đại cho ttk.Treeview
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
                             background="#FFFFFF",
                             foreground="#34495E",
                             rowheight=28,
                             fieldbackground="#FFFFFF",
                             font=("Arial", 10),
                             borderwidth=0)
        self.style.configure("Treeview.Heading",
                             background="#F2F3F4",
                             foreground="#2C3E50",
                             font=("Arial", 10, "bold"),
                             borderwidth=0,
                             relief="flat")
        self.style.map("Treeview",
                       background=[("selected", "#D6EAF8")],
                       foreground=[("selected", "#154360")])
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # Check license trước khi vào app
        activated, msg, expiry = check_license()
        if activated:
            self._build_ui()
        else:
            self._show_activation()

    def _show_activation(self):
        """Hiển thị màn hình kích hoạt bản quyền"""
        # Xóa mọi widget cũ
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color="#1A1A2E")
        screen = ActivationScreen(self, on_success=self._on_activated)
        screen.pack(fill="both", expand=True)

    def _on_activated(self):
        """Callback khi kích hoạt thành công → load app chính"""
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color=BG_MAIN)
        self._build_ui()

    def _build_ui(self):
        # === LICENSE BAR ===
        LicenseInfoBar(self, on_deactivate=self._show_activation).pack(fill="x")

        # === TOP BAR ===
        topbar = ctk.CTkFrame(self, height=55, fg_color=ACCENT, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="📝 ETA CONNECT — NHẬN XÉT HỌC SINH TỰ ĐỘNG",
                     font=("Arial", 16, "bold"), text_color="white").pack(side="left", padx=20)

        # Nút cập nhật (ẩn, chỉ hiện khi có bản mới)
        self._update_info = None
        self.update_btn = ctk.CTkButton(topbar, text="", width=0, height=30,
                                         fg_color="transparent", hover_color="#D35400",
                                         font=("Arial", 11, "bold"), text_color="#FFFFFF",
                                         corner_radius=15, command=self._on_update_click)
        # Chưa pack — chỉ pack khi phát hiện bản mới

        ctk.CTkLabel(topbar, text=f"v{get_current_version()} | Khầy Được — ETA GROUP",
                     font=("Arial", 11), text_color="#FFE0B2").pack(side="right", padx=20)

        # Kiểm tra cập nhật ngầm
        self._blink_state = True
        check_for_update_async(self._on_update_check_done)

        # === NAVBAR ===
        navbar = ctk.CTkFrame(self, height=40, fg_color="#34495E", corner_radius=0)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        self._active_page = "csdl"
        self.nav_btn_csdl = ctk.CTkButton(navbar, text="📋 CSDL Ngành", width=160, height=34,
                                            fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                            font=("Arial", 13, "bold"), corner_radius=6,
                                            command=lambda: self._switch_page("csdl"))
        self.nav_btn_csdl.pack(side="left", padx=(15,5), pady=3)
        self.nav_btn_vnedu = ctk.CTkButton(navbar, text="🌐 VNEDU", width=160, height=34,
                                            fg_color="transparent", hover_color="#4A6FA5",
                                            font=("Arial", 13, "bold"), corner_radius=6,
                                            text_color="#AAB7C4",
                                            command=lambda: self._switch_page("vnedu"))
        self.nav_btn_vnedu.pack(side="left", padx=5, pady=3)

        # === CONTENT CONTAINER ===
        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content.pack(fill="both", expand=True)

        # Tạo 2 trang
        self.page_csdl = ctk.CTkFrame(self.content, fg_color=BG_MAIN, corner_radius=0)
        self.page_vnedu = ctk.CTkFrame(self.content, fg_color=BG_MAIN, corner_radius=0)
        self._build_page_csdl(self.page_csdl)
        self._build_page_vnedu(self.page_vnedu)

        # Hiện trang mặc định
        self.page_csdl.pack(fill="both", expand=True)

        # === BOTTOM BAR ===
        bottom = ctk.CTkFrame(self, height=30, fg_color="#2C3E50", corner_radius=0)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        ctk.CTkLabel(bottom, text=f"ETA Connect v{get_current_version()} © 2026 | Phát triển bởi Khầy Được — ETA GROUP",
                     font=("Arial", 10), text_color="#95A5A6").pack(expand=True)

    def _switch_page(self, page_name):
        """Chuyển giữa trang CSDL Ngành và VNEDU"""
        if page_name == self._active_page:
            return
        self._active_page = page_name

        self.page_csdl.pack_forget()
        self.page_vnedu.pack_forget()

        if page_name == "csdl":
            self.nav_btn_csdl.configure(fg_color=ACCENT, text_color="white")
            self.nav_btn_vnedu.configure(fg_color="transparent", text_color="#AAB7C4")
            self.page_csdl.pack(fill="both", expand=True)
        else:
            self.nav_btn_vnedu.configure(fg_color="#3498DB", text_color="white")
            self.nav_btn_csdl.configure(fg_color="transparent", text_color="#AAB7C4")
            self.page_vnedu.pack(fill="both", expand=True)

    def _build_page_csdl(self, parent):
        """Xây dựng trang CSDL Ngành (nội dung hiện tại)"""

        # === MAIN LAYOUT: PanedWindow cho co giãn tối ưu ===
        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10,5))

        # === LEFT: Upload & Process (scrollable) ===
        left_wrapper = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                                     border_width=1, border_color="#E0D5C5")
        paned.add(left_wrapper, minsize=380, stretch="always")

        left = ctk.CTkScrollableFrame(left_wrapper, fg_color=BG_CARD, corner_radius=0)
        left.pack(fill="both", expand=True)

        # Section 1: Upload
        s1 = ctk.CTkFrame(left, fg_color="transparent")
        s1.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(s1, text="1. TẢI FILE EXCEL", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="Chọn file .xlsx từ máy tính (file đánh giá học sinh).",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))

        btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(btn_row, text="📂 Chọn File Excel...", fg_color="#FFFFFF",
                       text_color=ACCENT, border_width=1, border_color=ACCENT,
                       hover_color="#FDEBD0", font=("Arial", 12, "bold"),
                       height=36, width=160, command=self._open_file).pack(side="left", padx=(0,10))
        ctk.CTkButton(btn_row, text="⚙ Cấu Hình Lời Nhận Xét", fg_color="#2C3E50",
                       hover_color="#34495E", font=("Arial", 11),
                       height=36, width=160, command=self._open_config).pack(side="left")

        self.file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"),
                                       text_color=TEXT_MID)
        self.file_label.pack(anchor="w", pady=(8,0))

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=5)

        # Section 2: File info
        s2 = ctk.CTkFrame(left, fg_color="transparent")
        s2.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s2, text="2. THÔNG TIN FILE", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        self.info_frame = ctk.CTkFrame(s2, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=6)
        self.info_frame.pack(fill="x", pady=(5,0))
        self.info_label = ctk.CTkLabel(self.info_frame, text="Tải file để xem thông tin...",
                                       font=("Arial", 11), text_color=TEXT_MID, wraplength=350,
                                       justify="left")
        self.info_label.pack(padx=12, pady=10, anchor="w")

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=10)

        # Section 3: Settings
        s3 = ctk.CTkFrame(left, fg_color="transparent")
        s3.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s3, text="3. CẤU HÌNH XỬ LÝ", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        opt_frame = ctk.CTkFrame(s3, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=6)
        opt_frame.pack(fill="x", pady=8)

        ctk.CTkLabel(opt_frame, text="Chọn Cấp Học:", font=("Arial", 11, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(10,2))
        self.cap_display_var = ctk.StringVar(value="Tiểu Học")
        cap_menu = ctk.CTkSegmentedButton(opt_frame, values=["Tiểu Học", "Trung Học Cơ Sở"],
                                           variable=self.cap_display_var,
                                           font=("Arial", 11),
                                           selected_color=ACCENT, selected_hover_color=ACCENT_HOVER)
        cap_menu.pack(padx=12, pady=(0,8), fill="x")

        self.overwrite_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opt_frame, text="Ghi đè ô nhận xét đã có sẵn",
                        variable=self.overwrite_var, font=("Arial", 11),
                        text_color=TEXT_DARK, fg_color=ACCENT,
                        hover_color=ACCENT_HOVER).pack(anchor="w", padx=12, pady=(0,10))

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=5)

        # Section 4: Actions
        s4 = ctk.CTkFrame(left, fg_color="transparent")
        s4.pack(fill="x", padx=20, pady=(10,15))
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))

        action_frame = ctk.CTkFrame(s4, fg_color="transparent")
        action_frame.pack(fill="x")

        self.run_btn = ctk.CTkButton(action_frame, text="🚀 ĐIỀN NHẬN XÉT TỰ ĐỘNG",
                                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                      font=("Arial", 12, "bold"), height=40,
                                      command=self._run_process, state="disabled")
        self.run_btn.pack(fill="x", pady=(0,8))

        self.export_btn = ctk.CTkButton(action_frame, text="💾 XUẤT FILE KẾT QUẢ",
                                         fg_color=SUCCESS, hover_color="#219A52",
                                         font=("Arial", 12, "bold"), height=40,
                                         command=self._export_file, state="disabled")
        self.export_btn.pack(fill="x")

        # === RIGHT: Preview & Log ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")

        # Title bar cho preview
        preview_header = ctk.CTkFrame(right, fg_color="#2C3E50", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12,0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 XEM TRƯỚC DỮ LIỆU",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        self.preview_stats = ctk.CTkLabel(preview_header, text="",
                                          font=("Arial", 10), text_color="#82E0AA")
        self.preview_stats.pack(side="right", padx=15)

        # Sheet tabs container
        self.sheet_tabs_frame = ctk.CTkFrame(right, fg_color="#ECF0F1", corner_radius=0, height=35)
        self.sheet_tabs_frame.pack(fill="x", padx=12)
        self.sheet_tabs_frame.pack_propagate(False)
        self._current_sheets = []
        self._current_sheet_idx = 0

        # Preview
        self.preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        self.preview_frame.pack(fill="both", expand=True, padx=12, pady=(0,5))

        # Placeholder khi chưa có file
        self.preview_placeholder = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.preview_placeholder.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(self.preview_placeholder, text="📂",
                     font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(self.preview_placeholder, text="Tải file Excel để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10,0))
        ctk.CTkLabel(self.preview_placeholder, text="Hỗ trợ file .xlsx đánh giá học sinh",
                     font=("Arial", 11), text_color="#BDC3C7").pack()

        # Biến để giữ widget Treeview
        self.preview_tree = None

        # Log section
        log_header = ctk.CTkFrame(right, fg_color="#2C3E50", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5,0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ XỬ LÝ",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)

        self.log_box = ctk.CTkTextbox(right, height=120, fg_color="#1A252F", text_color="#2ECC71",
                                      font=("Consolas", 11), corner_radius=0,
                                      border_width=1, border_color="#34495E")
        self.log_box.pack(fill="x", padx=12, pady=(0,12))
        self._log("Ứng dụng sẵn sàng. Hãy tải file Excel để bắt đầu!")

    def _build_page_vnedu(self, parent):
        """Xây dựng trang VNEDU"""
        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10,5))

        # === LEFT: Upload & Cấu hình ===
        left_wrapper = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                                     border_width=1, border_color="#E0D5C5")
        paned.add(left_wrapper, minsize=380, stretch="always")
        left = ctk.CTkScrollableFrame(left_wrapper, fg_color=BG_CARD, corner_radius=0)
        left.pack(fill="both", expand=True)

        # Section 1: Upload file VNEDU
        s1 = ctk.CTkFrame(left, fg_color="transparent")
        s1.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(s1, text="1. TẢI FILE VNEDU", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="Chọn file .xlsx xuất từ hệ thống quản lý điểm VNEDU.",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))

        btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(btn_row, text="📂 Chọn File VNEDU...", fg_color="#FFFFFF",
                       text_color="#3498DB", border_width=1, border_color="#3498DB",
                       hover_color="#EBF5FB", font=("Arial", 12, "bold"),
                       height=36, width=180, command=self._vnedu_open_file).pack(side="left")

        self.vnedu_file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"),
                                              text_color=TEXT_MID)
        self.vnedu_file_label.pack(anchor="w", pady=(8,0))

        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=5)

        # Section 2: Thông tin
        s2 = ctk.CTkFrame(left, fg_color="transparent")
        s2.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s2, text="2. THÔNG TIN FILE", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        self.vnedu_info_frame = ctk.CTkFrame(s2, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=6)
        self.vnedu_info_frame.pack(fill="x", pady=(5,0))
        self.vnedu_info_label = ctk.CTkLabel(self.vnedu_info_frame, text="Vui lòng tải file để xem thông tin lớp...",
                                              font=("Arial", 11), text_color=TEXT_MID,
                                              wraplength=350, justify="left")
        self.vnedu_info_label.pack(padx=12, pady=10, anchor="w")

        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=10)

        # Section 3: Cấu hình ngưỡng điểm
        s3 = ctk.CTkFrame(left, fg_color="transparent")
        s3.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s3, text="3. CẤU HÌNH NGƯỠNG ĐIỂM", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        score_frame = ctk.CTkFrame(s3, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=6)
        score_frame.pack(fill="x", pady=8)

        settings = vnedu_load_settings()

        # T (Hoàn thành tốt)
        r1 = ctk.CTkFrame(score_frame, fg_color="transparent")
        r1.pack(fill="x", padx=12, pady=(10,3))
        ctk.CTkLabel(r1, text="T (Hoàn thành tốt):", font=("Arial", 11, "bold"),
                     text_color="#27AE60", width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(r1, text="từ", font=("Arial", 11), text_color=TEXT_MID).pack(side="left", padx=(5,5))
        self.vnedu_t_min = ctk.CTkEntry(r1, width=45, height=26, font=("Arial", 12), justify="center", border_width=1)
        self.vnedu_t_min.insert(0, str(settings.get("score_T_min", 9)))
        self.vnedu_t_min.pack(side="left")

        # H (Hoàn thành)
        r2 = ctk.CTkFrame(score_frame, fg_color="transparent")
        r2.pack(fill="x", padx=12, pady=3)
        ctk.CTkLabel(r2, text="H (Hoàn thành):", font=("Arial", 11, "bold"),
                     text_color="#E67E22", width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(r2, text="từ", font=("Arial", 11), text_color=TEXT_MID).pack(side="left", padx=(5,5))
        self.vnedu_h_min = ctk.CTkEntry(r2, width=45, height=26, font=("Arial", 12), justify="center", border_width=1)
        self.vnedu_h_min.insert(0, str(settings.get("score_H_min", 5)))
        self.vnedu_h_min.pack(side="left")

        # C (Chưa HT)
        r3 = ctk.CTkFrame(score_frame, fg_color="transparent")
        r3.pack(fill="x", padx=12, pady=(3,8))
        ctk.CTkLabel(r3, text="C (Chưa HT):", font=("Arial", 11, "bold"),
                     text_color="#E74C3C", width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(r3, text="< ngưỡng H", font=("Arial", 11), text_color=TEXT_MID).pack(side="left", padx=5)

        ctk.CTkButton(score_frame, text="Lưu cấu hình", fg_color="#F2F4F4", text_color="#2C3E50",
                       hover_color="#E5E8E8", height=28, width=100, font=("Arial", 11),
                       command=self._vnedu_save_settings).pack(padx=12, pady=(0,10), anchor="e")

        ctk.CTkFrame(left, height=1, fg_color="#EAECEE").pack(fill="x", padx=20, pady=5)

        # Section 4: Actions
        s4 = ctk.CTkFrame(left, fg_color="transparent")
        s4.pack(fill="x", padx=20, pady=(10,15))
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))

        action_frame = ctk.CTkFrame(s4, fg_color="transparent")
        action_frame.pack(fill="x")
        
        self.vnedu_run_btn = ctk.CTkButton(action_frame, text="🚀 ĐIỀN MỨC ĐẠT ĐƯỢC",
                                            fg_color="#2C3E50", hover_color="#34495E",
                                            font=("Arial", 12, "bold"), height=40,
                                            command=self._vnedu_run, state="disabled")
        self.vnedu_run_btn.pack(fill="x", pady=(0,8))

        self.vnedu_export_btn = ctk.CTkButton(action_frame, text="💾 XUẤT FILE KẾT QUẢ",
                                               fg_color=SUCCESS, hover_color="#219A52",
                                               font=("Arial", 12, "bold"), height=40,
                                               command=self._vnedu_export, state="disabled")
        self.vnedu_export_btn.pack(fill="x")

        # === RIGHT: Preview & Log ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")

        # Preview header
        preview_header = ctk.CTkFrame(right, fg_color="#1A5276", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12,0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 XEM TRƯỚC DỮ LIỆU VNEDU",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        self.vnedu_preview_stats = ctk.CTkLabel(preview_header, text="",
                                                 font=("Arial", 10), text_color="#82E0AA")
        self.vnedu_preview_stats.pack(side="right", padx=15)

        # Preview
        self.vnedu_preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        self.vnedu_preview_frame.pack(fill="both", expand=True, padx=12, pady=(5,5))

        # Placeholder
        self.vnedu_ph = ctk.CTkFrame(self.vnedu_preview_frame, fg_color="transparent")
        self.vnedu_ph.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(self.vnedu_ph, text="🌐", font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(self.vnedu_ph, text="Tải file VNEDU để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10,0))
        
        self.vnedu_tree = None

        # Log VNEDU
        log_header = ctk.CTkFrame(right, fg_color="#1A5276", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5,0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ XỬ LÝ VNEDU",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)

        self.vnedu_log_box = ctk.CTkTextbox(right, height=120, fg_color="#1A252F",
                                             text_color="#5DADE2", font=("Consolas", 11),
                                             corner_radius=0, border_width=1, border_color="#34495E")
        self.vnedu_log_box.pack(fill="x", padx=12, pady=(0,12))
        self._vnedu_log("Chọn file VNEDU (.xlsx) để bắt đầu!")

    # =======================================
    # VNEDU METHODS
    # =======================================
    def _vnedu_log(self, text):
        self.vnedu_log_box.insert("end", f"→ {text}\n")
        self.vnedu_log_box.see("end")

    def _vnedu_save_settings(self):
        """Lưu cấu hình ngưỡng điểm VNEDU"""
        try:
            t_min = float(self.vnedu_t_min.get())
            h_min = float(self.vnedu_h_min.get())
            if h_min >= t_min:
                messagebox.showwarning("Lỗi", "Ngưỡng H phải nhỏ hơn ngưỡng T!")
                return
            settings = {"score_T_min": t_min, "score_H_min": h_min}
            vnedu_save_settings(settings)
            self.vnedu.settings = settings
            self._vnedu_log(f"💾 Đã lưu: T ≥ {t_min}, H ≥ {h_min}, C < {h_min}")
            messagebox.showinfo("Đã lưu", f"Cấu hình ngưỡng điểm đã được lưu!\n\nT (Hoàn thành tốt): ≥ {t_min}\nH (Hoàn thành): ≥ {h_min}\nC (Chưa hoàn thành): < {h_min}")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

    def _vnedu_open_file(self):
        """Mở file VNEDU"""
        filepath = filedialog.askopenfilename(
            title="Chọn file Excel VNEDU",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return

        self.vnedu_loaded_file = filepath
        filename = os.path.basename(filepath)
        self.vnedu_file_label.configure(text=f"✅ {filename}", text_color=SUCCESS)
        self._vnedu_log(f"Đã tải: {filename}")

        try:
            info = self.vnedu.load_file(filepath)
            info_text = f"Trường: {info.get('school', 'N/A')}\n"
            info_text += f"{info.get('class', '')}\n"
            info_text += f"{info.get('year', '')}\n"
            info_text += f"Tổng số học sinh: {info.get('total_students', 0)}"
            self.vnedu_info_label.configure(text=info_text, text_color=TEXT_DARK)
            self.vnedu_preview_stats.configure(text=f"📊 {info.get('total_students', 0)} học sinh")

            # Preview
            self._vnedu_show_preview()
            self.vnedu_run_btn.configure(state="normal")
            self._vnedu_log(f"Sẵn sàng! {info.get('total_students', 0)} học sinh.")

        except Exception as e:
            self._vnedu_log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đọc file VNEDU:\n{str(e)}")

    def _vnedu_show_preview(self):
        """Hiển thị preview file VNEDU sử dụng Treeview để tối ưu hiệu năng"""
        # Xóa các widget hiện tại trong frame
        for w in self.vnedu_preview_frame.winfo_children():
            w.destroy()

        data = self.vnedu.get_preview_data(max_rows=100) # Cho phép hiện nhiều hơn vì Treeview rất nhẹ
        if not data:
            return

        headers = data["headers"]
        rows = data["rows"]

        # Chọn cột quan trọng (STT, Tên, Mức đạt được, Điểm)
        key_cols = []
        for j, h in enumerate(headers):
            if j < 4 or "Mức" in h or "Điểm" in h or j >= 25:
                key_cols.append((j, h))
        key_cols = key_cols[:15]  # Tối đa 15 cột để không quá chật

        col_ids = [str(i) for i in range(len(key_cols))]
        
        # Setup Treeview
        self.vnedu_tree = ttk.Treeview(self.vnedu_preview_frame, columns=col_ids, show="headings", style="Treeview")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(self.vnedu_preview_frame, orient="vertical", command=self.vnedu_tree.yview)
        x_scroll = ttk.Scrollbar(self.vnedu_preview_frame, orient="horizontal", command=self.vnedu_tree.xview)
        self.vnedu_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.vnedu_tree.pack(fill="both", expand=True)

        # Cấu hình Columns & Headings
        for i, (orig_j, h_text) in enumerate(key_cols):
            self.vnedu_tree.heading(str(i), text=h_text[:20])
            width = 150 if i == 2 else 70 # Cột Tên (index 2) rộng hơn
            self.vnedu_tree.column(str(i), width=width, minwidth=50, anchor="center")

        # Thêm Data
        for row in rows:
            display_row = []
            for (orig_j, _) in key_cols:
                val = row[orig_j] if orig_j < len(row) else ""
                display_row.append(val[:30])
            self.vnedu_tree.insert("", "end", values=display_row)

        # Row count
        valid_rows = sum(1 for r in rows if any(r))
        ctk.CTkLabel(self.vnedu_preview_frame, text=f"Hiển thị {valid_rows} dòng dữ liệu mẫu",
                     font=("Arial", 10), text_color="#7F8C8D").pack(anchor="e", padx=5, pady=(2,0))

    def _vnedu_run(self):
        """Chạy xử lý VNEDU: điền mức đạt được"""
        if not self.vnedu_loaded_file:
            messagebox.showwarning("Chưa có file", "Vui lòng tải file VNEDU trước!")
            return

        # Cập nhật settings từ UI
        try:
            t_min = float(self.vnedu_t_min.get())
            h_min = float(self.vnedu_h_min.get())
            self.vnedu.settings = {"score_T_min": t_min, "score_H_min": h_min}
        except ValueError:
            pass

        self._vnedu_log("Bắt đầu điền mức đạt được...")
        try:
            stats = self.vnedu.process()
            self._vnedu_log(f"✅ Hoàn tất! {stats['total']} học sinh")
            self._vnedu_log(f"   Đã điền: {stats['filled']} ô mức đạt được")
            self._vnedu_log(f"   Bỏ qua (đã có): {stats['skipped']} ô")

            for detail in stats.get("details", [])[:10]:
                self._vnedu_log(f"   {detail}")

            self.vnedu_export_btn.configure(state="normal")

            # Cập nhật preview
            self._vnedu_show_preview()
            messagebox.showinfo("Thành công",
                f"Đã điền mức đạt được tự động!\n\n"
                f"• Tổng: {stats['total']} học sinh\n"
                f"• Đã điền: {stats['filled']} ô\n"
                f"• Bỏ qua: {stats['skipped']} ô\n\n"
                f"Nhấn 'XUẤT FILE' để lưu kết quả.")

        except Exception as e:
            self._vnedu_log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi xử lý:\n{str(e)}")

    def _vnedu_export(self):
        """Xuất file VNEDU đã xử lý"""
        if not self.vnedu.wb:
            return

        default_name = os.path.splitext(os.path.basename(self.vnedu_loaded_file))[0] + "_DA_XU_LY.xlsx"
        output_path = filedialog.asksaveasfilename(
            title="Lưu file VNEDU kết quả",
            defaultextension=".xlsx",
            initialfile=default_name,
            filetypes=[("Excel files", "*.xlsx")]
        )
        if output_path:
            try:
                self.vnedu.save_output(output_path)
                self._vnedu_log(f"💾 Đã xuất: {os.path.basename(output_path)}")
                messagebox.showinfo("Thành công", f"Đã xuất file thành công!\n{output_path}")
            except Exception as e:
                self._vnedu_log(f"LỖI xuất: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể lưu:\n{str(e)}")

    # === COLOR MAP cho mức đánh giá ===
    LEVEL_COLORS = {
        "T": ("#27AE60", "#E8F8F5"),   # Tốt → xanh lá
        "T ": ("#27AE60", "#E8F8F5"),
        "H": ("#E67E22", "#FEF5E7"),   # Hoàn thành → cam
        "H ": ("#E67E22", "#FEF5E7"),
        "Đ": ("#E67E22", "#FEF5E7"),   # Đạt → cam
        "Đ ": ("#E67E22", "#FEF5E7"),
        "C": ("#E74C3C", "#FDEDEC"),   # Chưa HT → đỏ
        "C ": ("#E74C3C", "#FDEDEC"),
        "XS": ("#8E44AD", "#F5EEF8"),  # Xuất sắc → tím
        "K": ("#2980B9", "#EBF5FB"),   # Khá → xanh dương
        "G": ("#27AE60", "#E8F8F5"),   # Giỏi → xanh
        "TB": ("#F39C12", "#FEF9E7"),  # Trung bình → vàng
        "Y": ("#E74C3C", "#FDEDEC"),   # Yếu → đỏ
    }

    def _log(self, text):
        self.log_box.insert("end", f"→ {text}\n")
        self.log_box.see("end")

    def _open_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn file Excel đánh giá học sinh",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return

        self.loaded_file = filepath
        filename = os.path.basename(filepath)
        self.file_label.configure(text=f"✅ {filename}", text_color=SUCCESS)
        self._log(f"Đã tải file: {filename}")

        try:
            file_type = self.processor.load_file(filepath)
            type_display = {"nlpc": "Năng lực Phẩm chất (Tiểu học)",
                           "dinhky_monhoc": "Đánh giá định kỳ theo môn",
                           "unknown": "Chưa xác định"}.get(file_type, file_type)
            self._log(f"Loại file: {type_display}")

            sheets = self.processor.get_sheet_info()
            info_text = f"Loại file: {type_display}\n"
            total_students = 0
            for s in sheets:
                info_text += f"  • Sheet '{s['name']}': {s['rows']} học sinh\n"
                total_students += s['rows']
            self.info_label.configure(text=info_text, text_color=TEXT_DARK)

            if file_type == "nlpc":
                self.cap_display_var.set("Tiểu Học")
                self._log("Tự động chọn: Tiểu Học (file NLPC)")

            # Lưu sheets để chuyển tab
            self._current_sheets = sheets
            self._current_sheet_idx = 0
            self.preview_stats.configure(text=f"📊 {len(sheets)} sheet • {total_students} học sinh")
            self._build_sheet_tabs(sheets)
            self._show_preview_sheet(sheets[0]["name"])

            self.run_btn.configure(state="normal")
            self._log("Sẵn sàng điền nhận xét!")

        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đọc file:\n{str(e)}")

    def _build_sheet_tabs(self, sheets):
        """Tạo các tab chọn sheet"""
        for w in self.sheet_tabs_frame.winfo_children():
            w.destroy()

        self._tab_buttons = []
        for i, s in enumerate(sheets):
            btn = ctk.CTkButton(
                self.sheet_tabs_frame, text=f"  {s['name']}  ",
                font=("Arial", 11), height=28, corner_radius=5,
                fg_color=ACCENT if i == 0 else "transparent",
                text_color="white" if i == 0 else TEXT_DARK,
                hover_color=ACCENT_HOVER,
                command=lambda idx=i, name=s['name']: self._switch_sheet_tab(idx, name)
            )
            btn.pack(side="left", padx=(8 if i == 0 else 2, 2), pady=3)
            self._tab_buttons.append(btn)

    def _switch_sheet_tab(self, idx, name):
        """Chuyển tab sheet"""
        self._current_sheet_idx = idx
        for i, btn in enumerate(self._tab_buttons):
            if i == idx:
                btn.configure(fg_color=ACCENT, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_DARK)
        self._show_preview_sheet(name)

    def _show_preview(self, sheets):
        """Compatibility wrapper"""
        if sheets:
            self._current_sheets = sheets
            self._build_sheet_tabs(sheets)
            self._show_preview_sheet(sheets[0]["name"])

    def _show_preview_sheet(self, sheet_name):
        """Render bảng preview cho 1 sheet sử dụng Treeview để tối ưu hiệu năng"""
        for w in self.preview_frame.winfo_children():
            w.destroy()

        headers, rows = self.processor.get_preview_data(sheet_name, max_rows=100)
        if not headers:
            return

        # Lọc bỏ cột trống
        visible_cols = []
        for j, h in enumerate(headers):
            if h.strip():
                visible_cols.append((j, h))

        # Giới hạn hiển thị tối đa 15 cột
        visible_cols = visible_cols[:15]
        col_ids = [str(i) for i in range(len(visible_cols))]

        # Setup Treeview
        self.preview_tree = ttk.Treeview(self.preview_frame, columns=col_ids, show="headings", style="Treeview")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.preview_tree.yview)
        x_scroll = ttk.Scrollbar(self.preview_frame, orient="horizontal", command=self.preview_tree.xview)
        self.preview_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.preview_tree.pack(fill="both", expand=True)

        # Cấu hình Columns & Headings
        for i, (orig_j, h_text) in enumerate(visible_cols):
            display_h = h_text[:20] + "…" if len(h_text) > 20 else h_text
            self.preview_tree.heading(str(i), text=display_h)
            width = 150 if i == 2 else 80 # Cột Tên (index 2) rộng hơn
            self.preview_tree.column(str(i), width=width, minwidth=50, anchor="center")

        # Thêm Data
        for row in rows:
            if not any(row):
                continue
            display_row = []
            for (orig_j, _) in visible_cols:
                val = row[orig_j] if orig_j < len(row) else ""
                display_row.append(val[:30])
            self.preview_tree.insert("", "end", values=display_row)

        # Row count
        valid_rows = sum(1 for r in rows if any(r))
        ctk.CTkLabel(self.preview_frame, text=f"Hiển thị {valid_rows} dòng dữ liệu mẫu",
                     font=("Arial", 10), text_color="#7F8C8D").pack(anchor="e", padx=5, pady=(2,0))

    def _run_process(self):
        if not self.loaded_file:
            messagebox.showwarning("Chưa có file", "Vui lòng tải file Excel trước!")
            return

        self._log("Bắt đầu điền nhận xét tự động...")
        cap = CAP_REVERSE.get(self.cap_display_var.get(), "tieu_hoc")
        file_type = self.processor.file_type

        try:
            if file_type == "nlpc":
                count = self.processor.process_nlpc(self.cb)
                self._log(f"✅ Đã xử lý NLPC: {count} học sinh")
            elif file_type == "dinhky_monhoc":
                count = self.processor.process_monhoc(self.cb, cap)
                self._log(f"✅ Đã điền nhận xét: {count} ô")
            else:
                # Try both
                count1 = self.processor.process_nlpc(self.cb)
                count2 = self.processor.process_monhoc(self.cb, cap)
                self._log(f"✅ Đã xử lý: {count1} NLPC + {count2} môn học")

            self.export_btn.configure(state="normal")
            self._log("Hoàn tất! Nhấn 'XUẤT FILE KẾT QUẢ' để lưu.")
            messagebox.showinfo("Thành công", "Đã điền nhận xét tự động thành công!\nNhấn 'Xuất file' để lưu kết quả.")
        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi xử lý:\n{str(e)}")

    def _export_file(self):
        if not self.processor.wb:
            return

        default_name = os.path.splitext(os.path.basename(self.loaded_file))[0] + "_DA_NHAN_XET.xlsx"
        output_path = filedialog.asksaveasfilename(
            title="Lưu file kết quả",
            defaultextension=".xlsx",
            initialfile=default_name,
            filetypes=[("Excel files", "*.xlsx")]
        )
        if output_path:
            try:
                self.processor.save_output(output_path)
                self._log(f"💾 Đã xuất file: {os.path.basename(output_path)}")
                messagebox.showinfo("Thành công", f"Đã xuất file thành công!\n{output_path}")
            except Exception as e:
                self._log(f"LỖI xuất file: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")

    def _open_config(self):
        if self.config_win is None or not self.config_win.winfo_exists():
            self.config_win = ConfigWindow(self, self.cb)
        else:
            self.config_win.focus()

    # =======================================
    # AUTO-UPDATE METHODS
    # =======================================
    def _on_update_check_done(self, has_update, info):
        """Callback từ background thread khi kiểm tra xong"""
        if not has_update or not info:
            return
        # Dùng after() để cập nhật UI từ main thread
        self.after(0, lambda: self._show_update_available(info))

    def _show_update_available(self, info):
        """Hiển thị nút cập nhật nhấp nháy trên topbar"""
        self._update_info = info
        self.update_btn.configure(text=f"🔔 Có phiên bản mới {info['version']}!")
        self.update_btn.pack(side="right", padx=(0, 10))
        self._log(f"🔔 Phát hiện phiên bản mới: {info['version']} ({info['file_size_mb']} MB)")
        self._blink_update_btn()

    def _blink_update_btn(self):
        """Hiệu ứng nhấp nháy cho nút cập nhật"""
        if self._update_info is None:
            return
        self._blink_state = not self._blink_state
        if self._blink_state:
            self.update_btn.configure(fg_color="#E74C3C", text_color="white")
        else:
            self.update_btn.configure(fg_color="#F39C12", text_color="white")
        self.after(800, self._blink_update_btn)

    def _on_update_click(self):
        """Khi người dùng nhấn nút cập nhật"""
        info = self._update_info
        if not info:
            return

        notes = info.get("release_notes", "Không có ghi chú.")
        # Giới hạn ghi chú 300 ký tự
        if len(notes) > 300:
            notes = notes[:300] + "..."

        result = messagebox.askyesno(
            f"Cập nhật phiên bản {info['version']}",
            f"Đã có phiên bản mới: {info['version']}\n"
            f"Dung lượng: {info['file_size_mb']} MB\n\n"
            f"📝 Nội dung cập nhật:\n{notes}\n\n"
            f"Bạn có muốn tải và cập nhật ngay không?\n"
            f"(Ứng dụng sẽ tự động khởi động lại sau khi cập nhật)"
        )
        if result:
            self._start_download()

    def _start_download(self):
        """Bắt đầu tải file cập nhật"""
        info = self._update_info
        self._update_info = None  # Dừng nhấp nháy

        # Đổi nút thành progress
        self.update_btn.configure(
            text="⏳ Đang tải 0%...",
            fg_color="#3498DB",
            state="disabled"
        )
        self._log("⏳ Đang tải bản cập nhật...")

        download_update_async(
            info["download_url"],
            progress_callback=self._on_download_progress,
            done_callback=self._on_download_done
        )

    def _on_download_progress(self, downloaded, total):
        """Cập nhật tiến trình tải"""
        percent = int(downloaded / total * 100) if total > 0 else 0
        self.after(0, lambda p=percent: self.update_btn.configure(
            text=f"⏳ Đang tải {p}%..."
        ))

    def _on_download_done(self, file_path):
        """Callback khi tải xong"""
        if file_path and os.path.exists(file_path):
            self.after(0, lambda: self._apply_downloaded_update(file_path))
        else:
            self.after(0, lambda: self._download_failed())

    def _apply_downloaded_update(self, file_path):
        """Áp dụng bản cập nhật đã tải"""
        self.update_btn.configure(text="✅ Tải xong! Đang cập nhật...")
        self._log("✅ Tải xong! Đang áp dụng bản cập nhật...")

        result = messagebox.showinfo(
            "Cập nhật thành công",
            "Đã tải xong bản cập nhật!\n\n"
            "Ứng dụng sẽ tự động khởi động lại.\n"
            "Nhấn OK để tiếp tục."
        )
        apply_update(file_path)

    def _download_failed(self):
        """Xử lý khi tải thất bại"""
        self.update_btn.configure(
            text="❌ Tải thất bại — Thử lại",
            fg_color="#E74C3C",
            state="normal"
        )
        self._log("❌ Tải bản cập nhật thất bại. Kiểm tra kết nối mạng!")
        self._update_info = self._update_info  # Cho phép thử lại


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
