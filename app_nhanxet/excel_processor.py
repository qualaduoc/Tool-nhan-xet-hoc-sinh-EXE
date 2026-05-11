# excel_processor.py - Xử lý đọc/ghi file Excel
import openpyxl
from openpyxl.utils import get_column_letter
import os
import re

class ExcelProcessor:
    """Đọc file Excel giáo viên tải lên, nhận diện cấu trúc, điền nhận xét"""

    # Mapping mức đánh giá - dùng LOWERCASE để so khớp linh hoạt
    # Tiểu học: T (Tốt/Hoàn thành tốt), H (Hoàn thành/Đạt), C (Chưa hoàn thành)
    LEVEL_MAP_TIEU_HOC = {
        # Viết tắt 1 ký tự
        "t": "T", "h": "H", "c": "C", "đ": "H", "d": "H",
        # Viết tắt nhiều ký tự
        "htt": "T", "ht": "H", "cht": "C", "kht": "C",
        # Viết đầy đủ
        "tốt": "T", "hoàn thành tốt": "T",
        "hoàn thành": "H", "đạt": "H",
        "chưa hoàn thành": "C", "không hoàn thành": "C", "chưa đạt": "C",
        # Biến thể khác
        "t ": "T", "đ ": "H", "h ": "H", "c ": "C",  # có dấu cách thừa
    }

    # THCS: XS, T, K, D, CD
    LEVEL_MAP_THCS = {
        # Viết tắt
        "xs": "XS", "t": "T", "g": "T", "k": "K", "đ": "D", "d": "D",
        "tb": "D", "cd": "CD", "cđ": "CD", "y": "CD",
        # Viết đầy đủ
        "xuất sắc": "XS", "xuat sac": "XS",
        "tốt": "T", "giỏi": "T",
        "khá": "K", "kha": "K",
        "đạt": "D", "dat": "D", "trung bình": "D", "trung binh": "D",
        "chưa đạt": "CD", "chua dat": "CD", "yếu": "CD", "yeu": "CD", "kém": "CD", "kem": "CD",
        # Hoàn thành mapping (Tiểu học format nhưng trong file THCS)
        "hoàn thành tốt": "T", "htt": "T",
        "hoàn thành": "K", "ht": "K",
        "chưa hoàn thành": "CD", "cht": "CD", "kht": "CD", "không hoàn thành": "CD",
    }

    def __init__(self):
        self.wb = None
        self.filepath = None
        self.file_type = None  # "nlpc" or "dinhky_monhoc"

    def load_file(self, filepath):
        """Tải file Excel"""
        self.filepath = filepath
        self.wb = openpyxl.load_workbook(filepath)
        self.file_type = self._detect_file_type()
        return self.file_type

    def _detect_file_type(self):
        """Nhận diện loại file: NLPC (năng lực phẩm chất) hay đánh giá theo môn"""
        if not self.wb:
            return None
        sheet_names = [s.lower() for s in self.wb.sheetnames]

        # Check for NLPC format (has merged header "Năng lực chung", "Phẩm chất")
        first_sheet = self.wb[self.wb.sheetnames[0]]
        for row in first_sheet.iter_rows(min_row=1, max_row=2, values_only=False):
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    val = cell.value.strip().lower()
                    if "năng lực" in val or "phẩm chất" in val:
                        return "nlpc"

        # Check for subject-based format
        for sn in self.wb.sheetnames:
            ws = self.wb[sn]
            for cell in ws[1]:
                if cell.value and isinstance(cell.value, str):
                    if "mức đạt được" in cell.value.lower() or "nội dung nhận xét" in cell.value.lower():
                        return "dinhky_monhoc"

        return "unknown"

    def get_sheet_info(self):
        """Trả về thông tin các sheet và số dòng dữ liệu"""
        if not self.wb:
            return []
        info = []
        for sn in self.wb.sheetnames:
            if sn.lower() == "huongdan":
                continue
            ws = self.wb[sn]
            data_rows = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if any(v is not None for v in row):
                    data_rows += 1
            info.append({"name": sn, "rows": data_rows, "max_col": ws.max_column})
        return info

    def get_preview_data(self, sheet_name, max_rows=10):
        """Xem trước dữ liệu sheet"""
        if not self.wb or sheet_name not in self.wb.sheetnames:
            return [], []
        ws = self.wb[sheet_name]
        headers = []
        for cell in ws[1]:
            headers.append(str(cell.value) if cell.value else "")

        rows_data = []
        for row in ws.iter_rows(min_row=2, max_row=min(ws.max_row, max_rows + 1), values_only=True):
            rows_data.append([str(v) if v else "" for v in row])
        return headers, rows_data

    def process_nlpc(self, comment_bank):
        """Xử lý file NLPC (Năng lực Phẩm chất) - Tiểu học"""
        ws = self.wb[self.wb.sheetnames[0]]
        count = 0
        for row_idx in range(3, ws.max_row + 1):
            name_cell = ws.cell(row=row_idx, column=3).value
            if not name_cell:
                continue

            # Đọc các cột đánh giá NL (E-S) để xác định mức chung
            levels = []
            for col in range(5, 20):
                val = ws.cell(row=row_idx, column=col).value
                if val and isinstance(val, str):
                    levels.append(val.strip())

            # Xác định mức chung dựa trên đa số
            overall = self._get_majority_level(levels, "tieu_hoc")

            # Cột U - Nhận xét năng lực chung (nội dung)
            if not ws.cell(row=row_idx, column=21).value:
                comment = comment_bank.get_random_comment("tieu_hoc", "nlpc", "nang_luc_chung", overall)
                if comment:
                    ws.cell(row=row_idx, column=21).value = comment

            # Cột W - Nhận xét năng lực đặc thù (nội dung)
            if not ws.cell(row=row_idx, column=23).value:
                dt_level = overall
                if overall == "H":
                    dt_level = "D"
                comment = comment_bank.get_random_comment("tieu_hoc", "nlpc", "nang_luc_dac_thu", dt_level)
                if comment:
                    ws.cell(row=row_idx, column=23).value = comment

            # Cột Y - Nhận xét phẩm chất (nội dung)
            if not ws.cell(row=row_idx, column=25).value:
                pc_level = overall
                if overall == "H":
                    pc_level = "D"
                comment = comment_bank.get_random_comment("tieu_hoc", "nlpc", "pham_chat", pc_level)
                if comment:
                    ws.cell(row=row_idx, column=25).value = comment

            count += 1
        return count

    def process_monhoc(self, comment_bank, cap="tieu_hoc"):
        """Xử lý file đánh giá theo môn học"""
        count = 0
        for sn in self.wb.sheetnames:
            if sn.lower() == "huongdan":
                continue
            ws = self.wb[sn]

            # Tìm cột "Mức đạt được" và "Nội dung nhận xét"
            muc_col = None
            nhanxet_col = None
            for cell in ws[1]:
                if cell.value and isinstance(cell.value, str):
                    val = cell.value.strip().lower()
                    if "mức đạt" in val:
                        muc_col = cell.column
                    elif "nội dung nhận xét" in val or "nội dung" in val.lower():
                        nhanxet_col = cell.column

            if not muc_col or not nhanxet_col:
                continue

            subject_name = sn.strip()

            for row_idx in range(2, ws.max_row + 1):
                muc_val = ws.cell(row=row_idx, column=muc_col).value
                existing = ws.cell(row=row_idx, column=nhanxet_col).value

                if not muc_val or existing:
                    continue

                level = str(muc_val).strip()
                normalized = self._normalize_level(level, cap)

                comment = comment_bank.get_random_comment(cap, "mon_hoc", subject_name, normalized)
                if not comment:
                    # Fallback: thử tìm trong tên môn gần giống
                    comment = self._fallback_comment(comment_bank, cap, subject_name, normalized)

                if comment:
                    ws.cell(row=row_idx, column=nhanxet_col).value = comment
                    count += 1
        return count

    def _fallback_comment(self, comment_bank, cap, subject_name, level):
        """Tìm nhận xét từ môn học có tên gần giống"""
        subjects = comment_bank.data.get(cap, {}).get("mon_hoc", {})
        sn_lower = subject_name.lower()
        for key in subjects:
            if key.lower() in sn_lower or sn_lower in key.lower():
                comments = comment_bank.get_comments(cap, "mon_hoc", key, level)
                if comments:
                    import random
                    return random.choice(comments)

        # Nếu vẫn không có, dùng nhận xét mức chung
        if cap == "thcs":
            muc_chung = comment_bank.data.get("thcs", {}).get("muc_chung", {}).get(level, {})
            if isinstance(muc_chung, dict) and "nhan_xet" in muc_chung:
                pool = muc_chung["nhan_xet"]
                if pool:
                    import random
                    return random.choice(pool)
        return ""

    def _normalize_level(self, level, cap):
        """Chuẩn hóa mức đánh giá - xử lý mọi biến thể viết tắt/đầy đủ"""
        raw = level.strip()
        key = raw.lower().strip()

        level_map = self.LEVEL_MAP_TIEU_HOC if cap == "tieu_hoc" else self.LEVEL_MAP_THCS
        default = "H" if cap == "tieu_hoc" else "D"

        # Thử exact match (lowercase)
        if key in level_map:
            return level_map[key]

        # Thử với dấu cách thừa ở cuối (phổ biến trong file Excel)
        key_stripped = key.rstrip()
        if key_stripped in level_map:
            return level_map[key_stripped]

        # Thử match từ dài nhất trước (ưu tiên "hoàn thành tốt" trước "hoàn thành")
        sorted_keys = sorted(level_map.keys(), key=len, reverse=True)
        for k in sorted_keys:
            if k in key:
                return level_map[k]

        return default

    def _get_majority_level(self, levels, cap):
        """Xác định mức đánh giá chung - ưu tiên mức thấp nhất nếu có"""
        if not levels:
            return "T" if cap == "tieu_hoc" else "D"

        normalized = [self._normalize_level(l, cap) for l in levels]
        from collections import Counter
        counter = Counter(normalized)

        # Nếu tất cả cùng mức → trả về mức đó
        if len(counter) == 1:
            return counter.most_common(1)[0][0]

        # Nếu có nhiều mức → dùng mức chiếm đa số, nhưng nếu có "C" thì ưu tiên hạ
        if cap == "tieu_hoc":
            priority = {"C": 0, "H": 1, "T": 2}
        else:
            priority = {"CD": 0, "D": 1, "K": 2, "T": 3, "XS": 4}

        # Nếu mức thấp chiếm >= 30% → dùng mức thấp
        total = sum(counter.values())
        for muc in sorted(counter.keys(), key=lambda x: priority.get(x, 99)):
            if counter[muc] / total >= 0.3:
                return muc

        return counter.most_common(1)[0][0]

    def save_output(self, output_path):
        """Lưu file kết quả"""
        if self.wb:
            self.wb.save(output_path)
            return True
        return False
