# ui_page_vnedu.py - Giao diện trang VNEDU (tách từ main.py)
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from vnedu_processor import load_settings as vnedu_load_settings

ACCENT = "#E67E22"
ACCENT_HOVER = "#F39C12"
BG_CARD = "#FFFFFF"
TEXT_DARK = "#2C3E50"
TEXT_MID = "#666666"
SUCCESS = "#27AE60"
SUBJECT_PLACEHOLDER = "⚠ Chọn môn học..."


class VneduPageBuilder:
    """Xây dựng UI cho trang VNEDU. Handlers delegate về app (MainApp)."""

    def __init__(self, app):
        self.app = app

    def build(self, parent):
        app = self.app
        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10,5))

        left_wrapper = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                                     border_width=1, border_color="#E0D5C5")
        paned.add(left_wrapper, minsize=380, stretch="always")
        left = ctk.CTkScrollableFrame(left_wrapper, fg_color=BG_CARD, corner_radius=0)
        left.pack(fill="both", expand=True)

        # Section 1: Upload (Card)
        s1_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s1_card.pack(fill="x", padx=20, pady=(20, 10))
        s1 = ctk.CTkFrame(s1_card, fg_color="transparent")
        s1.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s1, text="1. TẢI FILE VNEDU", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="File tổng hợp đánh giá hoặc Sổ điểm chi tiết (.xls/.xlsx)",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))
        btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(btn_row, text="📂 Chọn File VNEDU...", fg_color="#FFFFFF",
                       text_color="#3498DB", border_width=1, border_color="#3498DB",
                       hover_color="#EBF5FB", font=("Arial", 12, "bold"),
                       height=36, width=160, command=app._vnedu_open_file).pack(side="left", padx=(0,10))
        ctk.CTkButton(btn_row, text="⚙ Cấu Hình Lời Nhận Xét", fg_color="#2C3E50",
                       hover_color="#34495E", font=("Arial", 11),
                       height=36, width=160, command=app._open_subject_config).pack(side="left")
        app.vnedu_mode_badge = ctk.CTkLabel(btn_row, text="", font=("Arial", 10, "bold"),
                                              corner_radius=6, width=0, height=22)
        app.vnedu_mode_badge.pack(side="left", padx=(10,0))
        app.vnedu_file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"),
                                              text_color=TEXT_MID)
        app.vnedu_file_label.pack(anchor="w", pady=(8,0))

        # Section 2: Thông tin (Card)
        s2_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s2_card.pack(fill="x", padx=20, pady=10)
        s2 = ctk.CTkFrame(s2_card, fg_color="transparent")
        s2.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s2, text="2. THÔNG TIN FILE", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        app.vnedu_info_frame = ctk.CTkFrame(s2, fg_color="#F8F9F9", corner_radius=6)
        app.vnedu_info_frame.pack(fill="x", pady=(5,0))
        app.vnedu_info_label = ctk.CTkLabel(app.vnedu_info_frame, text="Vui lòng tải file để xem thông tin lớp...",
                                              font=("Arial", 11), text_color=TEXT_MID,
                                              wraplength=350, justify="left")
        app.vnedu_info_label.pack(padx=12, pady=10, anchor="w")

        # Section 3: Chọn Cấp + Môn (Card)
        s25_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s25_card.pack(fill="x", padx=20, pady=10)
        s25 = ctk.CTkFrame(s25_card, fg_color="transparent")
        s25.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s25, text="3. CHỌN CẤP HỌC & MÔN HỌC", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        vnedu_cap_subj_frame = ctk.CTkFrame(s25, fg_color="#F8F9F9", corner_radius=6)
        vnedu_cap_subj_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(vnedu_cap_subj_frame, text="Chọn Cấp Học:", font=("Arial", 11, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(10,2))
        app.vnedu_cap_var = ctk.StringVar(value="THCS")
        ctk.CTkSegmentedButton(vnedu_cap_subj_frame, values=["Tiểu Học", "THCS", "THPT"],
                               variable=app.vnedu_cap_var, font=("Arial", 11),
                               selected_color="#3498DB", selected_hover_color="#2980B9",
                               command=app._on_vnedu_cap_changed).pack(padx=12, pady=(0,8), fill="x")
        ctk.CTkLabel(vnedu_cap_subj_frame, text="Chọn Môn Học:", font=("Arial", 11, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(4,2))
        app.vnedu_subject_var = ctk.StringVar(value=SUBJECT_PLACEHOLDER)
        app.vnedu_subject_menu = ctk.CTkOptionMenu(
            vnedu_cap_subj_frame, variable=app.vnedu_subject_var,
            values=app._get_subject_options("thcs"), font=("Arial", 11),
            fg_color="#FFFFFF", button_color="#3498DB", button_hover_color="#2980B9",
            text_color=TEXT_DARK, dropdown_font=("Arial", 11),
            width=300, height=32, command=app._on_vnedu_subject_changed)
        app.vnedu_subject_menu.pack(padx=12, pady=(0,4), fill="x")
        app.vnedu_subject_hint = ctk.CTkLabel(vnedu_cap_subj_frame, text="⚠ Vui lòng chọn môn học trước khi xử lý",
                                                font=("Arial", 10, "bold"), text_color="#E74C3C")
        app.vnedu_subject_hint.pack(anchor="w", padx=12, pady=(0,8))

        # Section 4: Cấu hình ngưỡng điểm (Card)
        app.vnedu_s3_container_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        app.vnedu_s3_container_card.pack(fill="x", padx=20, pady=10)
        app.vnedu_s3_container = ctk.CTkFrame(app.vnedu_s3_container_card, fg_color="transparent")
        app.vnedu_s3_container.pack(fill="x", padx=15, pady=15)

        # 4A: Ngưỡng điểm (assessment mode)
        app.vnedu_s3a = ctk.CTkFrame(app.vnedu_s3_container, fg_color="transparent")
        app.vnedu_s3a.pack(fill="x")
        ctk.CTkLabel(app.vnedu_s3a, text="4. CẤU HÌNH NGƯỠNG ĐIỂM", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        score_frame = ctk.CTkFrame(app.vnedu_s3a, fg_color="#F8F9F9", corner_radius=6)
        score_frame.pack(fill="x", pady=8)
        settings = vnedu_load_settings()
        for label_text, color, var_name, default_key, default_val in [
            ("T (Hoàn thành tốt):", "#27AE60", "vnedu_t_min", "score_T_min", 9),
            ("H (Hoàn thành):", "#E67E22", "vnedu_h_min", "score_H_min", 5),
        ]:
            r = ctk.CTkFrame(score_frame, fg_color="transparent")
            r.pack(fill="x", padx=12, pady=(10 if var_name == "vnedu_t_min" else 3, 3))
            ctk.CTkLabel(r, text=label_text, font=("Arial", 11, "bold"),
                         text_color=color, width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(r, text="từ", font=("Arial", 11), text_color=TEXT_MID).pack(side="left", padx=(5,5))
            entry = ctk.CTkEntry(r, width=45, height=26, font=("Arial", 12), justify="center", border_width=1)
            entry.insert(0, str(settings.get(default_key, default_val)))
            entry.pack(side="left")
            setattr(app, var_name, entry)
        r3 = ctk.CTkFrame(score_frame, fg_color="transparent")
        r3.pack(fill="x", padx=12, pady=(3,8))
        ctk.CTkLabel(r3, text="C (Chưa HT):", font=("Arial", 11, "bold"),
                     text_color="#E74C3C", width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(r3, text="< ngưỡng H", font=("Arial", 11), text_color=TEXT_MID).pack(side="left", padx=5)
        ctk.CTkButton(score_frame, text="Lưu cấu hình", fg_color="#F2F4F4", text_color="#2C3E50",
                       hover_color="#E5E8E8", height=28, width=100, font=("Arial", 11),
                       command=app._vnedu_save_settings).pack(padx=12, pady=(0,10), anchor="e")

        # 4B: Subject config (ẩn)
        app.vnedu_s3b = ctk.CTkFrame(app.vnedu_s3_container, fg_color="transparent")
        app.subj_level_widgets = []
        app.subj_text_widgets = {}
        app._subj_grade_key = "thcs"
        app._subject_config_win = None

        # Manual config
        manual_vnedu_frame = ctk.CTkFrame(app.vnedu_s3_container_card, fg_color="transparent")
        manual_vnedu_frame.pack(fill="x", padx=15, pady=(0, 15))
        ctk.CTkButton(manual_vnedu_frame, text="📐 Tùy Chỉnh Cột / Dòng",
                      fg_color="#8E44AD", hover_color="#9B59B6",
                      font=("Arial", 11, "bold"), height=32, width=180,
                      command=app._open_manual_config_vnedu).pack(side="left")
        app.manual_status_vnedu = ctk.CTkLabel(manual_vnedu_frame, text="",
                                                 font=("Arial", 10), text_color="#8E44AD")
        app.manual_status_vnedu.pack(side="left", padx=10)

        # Section 5: Actions (Card)
        s4_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s4_card.pack(fill="x", padx=20, pady=(10, 20))
        s4 = ctk.CTkFrame(s4_card, fg_color="transparent")
        s4.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))
        action_frame = ctk.CTkFrame(s4, fg_color="transparent")
        action_frame.pack(fill="x")
        app.vnedu_run_btn = ctk.CTkButton(action_frame, text="🚀 ĐIỀN MỨC ĐẠT ĐƯỢC",
                                            fg_color="#2C3E50", hover_color="#34495E",
                                            font=("Arial", 12, "bold"), height=40,
                                            command=app._vnedu_run, state="disabled")
        app.vnedu_run_btn.pack(fill="x", pady=(0,8))
        app.vnedu_subj_run_btn = ctk.CTkButton(action_frame, text="📝 NHẬN XÉT MÔN HỌC",
                                                 fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                                 font=("Arial", 12, "bold"), height=40,
                                                 command=app._vnedu_subject_run, state="disabled")
        app.vnedu_export_btn = ctk.CTkButton(action_frame, text="💾 XUẤT FILE KẾT QUẢ",
                                               fg_color=SUCCESS, hover_color="#219A52",
                                               font=("Arial", 12, "bold"), height=40,
                                               command=app._vnedu_export, state="disabled")
        app.vnedu_export_btn.pack(fill="x")
        ctk.CTkLabel(s4, text="").pack()

        # === RIGHT: Preview & Log ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")
        preview_header = ctk.CTkFrame(right, fg_color="#1A5276", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12,0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 XEM TRƯỚC DỮ LIỆU VNEDU",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        app.vnedu_preview_stats = ctk.CTkLabel(preview_header, text="",
                                                 font=("Arial", 10), text_color="#82E0AA")
        app.vnedu_preview_stats.pack(side="right", padx=15)
        app.vnedu_preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        app.vnedu_preview_frame.pack(fill="both", expand=True, padx=12, pady=(5,5))
        app.vnedu_ph = ctk.CTkFrame(app.vnedu_preview_frame, fg_color="transparent")
        app.vnedu_ph.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(app.vnedu_ph, text="🌐", font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(app.vnedu_ph, text="Tải file VNEDU để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10,0))
        app.vnedu_tree = None

        log_header = ctk.CTkFrame(right, fg_color="#1A5276", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5,0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ XỬ LÝ VNEDU",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)
        app.vnedu_log_box = ctk.CTkTextbox(right, height=120, fg_color="#1A252F",
                                             text_color="#5DADE2", font=("Consolas", 11),
                                             corner_radius=0, border_width=1, border_color="#34495E")
        app.vnedu_log_box.pack(fill="x", padx=12, pady=(0,12))
        app._vnedu_log("Chọn file VNEDU (.xlsx) để bắt đầu!")
