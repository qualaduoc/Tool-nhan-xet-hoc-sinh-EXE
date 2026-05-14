# ui_page_smas.py - Giao diện trang SMAS (module mới)
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

from smas_processor import SmasProcessor, is_smas_file_xls, is_smas_file_xlsx
from manual_column_ui import ManualColumnConfig, ManualColumnPopup

ACCENT_SMAS = "#16A085"
ACCENT_SMAS_HOVER = "#1ABC9C"
BG_CARD = "#FFFFFF"
TEXT_DARK = "#2C3E50"
TEXT_MID = "#666666"
SUCCESS = "#27AE60"
SUBJECT_PLACEHOLDER = "⚠ Chọn môn học..."
SUBJECT_ALL = "📚 Tất cả các môn (toàn bộ sheet)"
CAP_REVERSE = {"Tiểu Học": "tieu_hoc", "THCS": "thcs", "THPT": "thpt"}
CAP_DISPLAY = {"tieu_hoc": "Tiểu Học", "thcs": "THCS", "thpt": "THPT"}


class SmasPageBuilder:
    """Xây dựng UI và xử lý logic cho trang SMAS."""

    def __init__(self, app):
        self.app = app
        self.processor = SmasProcessor()
        self.loaded_file = None
        self.manual_config = ManualColumnConfig()
        self._sheet_tab_buttons = []

    def build(self, parent):
        app = self.app
        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # === LEFT ===
        left_wrapper = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                                     border_width=1, border_color="#E0D5C5")
        paned.add(left_wrapper, minsize=380, stretch="always")
        left = ctk.CTkScrollableFrame(left_wrapper, fg_color=BG_CARD, corner_radius=0)
        left.pack(fill="both", expand=True)

        # S1: Upload (Card)
        s1_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s1_card.pack(fill="x", padx=20, pady=(20, 10))
        s1 = ctk.CTkFrame(s1_card, fg_color="transparent")
        s1.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s1, text="1. TẢI FILE SMAS", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="File sổ đánh giá học sinh từ SMAS (.xls/.xlsx)",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2, 8))
        btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(btn_row, text="📂 Chọn File SMAS...", fg_color="#FFFFFF",
                       text_color=ACCENT_SMAS, border_width=1, border_color=ACCENT_SMAS,
                       hover_color="#E8F8F5", font=("Arial", 12, "bold"),
                       height=36, width=160, command=self._open_file).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="⚙ Cấu Hình Nhận Xét", fg_color="#2C3E50",
                       hover_color="#34495E", font=("Arial", 11),
                       height=36, width=160, command=self._open_config).pack(side="left")
        self.file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"),
                                        text_color=TEXT_MID)
        self.file_label.pack(anchor="w", pady=(8, 0))

        # S2: Thông tin (Card)
        s2_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s2_card.pack(fill="x", padx=20, pady=10)
        s2 = ctk.CTkFrame(s2_card, fg_color="transparent")
        s2.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s2, text="2. THÔNG TIN FILE", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        info_frame = ctk.CTkFrame(s2, fg_color="#F8F9F9", corner_radius=6)
        info_frame.pack(fill="x", pady=(5, 0))
        self.info_label = ctk.CTkLabel(info_frame, text="Tải file để xem thông tin...",
                                        font=("Arial", 11), text_color=TEXT_MID,
                                        wraplength=350, justify="left")
        self.info_label.pack(padx=12, pady=10, anchor="w")

        # S3: Cấp học + Môn (Card)
        s3_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s3_card.pack(fill="x", padx=20, pady=10)
        s3 = ctk.CTkFrame(s3_card, fg_color="transparent")
        s3.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s3, text="3. CẤP HỌC & MÔN HỌC", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        opt_frame = ctk.CTkFrame(s3, fg_color="#F8F9F9", corner_radius=6)
        opt_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(opt_frame, text="Chọn Cấp Học:", font=("Arial", 11, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(10, 2))
        self.cap_var = ctk.StringVar(value="Tiểu Học")
        ctk.CTkSegmentedButton(opt_frame, values=["Tiểu Học", "THCS", "THPT"],
                               variable=self.cap_var, font=("Arial", 11),
                               selected_color=ACCENT_SMAS, selected_hover_color=ACCENT_SMAS_HOVER,
                               command=self._on_cap_changed).pack(padx=12, pady=(0, 8), fill="x")
        ctk.CTkLabel(opt_frame, text="Chọn Môn / Sheet:", font=("Arial", 11, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(4, 2))
        self.subject_var = ctk.StringVar(value=SUBJECT_ALL)
        self.subject_menu = ctk.CTkOptionMenu(
            opt_frame, variable=self.subject_var,
            values=[SUBJECT_ALL], font=("Arial", 11),
            fg_color="#FFFFFF", button_color=ACCENT_SMAS, button_hover_color=ACCENT_SMAS_HOVER,
            text_color=TEXT_DARK, dropdown_font=("Arial", 11),
            width=300, height=32, command=self._on_subject_changed)
        self.subject_menu.pack(padx=12, pady=(0, 4), fill="x")
        self.subject_hint = ctk.CTkLabel(opt_frame, text="",
                                          font=("Arial", 10, "bold"), text_color=SUCCESS)
        self.subject_hint.pack(anchor="w", padx=12, pady=(0, 8))

        # Manual config
        manual_frame = ctk.CTkFrame(opt_frame, fg_color="transparent")
        manual_frame.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkButton(manual_frame, text="📐 Tùy Chỉnh Cột / Dòng",
                      fg_color="#8E44AD", hover_color="#9B59B6",
                      font=("Arial", 11, "bold"), height=32, width=180,
                      command=self._open_manual_config).pack(side="left")
        self.manual_status = ctk.CTkLabel(manual_frame, text="",
                                           font=("Arial", 10), text_color="#8E44AD")
        self.manual_status.pack(side="left", padx=10)

        # S4: Actions (Card)
        s4_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s4_card.pack(fill="x", padx=20, pady=(10, 20))
        s4 = ctk.CTkFrame(s4_card, fg_color="transparent")
        s4.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        self.run_btn = ctk.CTkButton(s4, text="🚀 ĐIỀN NHẬN XÉT TỰ ĐỘNG",
                                      fg_color=ACCENT_SMAS, hover_color=ACCENT_SMAS_HOVER,
                                      font=("Arial", 12, "bold"), height=40,
                                      command=self._run_process, state="disabled")
        self.run_btn.pack(fill="x", pady=(0, 8))
        self.export_btn = ctk.CTkButton(s4, text="💾 XUẤT FILE KẾT QUẢ",
                                         fg_color=SUCCESS, hover_color="#219A52",
                                         font=("Arial", 12, "bold"), height=40,
                                         command=self._export_file, state="disabled")
        self.export_btn.pack(fill="x")

        # === RIGHT ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")

        preview_header = ctk.CTkFrame(right, fg_color="#117864", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12, 0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 XEM TRƯỚC DỮ LIỆU SMAS",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        self.preview_stats = ctk.CTkLabel(preview_header, text="",
                                           font=("Arial", 10), text_color="#82E0AA")
        self.preview_stats.pack(side="right", padx=15)

        # Sheet tabs
        self.tabs_frame = ctk.CTkFrame(right, fg_color="#ECF0F1", corner_radius=0, height=35)
        self.tabs_frame.pack(fill="x", padx=12)
        self.tabs_frame.pack_propagate(False)

        self.preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        self.preview_frame.pack(fill="both", expand=True, padx=12, pady=(0, 5))

        # Placeholder
        ph = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        ph.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(ph, text="📊", font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(ph, text="Tải file SMAS để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10, 0))

        self.tree = None

        log_header = ctk.CTkFrame(right, fg_color="#117864", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5, 0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ XỬ LÝ SMAS",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)

        self.log_box = ctk.CTkTextbox(right, height=120, fg_color="#1A252F", text_color="#1ABC9C",
                                       font=("Consolas", 11), corner_radius=0,
                                       border_width=1, border_color="#34495E")
        self.log_box.pack(fill="x", padx=12, pady=(0, 12))
        self._log("Chọn file SMAS (.xls/.xlsx) để bắt đầu!")

    # === Helpers ===
    def _log(self, text):
        self.log_box.insert("end", f"→ {text}\n")
        self.log_box.see("end")

    def _on_cap_changed(self, value):
        self._log(f"Đã chọn cấp học: {value}")

    def _on_subject_changed(self, value):
        if value == SUBJECT_ALL:
            self.subject_hint.configure(text="✅ Sẽ nhận xét tất cả các sheet/môn", text_color=SUCCESS)
        else:
            self.subject_hint.configure(text=f"✅ Đã chọn: {value}", text_color=SUCCESS)

    # === File Operations ===
    def _open_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn file SMAS",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return

        self.loaded_file = filepath
        filename = os.path.basename(filepath)
        self.file_label.configure(text=f"✅ {filename}", text_color=SUCCESS)
        self._log(f"Đã tải: {filename}")

        try:
            info = self.processor.load_file(filepath)
            # Hiển thị thông tin
            info_text = f"Trường: {info['school']}\n"
            info_text += f"Lớp: {info['class']}\n"
            info_text += f"Năm học: {info['year']}\n"
            info_text += f"Cấp: {info['grade_level']}\n"
            info_text += f"Số sheet môn học: {info['total_sheets']}\n"
            info_text += f"Môn: {', '.join(info['subjects'][:5])}{'...' if len(info['subjects']) > 5 else ''}"
            self.info_label.configure(text=info_text, text_color=TEXT_DARK)

            # Auto-detect cấp học
            grade = (info.get("grade_level") or "").upper()
            if "TIỂU" in grade:
                self.cap_var.set("Tiểu Học")
            elif "THPT" in grade or "PHỔ THÔNG" in grade:
                self.cap_var.set("THPT")
            elif "THCS" in grade:
                self.cap_var.set("THCS")
            self._log(f"🎯 Auto-detect cấp: {self.cap_var.get()}")

            # Cập nhật dropdown môn
            options = [SUBJECT_ALL] + info["subjects"]
            self.subject_menu.configure(values=options)
            self.subject_var.set(SUBJECT_ALL)
            self.subject_hint.configure(text=f"✅ {info['total_sheets']} môn sẵn sàng", text_color=SUCCESS)

            # Preview & stats
            total_hs = info["total_students"]
            self.preview_stats.configure(text=f"📊 {info['total_sheets']} môn • {total_hs} HS")
            self._build_sheet_tabs()
            if self.processor.sheets_info:
                self._show_preview(self.processor.sheets_info[0]["sheet_name"])

            self.run_btn.configure(state="normal")
            self._log(f"Sẵn sàng! {info['total_sheets']} sheet, {total_hs} HS")

        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đọc file:\n{str(e)}")

    def _build_sheet_tabs(self):
        for w in self.tabs_frame.winfo_children():
            w.destroy()
        self._sheet_tab_buttons = []

        for i, info in enumerate(self.processor.sheets_info):
            # Rút gọn tên sheet
            short_name = info["subject"][:12] + ("…" if len(info["subject"]) > 12 else "")
            btn = ctk.CTkButton(
                self.tabs_frame, text=f"  {short_name}  ",
                font=("Arial", 10), height=26, corner_radius=5,
                fg_color=ACCENT_SMAS if i == 0 else "transparent",
                text_color="white" if i == 0 else TEXT_DARK,
                hover_color=ACCENT_SMAS_HOVER,
                command=lambda idx=i, sn=info["sheet_name"]: self._switch_tab(idx, sn)
            )
            btn.pack(side="left", padx=(6 if i == 0 else 1, 1), pady=3)
            self._sheet_tab_buttons.append(btn)

    def _switch_tab(self, idx, sheet_name):
        for i, btn in enumerate(self._sheet_tab_buttons):
            if i == idx:
                btn.configure(fg_color=ACCENT_SMAS, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_DARK)
        self._show_preview(sheet_name)

    def _show_preview(self, sheet_name):
        for w in self.preview_frame.winfo_children():
            w.destroy()

        headers, rows = self.processor.get_preview_data(sheet_name, max_rows=80)
        if not headers:
            return

        # Chỉ hiện cột quan trọng (bỏ StudentId, Mã HS)
        visible = []
        for j, h in enumerate(headers):
            h_upper = h.upper()
            if "STUDENTID" in h_upper or j == 1:
                continue
            if "MÃ HỌC SINH" in h_upper or j == 2:
                continue
            visible.append((j, h))
        visible = visible[:12]

        col_ids = [str(i) for i in range(len(visible))]
        self.tree = ttk.Treeview(self.preview_frame, columns=col_ids, show="headings")
        y_sb = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.tree.yview)
        x_sb = ttk.Scrollbar(self.preview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_sb.set, xscrollcommand=x_sb.set)
        y_sb.pack(side="right", fill="y")
        x_sb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        for i, (orig_j, h_text) in enumerate(visible):
            display_h = h_text[:18] + "…" if len(h_text) > 18 else h_text
            width = 160 if "tên" in h_text.lower() else (200 if "nhận xét" in h_text.lower() else 80)
            anchor = "w" if width > 100 else "center"
            self.tree.heading(str(i), text=display_h)
            self.tree.column(str(i), width=width, minwidth=50, anchor=anchor)

        for row in rows:
            if not any(row):
                continue
            display = [row[j][:50] if j < len(row) else "" for j, _ in visible]
            self.tree.insert("", "end", values=display)

    def _open_manual_config(self):
        ws = None
        if self.processor.wb and self.processor.sheets_info:
            first_sheet = self.processor.sheets_info[0]["sheet_name"]
            ws = self.processor.wb[first_sheet]
        ManualColumnPopup(self.app, self.manual_config,
                          on_apply=self._on_manual_applied, ws=ws)

    def _on_manual_applied(self, config):
        if config.enabled:
            self.manual_status.configure(
                text=f"✅ Cột {config.comment_col_letter}, dòng {config.row_start}→{config.row_end}")
            self._log(f"📐 Manual: Cột {config.comment_col_letter}, dòng {config.row_start}-{config.row_end}")
        else:
            self.manual_status.configure(text="")
            self._log("🔄 Đã reset về chế độ tự nhận diện")

    def _open_config(self):
        app = self.app
        if hasattr(app, 'config_win') and app.config_win and app.config_win.winfo_exists():
            app.config_win.focus()
        else:
            from config_ui import ConfigWindow
            app.config_win = ConfigWindow(app, app.cb)

    # === Process & Export ===
    def _run_process(self):
        if not self.loaded_file:
            messagebox.showwarning("Chưa có file", "Vui lòng tải file SMAS trước!")
            return

        cap = CAP_REVERSE.get(self.cap_var.get(), "tieu_hoc")
        selected = self.subject_var.get()
        self._log(f"Bắt đầu điền nhận xét [{selected}]...")

        try:
            cb = self.app.cb if hasattr(self.app, 'cb') else None

            if selected == SUBJECT_ALL:
                # Xử lý tất cả sheet
                stats = self.processor.process_all(
                    comment_bank=cb, cap=cap, overwrite=False)
                self._log(f"✅ Hoàn tất! {stats['total_sheets']} sheet")
                self._log(f"   Đã nhận xét: {stats['total_filled']} ô")
                self._log(f"   Bỏ qua: {stats['total_skipped']} ô")
                if stats['total_errors']:
                    self._log(f"   Lỗi: {stats['total_errors']} ô")
                for ps in stats.get("per_sheet", []):
                    self._log(f"   📖 {ps['subject']}: {ps['filled']}/{ps['total']} HS")

                msg = (f"Đã nhận xét tự động!\n\n"
                       f"• {stats['total_sheets']} sheet\n"
                       f"• Đã điền: {stats['total_filled']} ô\n"
                       f"• Bỏ qua: {stats['total_skipped']} ô")
            else:
                # Tìm sheet_name theo subject
                sheet_name = None
                for s in self.processor.sheets_info:
                    if s["subject"] == selected:
                        sheet_name = s["sheet_name"]
                        break
                if not sheet_name:
                    messagebox.showwarning("Lỗi", f"Không tìm thấy sheet cho môn: {selected}")
                    return

                mc = self.manual_config if self.manual_config.enabled else None
                stats = self.processor.process_sheet(
                    sheet_name, comment_bank=cb, cap=cap,
                    forced_subject=selected, manual_config=mc)
                self._log(f"✅ {selected}: {stats['filled']}/{stats['total']} HS")
                for d in stats.get("details", [])[:8]:
                    self._log(f"   {d}")

                msg = (f"Đã nhận xét môn {selected}!\n\n"
                       f"• Đã điền: {stats['filled']} ô\n"
                       f"• Bỏ qua: {stats['skipped']} ô")

            self.export_btn.configure(state="normal")

            # Refresh preview
            if self.processor.sheets_info:
                self._show_preview(self.processor.sheets_info[0]["sheet_name"])
                self.preview_stats.configure(text="✅ Đã nhận xét!")

            messagebox.showinfo("Thành công", msg + "\n\nNhấn 'Xuất file' để lưu.")

        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi xử lý:\n{str(e)}")

    def _export_file(self):
        if not self.processor.wb:
            return
        default_name = os.path.splitext(os.path.basename(self.loaded_file))[0] + "_DA_NHAN_XET.xlsx"
        output_path = filedialog.asksaveasfilename(
            title="Lưu file kết quả", defaultextension=".xlsx",
            initialfile=default_name, filetypes=[("Excel files", "*.xlsx")])
        if output_path:
            try:
                self.processor.save_output(output_path)
                self._log(f"💾 Đã xuất: {os.path.basename(output_path)}")
                messagebox.showinfo("Thành công", f"Đã xuất file!\n{output_path}")
            except Exception as e:
                self._log(f"LỖI xuất: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể lưu:\n{str(e)}")
