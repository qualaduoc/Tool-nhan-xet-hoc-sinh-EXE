# ui_page_convert.py - Giao diện trang Chuyển Đổi (tách từ main.py)
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

BG_CARD = "#FFFFFF"
TEXT_DARK = "#2C3E50"
TEXT_MID = "#666666"
SUCCESS = "#27AE60"


class ConvertPageBuilder:
    """Xây dựng UI cho trang Chuyển Đổi. Handlers delegate về app (MainApp)."""

    def __init__(self, app):
        self.app = app

    def build(self, parent):
        app = self.app
        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10,5))

        left_wrapper = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                                     border_width=1, border_color="#E0D5C5")
        paned.add(left_wrapper, minsize=400, stretch="always")
        left = ctk.CTkScrollableFrame(left_wrapper, fg_color=BG_CARD, corner_radius=0)
        left.pack(fill="both", expand=True)

        # Title
        title_frame = ctk.CTkFrame(left, fg_color="#8E44AD", corner_radius=8)
        title_frame.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(title_frame, text="🔄 CHUYỂN ĐỔI DỮ LIỆU",
                     font=("Arial", 15, "bold"), text_color="white").pack(padx=15, pady=8, anchor="w")
        ctk.CTkLabel(title_frame, text="Copy điểm & đánh giá giữa VNEDU ↔ CSDL Ngành",
                     font=("Arial", 11), text_color="#D2B4DE").pack(padx=15, pady=(0,8), anchor="w")

        # Section 1: File Nguồn (Card)
        s1_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s1_card.pack(fill="x", padx=20, pady=10)
        s1 = ctk.CTkFrame(s1_card, fg_color="transparent")
        s1.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s1, text="1. FILE NGUỒN (đã có dữ liệu)", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="File VNEDU hoặc CSDL Ngành đã chấm điểm.",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))
        ctk.CTkButton(s1, text="📂 Chọn File Nguồn...", fg_color="#FFFFFF",
                       text_color="#8E44AD", border_width=1, border_color="#8E44AD",
                       hover_color="#F4ECF7", font=("Arial", 12, "bold"),
                       height=36, width=200, command=app._convert_open_source).pack(anchor="w")
        app.cvt_source_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"), text_color=TEXT_MID)
        app.cvt_source_label.pack(anchor="w", pady=(5,0))
        app.cvt_source_info = ctk.CTkLabel(s1, text="", font=("Arial", 10), text_color="#7D3C98")
        app.cvt_source_info.pack(anchor="w")

        # Section 2: File Đích (Card)
        s2_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s2_card.pack(fill="x", padx=20, pady=10)
        s2 = ctk.CTkFrame(s2_card, fg_color="transparent")
        s2.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s2, text="2. FILE ĐÍCH (cần điền dữ liệu vào)", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s2, text="File trống hoặc chưa hoàn chỉnh của hệ thống kia.",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))
        ctk.CTkButton(s2, text="📂 Chọn File Đích...", fg_color="#FFFFFF",
                       text_color="#8E44AD", border_width=1, border_color="#8E44AD",
                       hover_color="#F4ECF7", font=("Arial", 12, "bold"),
                       height=36, width=200, command=app._convert_open_dest).pack(anchor="w")
        app.cvt_dest_label = ctk.CTkLabel(s2, text="Chưa chọn file", font=("Arial", 11, "italic"), text_color=TEXT_MID)
        app.cvt_dest_label.pack(anchor="w", pady=(5,0))
        app.cvt_dest_info = ctk.CTkLabel(s2, text="", font=("Arial", 10), text_color="#7D3C98")
        app.cvt_dest_info.pack(anchor="w")

        # Section 3: Hướng chuyển đổi (Card)
        s3_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s3_card.pack(fill="x", padx=20, pady=10)
        s3 = ctk.CTkFrame(s3_card, fg_color="transparent")
        s3.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s3, text="3. HƯỚNG CHUYỂN ĐỔI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        app.cvt_direction_frame = ctk.CTkFrame(s3, fg_color="#F8F9F9", corner_radius=6)
        app.cvt_direction_frame.pack(fill="x", pady=5)
        app.cvt_direction_label = ctk.CTkLabel(app.cvt_direction_frame,
                                                 text="Chọn 2 file để xác định hướng chuyển đổi...",
                                                 font=("Arial", 12), text_color=TEXT_MID)
        app.cvt_direction_label.pack(padx=12, pady=10)

        # Section 4: Actions (Card)
        s4_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s4_card.pack(fill="x", padx=20, pady=(10, 20))
        s4 = ctk.CTkFrame(s4_card, fg_color="transparent")
        s4.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))
        app.cvt_run_btn = ctk.CTkButton(s4, text="🔄 CHUYỂN ĐỔI DỮ LIỆU",
                                          fg_color="#8E44AD", hover_color="#7D3C98",
                                          font=("Arial", 12, "bold"), height=40,
                                          command=app._convert_run, state="disabled")
        app.cvt_run_btn.pack(fill="x", pady=(0,8))
        app.cvt_export_btn = ctk.CTkButton(s4, text="💾 XUẤT FILE KẾT QUẢ",
                                             fg_color=SUCCESS, hover_color="#219A52",
                                             font=("Arial", 12, "bold"), height=40,
                                             command=app._convert_export, state="disabled")
        app.cvt_export_btn.pack(fill="x")

        # === RIGHT: Preview & Log ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")
        preview_header = ctk.CTkFrame(right, fg_color="#6C3483", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12,0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 KẾT QUẢ CHUYỂN ĐỔI",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        app.cvt_preview_stats = ctk.CTkLabel(preview_header, text="",
                                               font=("Arial", 10), text_color="#D7BDE2")
        app.cvt_preview_stats.pack(side="right", padx=15)
        app.cvt_preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        app.cvt_preview_frame.pack(fill="both", expand=True, padx=12, pady=(5,5))
        app.cvt_ph = ctk.CTkFrame(app.cvt_preview_frame, fg_color="transparent")
        app.cvt_ph.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(app.cvt_ph, text="🔄", font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(app.cvt_ph, text="Chọn 2 file và bấm Chuyển Đổi để xem kết quả",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10,0))
        app.cvt_tree = None

        log_header = ctk.CTkFrame(right, fg_color="#6C3483", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5,0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ CHUYỂN ĐỔI",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)
        app.cvt_log_box = ctk.CTkTextbox(right, height=150, fg_color="#1A252F",
                                           text_color="#BB8FCE", font=("Consolas", 11),
                                           corner_radius=0, border_width=1, border_color="#34495E")
        app.cvt_log_box.pack(fill="x", padx=12, pady=(0,12))
        app._convert_log("Chọn File Nguồn và File Đích để bắt đầu!")
