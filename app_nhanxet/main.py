# main.py - Giao diện chính App Nhận Xét Học Sinh ETA Connect
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from comment_data import CommentBank
from excel_processor import ExcelProcessor
from config_ui import ConfigWindow
from license_manager import check_license
from license_ui import ActivationScreen, LicenseInfoBar

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
        self.title("[ ETA Connect — Nhận Xét Học Sinh Tự Động v1.0 ]")
        self.geometry("1050x700")
        self.minsize(800, 550)
        self.configure(fg_color=BG_MAIN)

        self.cb = CommentBank()
        self.processor = ExcelProcessor()
        self.loaded_file = None
        self.config_win = None

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
        ctk.CTkLabel(topbar, text="v1.0 | Khầy Được — ETA GROUP",
                     font=("Arial", 11), text_color="#FFE0B2").pack(side="right", padx=20)

        # === MAIN LAYOUT: PanedWindow cho co giãn tối ưu ===
        paned = tk.PanedWindow(self, orient="horizontal", sashwidth=6,
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
        ctk.CTkLabel(s1, text="[1] TẢI FILE EXCEL", font=("Arial", 14, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(s1, text="Chọn file .xlsx từ máy tính (file đánh giá học sinh)",
                     font=("Arial", 11), text_color=TEXT_MID).pack(anchor="w", pady=(2,8))

        btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        btn_row.pack(fill="x")
        ctk.CTkButton(btn_row, text="📂 Chọn File Excel...", fg_color=ACCENT,
                       hover_color=ACCENT_HOVER, font=("Arial", 13, "bold"),
                       height=40, command=self._open_file).pack(side="left", padx=(0,10))
        ctk.CTkButton(btn_row, text="⚙ Cấu Hình Nhận Xét", fg_color="#2C3E50",
                       hover_color="#34495E", font=("Arial", 12),
                       height=40, command=self._open_config).pack(side="left")

        self.file_label = ctk.CTkLabel(s1, text="Chưa chọn file", font=("Arial", 11),
                                       text_color=TEXT_MID)
        self.file_label.pack(anchor="w", pady=(8,0))

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#E0D5C5").pack(fill="x", padx=20, pady=5)

        # Section 2: File info
        s2 = ctk.CTkFrame(left, fg_color="transparent")
        s2.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s2, text="[2] THÔNG TIN FILE", font=("Arial", 14, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        self.info_frame = ctk.CTkFrame(s2, fg_color="#FFF8F0", corner_radius=8)
        self.info_frame.pack(fill="x", pady=(5,0))
        self.info_label = ctk.CTkLabel(self.info_frame, text="Tải file để xem thông tin...",
                                       font=("Arial", 11), text_color=TEXT_MID, wraplength=400,
                                       justify="left")
        self.info_label.pack(padx=15, pady=10, anchor="w")

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#E0D5C5").pack(fill="x", padx=20, pady=5)

        # Section 3: Settings
        s3 = ctk.CTkFrame(left, fg_color="transparent")
        s3.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(s3, text="[3] CẤU HÌNH XỬ LÝ", font=("Arial", 14, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w")

        opt_frame = ctk.CTkFrame(s3, fg_color="#FFF8F0", corner_radius=8)
        opt_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(opt_frame, text="Cấp học:", font=("Arial", 12), text_color=TEXT_DARK).pack(anchor="w", padx=15, pady=(10,2))
        self.cap_display_var = ctk.StringVar(value="Tiểu Học")
        cap_menu = ctk.CTkSegmentedButton(opt_frame, values=["Tiểu Học", "Trung Học Cơ Sở"],
                                           variable=self.cap_display_var,
                                           font=("Arial", 12),
                                           selected_color=ACCENT, selected_hover_color=ACCENT_HOVER)
        cap_menu.pack(padx=15, pady=(0,5), fill="x")

        self.overwrite_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(opt_frame, text="Ghi đè ô nhận xét đã có sẵn",
                        variable=self.overwrite_var, font=("Arial", 11),
                        text_color=TEXT_DARK, fg_color=ACCENT,
                        hover_color=ACCENT_HOVER).pack(anchor="w", padx=15, pady=(0,10))

        # Separator
        ctk.CTkFrame(left, height=1, fg_color="#E0D5C5").pack(fill="x", padx=20, pady=5)

        # Section 4: Actions
        s4 = ctk.CTkFrame(left, fg_color="transparent")
        s4.pack(fill="x", padx=20, pady=(5,15))
        ctk.CTkLabel(s4, text="[4] THỰC THI", font=("Arial", 14, "bold"),
                     text_color=TEXT_DARK).pack(anchor="w", pady=(0,8))

        self.run_btn = ctk.CTkButton(s4, text="🚀 ĐIỀN NHẬN XÉT TỰ ĐỘNG",
                                     fg_color=SUCCESS, hover_color="#2ECC71",
                                     font=("Arial", 14, "bold"), height=45,
                                     command=self._run_process, state="disabled")
        self.run_btn.pack(fill="x", pady=(0,8))

        self.export_btn = ctk.CTkButton(s4, text="💾 XUẤT FILE KẾT QUẢ",
                                        fg_color="#3498DB", hover_color="#5DADE2",
                                        font=("Arial", 14, "bold"), height=45,
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

        # Preview table (scrollable cả ngang lẫn dọc)
        self.preview_frame = ctk.CTkScrollableFrame(right, fg_color="#FAFAFA",
                                                     corner_radius=0, height=250)
        self.preview_frame.pack(fill="both", expand=True, padx=12, pady=(0,5))

        # Placeholder khi chưa có file
        self.preview_placeholder = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.preview_placeholder.pack(fill="both", expand=True, pady=40)
        ctk.CTkLabel(self.preview_placeholder, text="📂",
                     font=("Arial", 36), text_color="#BDC3C7").pack()
        ctk.CTkLabel(self.preview_placeholder, text="Tải file Excel để xem trước dữ liệu",
                     font=("Arial", 13), text_color="#95A5A6").pack(pady=(5,0))
        ctk.CTkLabel(self.preview_placeholder, text="Hỗ trợ file .xlsx đánh giá học sinh",
                     font=("Arial", 11), text_color="#BDC3C7").pack()

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

        # === BOTTOM BAR ===
        bottom = ctk.CTkFrame(self, height=30, fg_color="#2C3E50", corner_radius=0)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)
        ctk.CTkLabel(bottom, text="ETA Connect v1.0 © 2026 | Phát triển bởi Khầy Được — ETA GROUP",
                     font=("Arial", 10), text_color="#95A5A6").pack(expand=True)

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
        """Render bảng preview cho 1 sheet — chuyên nghiệp"""
        for w in self.preview_frame.winfo_children():
            w.destroy()

        headers, rows = self.processor.get_preview_data(sheet_name, max_rows=50)
        if not headers:
            return

        # Lọc bỏ cột trống
        visible_cols = []
        for j, h in enumerate(headers):
            if h.strip():
                visible_cols.append((j, h))

        # Giới hạn hiển thị tối đa 10 cột
        visible_cols = visible_cols[:10]

        # === TABLE CONTAINER ===
        table = ctk.CTkFrame(self.preview_frame, fg_color="#FFFFFF", corner_radius=6,
                             border_width=1, border_color="#D5D8DC")
        table.pack(fill="x", pady=(5,10), padx=2)

        # Cấu hình grid columns đều nhau
        for col_idx in range(len(visible_cols)):
            table.grid_columnconfigure(col_idx, weight=1, uniform="col")

        # === HEADER ROW ===
        for col_idx, (orig_j, h_text) in enumerate(visible_cols):
            hdr_cell = ctk.CTkFrame(table, fg_color="#2C3E50", corner_radius=0,
                                    height=32)
            hdr_cell.grid(row=0, column=col_idx, sticky="nsew", padx=(0, 1), pady=(0, 1))
            hdr_cell.grid_propagate(False)
            # Rút gọn header dài
            display_h = h_text[:18] + "…" if len(h_text) > 18 else h_text
            ctk.CTkLabel(hdr_cell, text=display_h, font=("Arial", 9, "bold"),
                         text_color="white").pack(expand=True, padx=3)

        # === DATA ROWS ===
        for i, row in enumerate(rows):
            if not any(row):
                continue
            stripe_bg = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"

            for col_idx, (orig_j, _) in enumerate(visible_cols):
                val = row[orig_j] if orig_j < len(row) else ""

                # Xác định màu cho mức đánh giá
                cell_fg = TEXT_DARK
                cell_bg = stripe_bg
                cell_font = ("Arial", 9)
                val_stripped = val.strip()

                if val_stripped in self.LEVEL_COLORS:
                    text_color, bg_color = self.LEVEL_COLORS[val_stripped]
                    cell_fg = text_color
                    cell_bg = bg_color
                    cell_font = ("Arial", 9, "bold")

                cell = ctk.CTkFrame(table, fg_color=cell_bg, corner_radius=0, height=28)
                cell.grid(row=i + 1, column=col_idx, sticky="nsew", padx=(0, 1), pady=(0, 1))
                cell.grid_propagate(False)

                # Rút gọn nội dung dài
                display_val = val[:25] + "…" if len(val) > 25 else val
                ctk.CTkLabel(cell, text=display_val, font=cell_font,
                             text_color=cell_fg).pack(expand=True, padx=3)

        # === LEGEND ===
        legend = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        legend.pack(fill="x", pady=(0, 5), padx=5)
        ctk.CTkLabel(legend, text="Chú thích:", font=("Arial", 9, "bold"),
                     text_color=TEXT_MID).pack(side="left", padx=(0, 8))
        legend_items = [
            ("T/Tốt", "#27AE60"), ("H/Hoàn thành", "#E67E22"),
            ("C/Chưa HT", "#E74C3C"), ("XS/Xuất sắc", "#8E44AD"),
            ("K/Khá", "#2980B9"),
        ]
        for label, color in legend_items:
            dot = ctk.CTkFrame(legend, width=10, height=10, fg_color=color, corner_radius=5)
            dot.pack(side="left", padx=(0, 2))
            ctk.CTkLabel(legend, text=label, font=("Arial", 9),
                         text_color=TEXT_MID).pack(side="left", padx=(0, 8))

        # Row count
        valid_rows = sum(1 for r in rows if any(r))
        ctk.CTkLabel(self.preview_frame, text=f"Hiển thị {valid_rows} dòng dữ liệu",
                     font=("Arial", 9), text_color="#95A5A6").pack(anchor="e", padx=5)

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


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
