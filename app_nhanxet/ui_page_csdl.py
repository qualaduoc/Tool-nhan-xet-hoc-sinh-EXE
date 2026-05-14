# ui_page_csdl.py - Giao diện trang CSDL Ngành (tách từ main.py)
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

from config_ui import ConfigWindow
from manual_column_ui import ManualColumnPopup

# Constants (đồng bộ với main.py)
ACCENT = "#E67E22"
ACCENT_HOVER = "#F39C12"
BG_CARD = "#FFFFFF"
TEXT_DARK = "#2C3E50"
TEXT_MID = "#666666"
SUCCESS = "#27AE60"

SUBJECT_PLACEHOLDER = "⚠ Chọn môn học..."
SUBJECT_ALL = "📚 File tổng hợp các môn"
CAP_REVERSE = {"Tiểu Học": "tieu_hoc", "THCS": "thcs", "THPT": "thpt"}


class CsdlPageBuilder:
    """Xây dựng UI và xử lý logic cho trang CSDL Ngành.
    
    Nhận `app` (MainApp instance) để truy cập shared state:
    app.cb, app.processor, app.loaded_file, app.manual_config_csdl, app.config_win
    """

    def __init__(self, app):
        self.app = app

    def build(self, parent):
        """Xây dựng toàn bộ giao diện trang CSDL Ngành"""
        app = self.app

        paned = tk.PanedWindow(parent, orient="horizontal", sashwidth=6,
                               bg="#D5C9B8", sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=(10,5))

        # === LEFT: Upload & Process (scrollable) ===
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
        
        ctk.CTkLabel(s1, text="1. TẢI FILE EXCEL", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="Chọn file .xls hoặc .xlsx từ máy tính (file đánh giá học sinh).",
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

        app.file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11, "italic"),
                                       text_color=TEXT_MID)
        app.file_label.pack(anchor="w", pady=(8,0))

        # Section 2: File info (Card)
        s2_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s2_card.pack(fill="x", padx=20, pady=10)
        s2 = ctk.CTkFrame(s2_card, fg_color="transparent")
        s2.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(s2, text="2. THÔNG TIN FILE", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        app.info_frame = ctk.CTkFrame(s2, fg_color="#F8F9F9", corner_radius=6)
        app.info_frame.pack(fill="x", pady=(5,0))
        app.info_label = ctk.CTkLabel(app.info_frame, text="Tải file để xem thông tin...",
                                       font=("Arial", 11), text_color=TEXT_MID, wraplength=350,
                                       justify="left")
        app.info_label.pack(padx=12, pady=10, anchor="w")

        # Section 3: Settings (Card)
        s3_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s3_card.pack(fill="x", padx=20, pady=10)
        s3 = ctk.CTkFrame(s3_card, fg_color="transparent")
        s3.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(s3, text="3. CẤU HÌNH XỬ LÝ", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        opt_frame = ctk.CTkFrame(s3, fg_color="#F8F9F9", corner_radius=6)
        opt_frame.pack(fill="x", pady=8)

        ctk.CTkLabel(opt_frame, text="Chọn Cấp Học:", font=("Arial", 11, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(10,2))
        app.cap_display_var = ctk.StringVar(value="Tiểu Học")
        cap_menu = ctk.CTkSegmentedButton(opt_frame, values=["Tiểu Học", "THCS", "THPT"],
                                           variable=app.cap_display_var,
                                           font=("Arial", 11),
                                           selected_color=ACCENT, selected_hover_color=ACCENT_HOVER,
                                           command=self._on_cap_changed)
        cap_menu.pack(padx=12, pady=(0,8), fill="x")

        ctk.CTkLabel(opt_frame, text="Chọn Môn Học:", font=("Arial", 11, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=12, pady=(4,2))
        app.csdl_subject_var = ctk.StringVar(value=SUBJECT_PLACEHOLDER)
        app.csdl_subject_menu = ctk.CTkOptionMenu(
            opt_frame,
            variable=app.csdl_subject_var,
            values=app._get_subject_options("tieu_hoc"),
            font=("Arial", 11),
            fg_color="#FFFFFF", button_color=ACCENT, button_hover_color=ACCENT_HOVER,
            text_color=TEXT_DARK, dropdown_font=("Arial", 11),
            width=300, height=32,
            command=self._on_subject_changed
        )
        app.csdl_subject_menu.pack(padx=12, pady=(0,4), fill="x")
        app.csdl_subject_hint = ctk.CTkLabel(opt_frame, text="⚠ Vui lòng chọn môn học trước khi xử lý",
                                               font=("Arial", 10, "bold"), text_color="#E74C3C")
        app.csdl_subject_hint.pack(anchor="w", padx=12, pady=(0,8))

        app.overwrite_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opt_frame, text="Ghi đè ô nhận xét đã có sẵn",
                        variable=app.overwrite_var, font=("Arial", 11),
                        text_color=TEXT_DARK, fg_color=ACCENT,
                        hover_color=ACCENT_HOVER).pack(anchor="w", padx=12, pady=(0,10))

        manual_frame = ctk.CTkFrame(opt_frame, fg_color="transparent")
        manual_frame.pack(fill="x", padx=12, pady=(0,10))
        ctk.CTkButton(manual_frame, text="📐 Tùy Chỉnh Cột / Dòng",
                      fg_color="#8E44AD", hover_color="#9B59B6",
                      font=("Arial", 11, "bold"), height=32, width=180,
                      command=self._open_manual_config).pack(side="left")
        app.manual_status_csdl = ctk.CTkLabel(manual_frame, text="",
                                                font=("Arial", 10), text_color="#8E44AD")
        app.manual_status_csdl.pack(side="left", padx=10)

        # Section 4: Actions (Card)
        s4_card = ctk.CTkFrame(left, fg_color="#FFFFFF", border_width=1, border_color="#BDC3C7", corner_radius=8)
        s4_card.pack(fill="x", padx=20, pady=(10, 20))
        s4 = ctk.CTkFrame(s4_card, fg_color="transparent")
        s4.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(s4, text="4. THỰC THI", font=("Arial", 13, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))

        action_frame = ctk.CTkFrame(s4, fg_color="transparent")
        action_frame.pack(fill="x")

        app.run_btn = ctk.CTkButton(action_frame, text="🚀 ĐIỀN NHẬN XÉT TỰ ĐỘNG",
                                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                      font=("Arial", 12, "bold"), height=40,
                                      command=self._run_process, state="disabled")
        app.run_btn.pack(fill="x", pady=(0,8))

        app.export_btn = ctk.CTkButton(action_frame, text="💾 XUẤT FILE KẾT QUẢ",
                                         fg_color=SUCCESS, hover_color="#219A52",
                                         font=("Arial", 12, "bold"), height=40,
                                         command=self._export_file, state="disabled")
        app.export_btn.pack(fill="x")

        # === RIGHT: Preview & Log ===
        right = ctk.CTkFrame(paned, fg_color=BG_CARD, corner_radius=12,
                             border_width=1, border_color="#E0D5C5")
        paned.add(right, minsize=350, stretch="always")

        preview_header = ctk.CTkFrame(right, fg_color="#2C3E50", corner_radius=8, height=40)
        preview_header.pack(fill="x", padx=12, pady=(12,0))
        preview_header.pack_propagate(False)
        ctk.CTkLabel(preview_header, text="📋 XEM TRƯỚC DỮ LIỆU",
                     font=("Arial", 13, "bold"), text_color="white").pack(side="left", padx=15)
        app.preview_stats = ctk.CTkLabel(preview_header, text="",
                                          font=("Arial", 10), text_color="#82E0AA")
        app.preview_stats.pack(side="right", padx=15)

        app.sheet_tabs_frame = ctk.CTkFrame(right, fg_color="#ECF0F1", corner_radius=0, height=35)
        app.sheet_tabs_frame.pack(fill="x", padx=12)
        app.sheet_tabs_frame.pack_propagate(False)
        app._current_sheets = []
        app._current_sheet_idx = 0

        app.preview_frame = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=0)
        app.preview_frame.pack(fill="both", expand=True, padx=12, pady=(0,5))

        app.preview_placeholder = ctk.CTkFrame(app.preview_frame, fg_color="transparent")
        app.preview_placeholder.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(app.preview_placeholder, text="📂",
                     font=("Arial", 42), text_color="#BDC3C7").pack()
        ctk.CTkLabel(app.preview_placeholder, text="Tải file Excel để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#7F8C8D").pack(pady=(10,0))
        ctk.CTkLabel(app.preview_placeholder, text="Hỗ trợ file .xls và .xlsx đánh giá học sinh",
                     font=("Arial", 11), text_color="#BDC3C7").pack()

        app.preview_tree = None

        log_header = ctk.CTkFrame(right, fg_color="#2C3E50", corner_radius=8, height=32)
        log_header.pack(fill="x", padx=12, pady=(5,0))
        log_header.pack_propagate(False)
        ctk.CTkLabel(log_header, text="📝 NHẬT KÝ XỬ LÝ",
                     font=("Arial", 11, "bold"), text_color="white").pack(side="left", padx=15)

        app.log_box = ctk.CTkTextbox(right, height=120, fg_color="#1A252F", text_color="#2ECC71",
                                      font=("Consolas", 11), corner_radius=0,
                                      border_width=1, border_color="#34495E")
        app.log_box.pack(fill="x", padx=12, pady=(0,12))
        self._log("Ứng dụng sẵn sàng. Hãy tải file Excel để bắt đầu!")

    # === Event Handlers ===

    def _log(self, text):
        self.app.log_box.insert("end", f"→ {text}\n")
        self.app.log_box.see("end")

    def _on_cap_changed(self, value):
        app = self.app
        cap_key = CAP_REVERSE.get(value, "tieu_hoc")
        new_options = app._get_subject_options(cap_key)
        app.csdl_subject_menu.configure(values=new_options)
        app.csdl_subject_var.set(SUBJECT_PLACEHOLDER)
        app.csdl_subject_hint.configure(text="⚠ Vui lòng chọn môn học trước khi xử lý", text_color="#E74C3C")
        self._log(f"Đã chuyển cấp học: {value} — vui lòng chọn lại môn học")

    def _on_subject_changed(self, value):
        app = self.app
        if value == SUBJECT_PLACEHOLDER:
            app.csdl_subject_hint.configure(text="⚠ Vui lòng chọn môn học trước khi xử lý", text_color="#E74C3C")
        elif value == SUBJECT_ALL:
            app.csdl_subject_hint.configure(text="✅ Sẽ nhận xét tất cả các môn trong file", text_color=SUCCESS)
            self._log(f"📚 Đã chọn: File tổng hợp các môn")
        else:
            app.csdl_subject_hint.configure(text=f"✅ Đã chọn: {value}", text_color=SUCCESS)
            self._log(f"📖 Đã chọn môn: {value}")

    def _open_file(self):
        app = self.app
        filepath = filedialog.askopenfilename(
            title="Chọn file Excel đánh giá học sinh",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return

        app.loaded_file = filepath
        filename = os.path.basename(filepath)
        app.file_label.configure(text=f"✅ {filename}", text_color=SUCCESS)
        self._log(f"Đã tải file: {filename}")

        try:
            file_type = app.processor.load_file(filepath)
            type_display = {"nlpc": "Năng lực Phẩm chất (Tiểu học)",
                           "dinhky_monhoc": "Đánh giá định kỳ theo môn",
                           "unknown": "Chưa xác định"}.get(file_type, file_type)
            self._log(f"Loại file: {type_display}")

            sheets = app.processor.get_sheet_info()
            info_text = f"Loại file: {type_display}\n"
            total_students = 0
            for s in sheets:
                info_text += f"  • Sheet '{s['name']}': {s['rows']} học sinh\n"
                total_students += s['rows']
            app.info_label.configure(text=info_text, text_color=TEXT_DARK)

            if file_type == "nlpc":
                app.cap_display_var.set("Tiểu Học")
                self._log("Tự động chọn: Tiểu Học (file NLPC)")

            app._current_sheets = sheets
            app._current_sheet_idx = 0
            app.preview_stats.configure(text=f"📊 {len(sheets)} sheet • {total_students} học sinh")
            self._build_sheet_tabs(sheets)
            self._show_preview_sheet(sheets[0]["name"])

            app.run_btn.configure(state="normal")
            self._log("Sẵn sàng điền nhận xét!")

        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đọc file:\n{str(e)}")

    def _build_sheet_tabs(self, sheets):
        app = self.app
        for w in app.sheet_tabs_frame.winfo_children():
            w.destroy()

        app._tab_buttons = []
        for i, s in enumerate(sheets):
            btn = ctk.CTkButton(
                app.sheet_tabs_frame, text=f"  {s['name']}  ",
                font=("Arial", 11), height=28, corner_radius=5,
                fg_color=ACCENT if i == 0 else "transparent",
                text_color="white" if i == 0 else TEXT_DARK,
                hover_color=ACCENT_HOVER,
                command=lambda idx=i, name=s['name']: self._switch_sheet_tab(idx, name)
            )
            btn.pack(side="left", padx=(8 if i == 0 else 2, 2), pady=3)
            app._tab_buttons.append(btn)

    def _switch_sheet_tab(self, idx, name):
        app = self.app
        app._current_sheet_idx = idx
        for i, btn in enumerate(app._tab_buttons):
            if i == idx:
                btn.configure(fg_color=ACCENT, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_DARK)
        self._show_preview_sheet(name)

    def _show_preview(self, sheets):
        """Compatibility wrapper"""
        if sheets:
            self.app._current_sheets = sheets
            self._build_sheet_tabs(sheets)
            self._show_preview_sheet(sheets[0]["name"])

    def _show_preview_sheet(self, sheet_name):
        app = self.app
        for w in app.preview_frame.winfo_children():
            w.destroy()

        headers, rows = app.processor.get_preview_data(sheet_name, max_rows=100)
        if not headers:
            return

        visible_cols = []
        for j, h in enumerate(headers):
            if h.strip():
                visible_cols.append((j, h))
        visible_cols = visible_cols[:15]
        col_ids = [str(i) for i in range(len(visible_cols))]

        app.preview_tree = ttk.Treeview(app.preview_frame, columns=col_ids, show="headings", style="Treeview")
        
        y_scroll = ttk.Scrollbar(app.preview_frame, orient="vertical", command=app.preview_tree.yview)
        x_scroll = ttk.Scrollbar(app.preview_frame, orient="horizontal", command=app.preview_tree.xview)
        app.preview_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        app.preview_tree.pack(fill="both", expand=True)

        for i, (orig_j, h_text) in enumerate(visible_cols):
            display_h = h_text[:20] + "…" if len(h_text) > 20 else h_text
            app.preview_tree.heading(str(i), text=display_h)
            h_lower = h_text.lower()
            if "nội dung" in h_lower or "nhận xét" in h_lower:
                width = 250
                anchor = "w"
            elif i == 1 or "họ" in h_lower or "tên" in h_lower:
                width = 150
                anchor = "w"
            else:
                width = 80
                anchor = "center"
            app.preview_tree.column(str(i), width=width, minwidth=50, anchor=anchor)

        for row in rows:
            if not any(row):
                continue
            display_row = []
            for (orig_j, _) in visible_cols:
                val = row[orig_j] if orig_j < len(row) else ""
                display_row.append(val[:60])
            app.preview_tree.insert("", "end", values=display_row)

        valid_rows = sum(1 for r in rows if any(r))
        ctk.CTkLabel(app.preview_frame, text=f"Hiển thị {valid_rows} dòng dữ liệu mẫu",
                     font=("Arial", 10), text_color="#7F8C8D").pack(anchor="e", padx=5, pady=(2,0))

    def _open_manual_config(self):
        app = self.app
        ws = None
        if app.processor.wb:
            ws = app.processor.wb[app.processor.wb.sheetnames[0]]
        ManualColumnPopup(app, app.manual_config_csdl,
                          on_apply=self._on_manual_applied, ws=ws)

    def _on_manual_applied(self, config):
        app = self.app
        if config.enabled:
            app.manual_status_csdl.configure(
                text=f"✅ Cột {config.comment_col_letter}, dòng {config.row_start}→{config.row_end}")
            self._log(f"📐 Manual mode: Cột {config.comment_col_letter}, dòng {config.row_start}-{config.row_end}")
        else:
            app.manual_status_csdl.configure(text="")
            self._log("🔄 Đã reset về chế độ tự nhận diện")

    def _run_process(self):
        app = self.app
        if not app.loaded_file:
            messagebox.showwarning("Chưa có file", "Vui lòng tải file Excel trước!")
            return

        if not app._validate_subject_selection(app.csdl_subject_var, "CSDL Ngành"):
            return

        cap = CAP_REVERSE.get(app.cap_display_var.get(), "tieu_hoc")
        forced_subject = app._get_forced_subject(app.csdl_subject_var)
        subj_display = forced_subject or "Tổng hợp các môn"
        self._log(f"Bắt đầu điền nhận xét tự động [{subj_display}]...")
        file_type = app.processor.file_type

        try:
            if app.manual_config_csdl.enabled:
                self._log(f"📐 Chế độ thủ công: Cột {app.manual_config_csdl.comment_col_letter}, dòng {app.manual_config_csdl.row_start}-{app.manual_config_csdl.row_end}")
                count = app.processor.process_manual(app.cb, app.manual_config_csdl, cap, forced_subject=forced_subject)
                self._log(f"✅ Đã điền {count} ô nhận xét (chế độ thủ công)")
            elif file_type == "nlpc":
                count = app.processor.process_nlpc(app.cb, cap)
                self._log(f"✅ Đã xử lý NLPC: {count} học sinh")
            elif file_type == "dinhky_monhoc":
                count = app.processor.process_monhoc(app.cb, cap, forced_subject=forced_subject)
                self._log(f"✅ Đã điền nhận xét [{subj_display}]: {count} ô")
            else:
                count1 = app.processor.process_nlpc(app.cb, cap)
                count2 = app.processor.process_monhoc(app.cb, cap, forced_subject=forced_subject)
                self._log(f"✅ Đã xử lý: {count1} NLPC + {count2} môn học")

            app.export_btn.configure(state="normal")
            self._log("Hoàn tất! Nhấn 'XUẤT FILE KẾT QUẢ' để lưu.")

            try:
                sheets = app.processor.get_sheet_info()
                if sheets:
                    self._show_preview(sheets)
                    app.preview_stats.configure(text="✅ Đã điền nhận xét!")
            except Exception:
                pass

            messagebox.showinfo("Thành công", f"Đã điền nhận xét tự động thành công!\nNhấn 'Xuất file' để lưu kết quả.")
        except Exception as e:
            self._log(f"LỖI: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi xử lý:\n{str(e)}")

    def _export_file(self):
        app = self.app
        if not app.processor.wb:
            return

        default_name = os.path.splitext(os.path.basename(app.loaded_file))[0] + "_DA_NHAN_XET.xlsx"
        output_path = filedialog.asksaveasfilename(
            title="Lưu file kết quả",
            defaultextension=".xlsx",
            initialfile=default_name,
            filetypes=[("Excel files", "*.xlsx")]
        )
        if output_path:
            try:
                app.processor.save_output(output_path)
                self._log(f"💾 Đã xuất file: {os.path.basename(output_path)}")
                messagebox.showinfo("Thành công", f"Đã xuất file thành công!\n{output_path}")
            except Exception as e:
                self._log(f"LỖI xuất file: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể lưu file:\n{str(e)}")

    def _open_config(self):
        app = self.app
        if app.config_win is None or not app.config_win.winfo_exists():
            app.config_win = ConfigWindow(app, app.cb)
        else:
            app.config_win.focus()
