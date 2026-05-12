# config_ui.py - Giao diện cấu hình kho nhận xét
import customtkinter as ctk
from tkinter import messagebox

class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, parent, comment_bank):
        super().__init__(parent)
        self.cb = comment_bank
        self.title("⚙ Cấu Hình Nhận Xét - ETA Connect")
        self.geometry("1100x700")
        self.configure(fg_color="#FFF8F0")
        self.current_cap = "tieu_hoc"
        self.current_loai = "mon_hoc"
        self.current_subject = None
        self.current_muc = None
        self._build_ui()

    def _build_ui(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200, fg_color="#FFF0E0", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="⚙ CẤU HÌNH\nNHẬN XÉT", font=("Arial", 16, "bold"),
                     text_color="#333").pack(pady=(20,5))
        ctk.CTkLabel(sidebar, text="N.T.Được – ETA GROUP\n0904059866",
                     font=("Arial", 11), text_color="#666").pack(pady=(0,20))

        # Navigation buttons
        sections = [
            ("CẤP TIỂU HỌC", None),
            ("📚 Theo môn học", ("tieu_hoc", "mon_hoc")),
            ("🏠 NLPC Tiểu học", ("tieu_hoc", "nlpc")),
            ("", None),
            ("CẤP THCS", None),
            ("📖 Theo môn học", ("thcs", "mon_hoc")),
            ("📊 Mức chung THCS", ("thcs", "muc_chung")),
            ("", None),
            ("CẤP THPT", None),
            ("📖 Theo môn học", ("thpt", "mon_hoc")),
            ("📊 Mức chung THPT", ("thpt", "muc_chung")),
        ]
        for text, cmd_data in sections:
            if cmd_data is None:
                lbl = ctk.CTkLabel(sidebar, text=text, font=("Arial", 12, "bold"),
                                   text_color="#E67E22" if text else "#ccc")
                lbl.pack(pady=(10,2) if text else (5,2), padx=10, anchor="w")
                if not text:
                    ctk.CTkFrame(sidebar, height=1, fg_color="#ddd").pack(fill="x", padx=15, pady=5)
            else:
                btn = ctk.CTkButton(sidebar, text=text, fg_color="transparent",
                                    text_color="#333", hover_color="#FFE0B2",
                                    anchor="w", font=("Arial", 12),
                                    command=lambda d=cmd_data: self._switch_section(d[0], d[1]))
                btn.pack(fill="x", padx=10, pady=2)

        # Bottom buttons
        bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=10, pady=15)
        ctk.CTkButton(bottom, text="💾 Lưu", fg_color="#27AE60", hover_color="#2ECC71",
                       width=80, command=self._save).pack(side="left", padx=2)
        ctk.CTkButton(bottom, text="↩ Reset", fg_color="#E67E22", hover_color="#F39C12",
                       width=80, command=self._reset).pack(side="left", padx=2)

        # Main content
        self.content = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        # Status label
        self.status_lbl = ctk.CTkLabel(self, text="", font=("Arial", 11),
                                       text_color="#27AE60")
        self.status_lbl.place(relx=0.95, y=10, anchor="ne")

        self._switch_section("tieu_hoc", "mon_hoc")

    def _switch_section(self, cap, loai):
        self.current_cap = cap
        self.current_loai = loai
        self.current_subject = None
        self._render_content()

    def _render_content(self):
        for w in self.content.winfo_children():
            w.destroy()

        cap = self.current_cap
        loai = self.current_loai
        cap_label = "TIỂU HỌC" if cap == "tieu_hoc" else "THCS"

        if loai == "muc_chung":
            self._render_muc_chung(cap)
            return

        if loai == "nlpc":
            self._render_nlpc()
            return

        # Mon hoc view
        title = f"NHẬN XÉT MÔN HỌC — CẤP {cap_label}"
        ctk.CTkLabel(self.content, text=title, font=("Arial", 18, "bold"),
                     text_color="#333").pack(pady=(15,5), padx=20, anchor="w")
        ctk.CTkLabel(self.content, text="Lời nhận xét riêng cho từng môn học",
                     font=("Arial", 12), text_color="#888").pack(padx=20, anchor="w")

        data = self.cb.data.get(cap, {}).get(loai, {})
        subjects = list(data.keys())

        # Subject list + Add button
        subj_frame = ctk.CTkFrame(self.content, fg_color="#FFF8F0", corner_radius=8)
        subj_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(subj_frame, text=f"Môn học — {cap_label}", font=("Arial", 13, "bold"),
                     text_color="#333").pack(side="left", padx=10)

        add_entry = ctk.CTkEntry(subj_frame, width=150, placeholder_text="Tên môn mới...")
        add_entry.pack(side="right", padx=5)
        ctk.CTkButton(subj_frame, text="+ Thêm", width=70, fg_color="#E67E22",
                       hover_color="#F39C12",
                       command=lambda: self._add_subject(add_entry.get())).pack(side="right", padx=5)

        # Subject buttons
        btn_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=5)
        for subj in subjects:
            sf = ctk.CTkFrame(btn_frame, fg_color="#FFF0E0", corner_radius=5)
            sf.pack(side="left", padx=3, pady=3)
            ctk.CTkButton(sf, text=subj, fg_color="#FFF0E0", text_color="#333",
                          hover_color="#FFE0B2", width=120,
                          command=lambda s=subj: self._select_subject(s)).pack(side="left")
            ctk.CTkButton(sf, text="✕", width=25, fg_color="#E74C3C",
                          hover_color="#C0392B",
                          command=lambda s=subj: self._remove_subject(s)).pack(side="left")

        # Subject detail
        if self.current_subject and self.current_subject in data:
            self._render_subject_detail(cap, loai, self.current_subject, data[self.current_subject])

    def _render_nlpc(self):
        ctk.CTkLabel(self.content, text="NLPC TIỂU HỌC", font=("Arial", 18, "bold"),
                     text_color="#333").pack(pady=(15,5), padx=20, anchor="w")
        ctk.CTkLabel(self.content, text="Lời nhận xét Năng lực và Phẩm chất chủ yếu theo từng mức",
                     font=("Arial", 12), text_color="#888").pack(padx=20, anchor="w")

        nlpc_data = self.cb.data.get("tieu_hoc", {}).get("nlpc", {})
        for nhom_key, nhom_label in [("nang_luc_chung", "Năng lực chung"),
                                      ("nang_luc_dac_thu", "Năng lực đặc thù"),
                                      ("pham_chat", "Phẩm chất chủ yếu")]:
            nhom_data = nlpc_data.get(nhom_key, {})
            frame = ctk.CTkFrame(self.content, fg_color="#FFF8F0", corner_radius=8, border_width=1, border_color="#E67E22")
            frame.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(frame, text=nhom_label, font=("Arial", 14, "bold"),
                         text_color="#E67E22").pack(pady=(10,5), padx=15, anchor="w")

            for muc in ["T", "D", "C"]:
                muc_labels = {"T": "Tốt (T)", "D": "Hoàn thành (Đ)", "C": "Chưa hoàn thành (C)"}
                muc_label = muc_labels.get(muc, muc)
                comments = nhom_data.get(muc, [])
                self._render_comment_group(frame, "tieu_hoc", "nlpc", nhom_key, muc, muc_label, comments)

    def _render_muc_chung(self, cap):
        ctk.CTkLabel(self.content, text=f"MỨC CHUNG — CẤP {'THCS' if cap=='thcs' else 'TIỂU HỌC'}",
                     font=("Arial", 18, "bold"), text_color="#333").pack(pady=(15,5), padx=20, anchor="w")

        muc_data = self.cb.data.get(cap, {}).get("muc_chung", {})
        for muc_key, muc_info in muc_data.items():
            if not isinstance(muc_info, dict):
                continue
            frame = ctk.CTkFrame(self.content, fg_color="#FFF8F0", corner_radius=8,
                                 border_width=1, border_color="#E67E22")
            frame.pack(fill="x", padx=20, pady=8)

            dmin = muc_info.get("diem_min", "")
            dmax = muc_info.get("diem_max", "")
            ma = muc_info.get("ma", muc_key)
            title = f"{muc_key} — Điểm: {dmin} – {dmax} — Mã: {ma}"
            ctk.CTkLabel(frame, text=title, font=("Arial", 13, "bold"),
                         text_color="#E67E22").pack(pady=(10,5), padx=15, anchor="w")

            comments = muc_info.get("nhan_xet", [])
            self._render_comment_list_inline(frame, cap, "muc_chung", muc_key, comments, is_muc_chung=True)

    def _select_subject(self, subj):
        self.current_subject = subj
        self._render_content()

    def _render_subject_detail(self, cap, loai, subject, data):
        frame = ctk.CTkFrame(self.content, fg_color="#FFFFFF", corner_radius=8,
                             border_width=1, border_color="#E67E22")
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame, text=f"📝 {subject}", font=("Arial", 15, "bold"),
                     text_color="#E67E22").pack(pady=(10,5), padx=15, anchor="w")

        if cap == "tieu_hoc":
            mucs = [("T", "Hoàn thành tốt (T)"), ("H", "Hoàn thành (H)"), ("C", "Chưa hoàn thành (C)")]
        else:
            mucs = [("XS", "Xuất sắc"), ("T", "Tốt"), ("K", "Khá"), ("D", "Đạt"), ("CD", "Chưa đạt")]

        for muc_key, muc_label in mucs:
            comments = data.get(muc_key, [])
            self._render_comment_group(frame, cap, loai, subject, muc_key, muc_label, comments)

    def _render_comment_group(self, parent, cap, loai, key, muc, label, comments):
        ctk.CTkLabel(parent, text=label, font=("Arial", 12, "bold"),
                     text_color="#C0392B").pack(pady=(8,2), padx=20, anchor="w")

        if isinstance(comments, list):
            for i, c in enumerate(comments):
                row = ctk.CTkFrame(parent, fg_color="#FFF0E0", corner_radius=5)
                row.pack(fill="x", padx=25, pady=2)
                ctk.CTkLabel(row, text=c, font=("Arial", 11), text_color="#333",
                             wraplength=600, anchor="w", justify="left").pack(side="left", padx=10, pady=5, fill="x", expand=True)
                ctk.CTkButton(row, text="✕", width=28, height=28, fg_color="#E74C3C",
                              hover_color="#C0392B",
                              command=lambda idx=i: self._del_comment(cap, loai, key, muc, idx)
                              ).pack(side="right", padx=5, pady=3)

        # Add new
        add_frame = ctk.CTkFrame(parent, fg_color="transparent")
        add_frame.pack(fill="x", padx=25, pady=(2,8))
        entry = ctk.CTkEntry(add_frame, placeholder_text="Nhập lời nhận xét mới...", width=500)
        entry.pack(side="left", padx=(0,5))
        ctk.CTkButton(add_frame, text="+ Thêm mẫu", width=90, fg_color="#E67E22",
                       hover_color="#F39C12",
                       command=lambda e=entry: self._add_comment(cap, loai, key, muc, e)
                       ).pack(side="left")

    def _render_comment_list_inline(self, parent, cap, loai, muc_key, comments, is_muc_chung=False):
        for i, c in enumerate(comments):
            row = ctk.CTkFrame(parent, fg_color="#FFF0E0", corner_radius=5)
            row.pack(fill="x", padx=25, pady=2)
            ctk.CTkLabel(row, text=c, font=("Arial", 11), text_color="#333",
                         wraplength=600, anchor="w", justify="left").pack(side="left", padx=10, pady=5, fill="x", expand=True)
            ctk.CTkButton(row, text="✕", width=28, height=28, fg_color="#E74C3C",
                          hover_color="#C0392B",
                          command=lambda idx=i: self._del_comment_muc_chung(cap, muc_key, idx)
                          ).pack(side="right", padx=5, pady=3)

        add_frame = ctk.CTkFrame(parent, fg_color="transparent")
        add_frame.pack(fill="x", padx=25, pady=(2,10))
        entry = ctk.CTkEntry(add_frame, placeholder_text="Nhập lời nhận xét mới...", width=500)
        entry.pack(side="left", padx=(0,5))
        ctk.CTkButton(add_frame, text="+ Thêm mẫu", width=90, fg_color="#E67E22",
                       hover_color="#F39C12",
                       command=lambda e=entry: self._add_comment_muc_chung(cap, muc_key, e)
                       ).pack(side="left")

    def _add_comment(self, cap, loai, key, muc, entry):
        text = entry.get().strip()
        if text:
            self.cb.add_comment(cap, loai, key, muc, text)
            entry.delete(0, "end")
            self._show_status("✅ Đã thêm nhận xét!")
            self._render_content()

    def _del_comment(self, cap, loai, key, muc, idx):
        self.cb.remove_comment(cap, loai, key, muc, idx)
        self._show_status("🗑 Đã xóa nhận xét!")
        self._render_content()

    def _add_comment_muc_chung(self, cap, muc_key, entry):
        text = entry.get().strip()
        if text:
            muc = self.cb.data.get(cap, {}).get("muc_chung", {}).get(muc_key, {})
            if isinstance(muc, dict):
                muc.setdefault("nhan_xet", []).append(text)
                self.cb.save()
                entry.delete(0, "end")
                self._show_status("✅ Đã thêm!")
                self._render_content()

    def _del_comment_muc_chung(self, cap, muc_key, idx):
        try:
            self.cb.data[cap]["muc_chung"][muc_key]["nhan_xet"].pop(idx)
            self.cb.save()
            self._show_status("🗑 Đã xóa!")
            self._render_content()
        except (KeyError, IndexError):
            pass

    def _add_subject(self, name):
        name = name.strip()
        if name:
            self.cb.add_subject(self.current_cap, self.current_loai, name)
            self._show_status(f"✅ Đã thêm môn: {name}")
            self._render_content()

    def _remove_subject(self, name):
        if messagebox.askyesno("Xác nhận", f"Xóa môn '{name}' và toàn bộ nhận xét?"):
            self.cb.remove_subject(self.current_cap, self.current_loai, name)
            if self.current_subject == name:
                self.current_subject = None
            self._show_status(f"🗑 Đã xóa môn: {name}")
            self._render_content()

    def _save(self):
        self.cb.save()
        self._show_status("💾 Đã lưu cấu hình thành công!")

    def _reset(self):
        if messagebox.askyesno("Xác nhận", "Reset toàn bộ về mặc định?\nMọi thay đổi sẽ bị mất!"):
            self.cb.reset()
            self._show_status("↩ Đã reset về mặc định!")
            self._render_content()

    def _show_status(self, text):
        self.status_lbl.configure(text=text)
        self.after(3000, lambda: self.status_lbl.configure(text=""))
