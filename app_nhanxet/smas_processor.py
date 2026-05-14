# smas_processor.py - Xử lý file SMAS (Sổ đánh giá học sinh)
import os
import json
import random
import openpyxl
import xlrd

import sys
if getattr(sys, 'frozen', False):
    _APP_DIR = os.path.dirname(sys.executable)
else:
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(_APP_DIR, "smas_settings.json")


def is_smas_file_xls(filepath):
    """Kiểm tra file .xls có phải file SMAS không.
    Dấu hiệu: nhiều sheet, mỗi sheet có 'BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN' ở row 5."""
    try:
        wb = xlrd.open_workbook(filepath, on_demand=True)
        names = wb.sheet_names()
        if len(names) < 2:
            return False
        # Thử đọc sheet thứ 2 (sheet 0 thường bị lỗi)
        for idx in range(1, min(3, len(names))):
            try:
                ws = wb.sheet_by_index(idx)
                for r in range(min(8, ws.nrows)):
                    v = ws.cell_value(r, 0)
                    if v and isinstance(v, str) and "BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN" in v.upper():
                        wb.release_resources()
                        return True
            except Exception:
                continue
        wb.release_resources()
    except Exception:
        pass
    return False


def is_smas_file_xlsx(filepath):
    """Kiểm tra file .xlsx có phải file SMAS không."""
    try:
        wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
        names = wb.sheetnames
        if len(names) < 2:
            wb.close()
            return False
        for sn in names[1:3]:
            ws = wb[sn]
            for row in ws.iter_rows(min_row=1, max_row=8, max_col=1, values_only=True):
                v = row[0]
                if v and isinstance(v, str) and "BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN" in v.upper():
                    wb.close()
                    return True
        wb.close()
    except Exception:
        pass
    return False


class SmasProcessor:
    """Xử lý file SMAS: đọc nhiều sheet môn học, điền nhận xét tự động."""

    def __init__(self):
        self.wb = None          # openpyxl workbook (để ghi)
        self.file_path = None
        self.file_ext = None
        self.school_name = ""
        self.class_name = ""
        self.year = ""
        self.grade_level = ""   # "Tiểu học", "THCS", "THPT"
        self.sheets_info = []   # [{name, subject, header_row, data_start, comment_cols, score_col, total_students}]

    def load_file(self, filepath):
        """Load file SMAS. Trả về dict thông tin tổng quan."""
        self.file_path = filepath
        self.file_ext = os.path.splitext(filepath)[1].lower()
        self.sheets_info = []

        if self.file_ext == ".xls":
            return self._load_xls(filepath)
        else:
            return self._load_xlsx(filepath)

    def _load_xls(self, filepath):
        """Load file .xls bằng xlrd, convert sang openpyxl."""
        xls_wb = xlrd.open_workbook(filepath, on_demand=True)
        sheet_names = xls_wb.sheet_names()

        self.wb = openpyxl.Workbook()
        # Xóa sheet mặc định
        default_ws = self.wb.active

        first_valid = True
        for idx, sn in enumerate(sheet_names):
            try:
                xls_ws = xls_wb.sheet_by_index(idx)
            except Exception:
                continue

            if first_valid:
                ws = default_ws
                ws.title = sn
                first_valid = False
            else:
                ws = self.wb.create_sheet(title=sn)

            for r in range(xls_ws.nrows):
                for c in range(xls_ws.ncols):
                    val = xls_ws.cell_value(r, c)
                    ctype = xls_ws.cell_type(r, c)
                    if ctype == xlrd.XL_CELL_NUMBER and val == int(val):
                        val = int(val)
                    ws.cell(row=r + 1, column=c + 1, value=val)

        xls_wb.release_resources()
        self._detect_all_sheets()
        return self._get_info()

    def _load_xlsx(self, filepath):
        """Load file .xlsx bằng openpyxl."""
        self.wb = openpyxl.load_workbook(filepath, data_only=True)
        self._detect_all_sheets()
        return self._get_info()

    def _detect_all_sheets(self):
        """Phân tích cấu trúc từng sheet trong workbook."""
        self.sheets_info = []
        for sn in self.wb.sheetnames:
            ws = self.wb[sn]
            info = self._detect_sheet(ws, sn)
            if info:
                self.sheets_info.append(info)

    def _detect_sheet(self, ws, sheet_name):
        """Phân tích 1 sheet. Hỗ trợ cả SMAS lẫn file đánh giá generic."""
        subject = ""
        school = ""
        year = ""
        grade = ""
        class_name = ""

        # Bỏ qua sheet trống hoặc quá nhỏ
        if ws.max_row is None or ws.max_row < 3:
            return None

        # Scan header rows (1-10) trên NHIỀU cột
        for r in range(1, min(11, ws.max_row + 1)):
            for col in range(1, min(15, (ws.max_column or 1) + 1)):
                v = ws.cell(r, col).value
                if not v or not isinstance(v, str):
                    continue
                vu = v.upper().strip()

                if "TRƯỜNG" in vu and not school:
                    school = v.strip()
                    if not self.school_name:
                        self.school_name = school

                # Header SMAS: "BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN..."
                if "BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN" in vu and not subject:
                    text_after = v.upper().replace("BẢNG KẾT QUẢ ĐÁNH GIÁ MÔN", "").strip()
                    parts = text_after.split("-")
                    if parts:
                        # Lấy case gốc
                        try:
                            orig_after = v[v.upper().index("MÔN") + 3:].strip()
                            orig_parts = orig_after.split("-")
                            if orig_parts:
                                subject = orig_parts[0].strip()
                        except ValueError:
                            subject = parts[0].strip()
                    if len(parts) > 1:
                        for p in parts[1:]:
                            if "LỚP" in p.upper():
                                class_name = p.strip()

                # Header generic: "NỘI DUNG NHẬN XÉT", "ĐÁNH GIÁ ĐỊNH KỲ", etc.
                if not subject:
                    for kw in ["ĐÁNH GIÁ ĐỊNH KỲ", "ĐÁNH GIÁ NĂNG LỰC", "NỘI DUNG NHẬN XÉT",
                               "BẢNG ĐÁNH GIÁ", "ĐÁNH GIÁ HỌC SINH"]:
                        if kw in vu:
                            subject = sheet_name  # Dùng tên sheet làm subject
                            break

                if ("HỌC KỲ" in vu or "NĂM HỌC" in vu) and not year:
                    year = v.strip()
                    if not self.year:
                        self.year = year

                if ("LỚP" in vu or "KHỐI" in vu) and not class_name and len(v.strip()) < 30:
                    class_name = v.strip()

        # Detect grade from metadata row (col 7-8)
        for meta_col in [8, 7, 10]:
            meta_grade = ws.cell(1, meta_col).value
            if meta_grade and isinstance(meta_grade, str):
                mg = meta_grade.strip()
                if any(kw in mg.upper() for kw in ["TIỂU HỌC", "THCS", "THPT"]):
                    self.grade_level = mg
                    grade = mg
                    break

        # Fallback: nếu chưa có subject, dùng tên sheet (bỏ qua sheet tên lạ)
        if not subject:
            clean_name = sheet_name.strip()
            # Bỏ qua sheet có tên giống mã hệ thống
            if clean_name and clean_name != "Sheet1" and not clean_name.startswith("XXXX"):
                subject = clean_name
            else:
                # Thử quét thêm: có STT + Họ tên + dữ liệu → vẫn là sheet hợp lệ
                pass

        # Tìm header row (chứa "STT" hoặc "Họ và tên")
        header_row = None
        for r in range(1, min(20, ws.max_row + 1)):
            for c in range(1, min(10, (ws.max_column or 1) + 1)):
                v = ws.cell(r, c).value
                if v and isinstance(v, str):
                    vu = v.strip().upper()
                    if vu in ("STT", "SỐ THỨ TỰ", "TT"):
                        header_row = r
                        break
                    if "HỌ VÀ TÊN" in vu or "HỌ TÊN" in vu:
                        header_row = r
                        break
            if header_row:
                break

        if not header_row:
            return None

        # Nếu vẫn chưa có subject nhưng có header → dùng sheet_name
        if not subject:
            subject = sheet_name.strip() or f"Sheet"

        # Tìm tất cả cột "Nhận xét" / "Nội dung" trong header (quét nhiều dòng)
        comment_cols = []
        score_col = None
        name_col = None

        for c in range(1, (ws.max_column or 1) + 1):
            for check_r in range(max(1, header_row - 3), min(header_row + 2, ws.max_row + 1)):
                v = ws.cell(check_r, c).value
                if v and isinstance(v, str):
                    vu = v.upper().strip()
                    if "NHẬN XÉT" in vu or "NỘI DUNG" in vu:
                        if c not in comment_cols:
                            comment_cols.append(c)
                        break
                    if "HỌ VÀ TÊN" in vu or "HỌ TÊN" in vu:
                        name_col = c

        # Tìm cột điểm/mức
        for c in range(1, (ws.max_column or 1) + 1):
            for check_r in [header_row, header_row + 1]:
                if check_r > ws.max_row:
                    continue
                v = ws.cell(check_r, c).value
                if v and isinstance(v, str):
                    vu = v.upper().strip()
                    if any(kw in vu for kw in ["MỨC ĐẠT", "CUỐI HỌC KỲ", "CUỐI KỲ",
                                                "GIỮA HỌC KỲ", "ĐIỂM", "XẾP LOẠI", "MỨC"]):
                        score_col = c
                        if "CUỐI" in vu or "MỨC ĐẠT" in vu:
                            break

        # Fallback: nếu không tìm thấy cột nhận xét
        if not comment_cols:
            # Tìm cột cuối có header text
            for c in range((ws.max_column or 1), 0, -1):
                v = ws.cell(header_row, c).value
                if v and str(v).strip():
                    comment_cols = [c]
                    break

        if not comment_cols:
            return None

        # Fallback score_col
        if not score_col and comment_cols:
            score_col = comment_cols[-1] - 1
            if score_col < 1:
                score_col = 1

        # Data start row: sau header, bỏ qua sub-header
        data_start = header_row + 1
        # Kiểm tra 2 dòng tiếp theo xem có phải sub-header không
        for offset in range(3):
            check_row = header_row + 1 + offset
            if check_row > ws.max_row:
                break
            first_val = ws.cell(check_row, 1).value
            if first_val is not None:
                try:
                    int(float(str(first_val)))
                    data_start = check_row
                    break
                except (ValueError, TypeError):
                    continue

        # Đếm học sinh
        total = 0
        for r in range(data_start, ws.max_row + 1):
            stt = ws.cell(r, 1).value
            if stt is None or str(stt).strip() == "":
                continue
            try:
                int(float(str(stt)))
                total += 1
            except (ValueError, TypeError):
                continue

        if total == 0:
            return None

        if not self.class_name and class_name:
            self.class_name = class_name

        return {
            "sheet_name": sheet_name,
            "subject": subject,
            "header_row": header_row,
            "data_start": data_start,
            "comment_cols": comment_cols,
            "score_col": score_col,
            "total_students": total,
            "grade": grade,
        }

    def _get_info(self):
        """Trả về dict thông tin tổng quan."""
        subjects = [s["subject"] for s in self.sheets_info]
        total = sum(s["total_students"] for s in self.sheets_info)
        return {
            "school": self.school_name,
            "class": self.class_name,
            "year": self.year,
            "grade_level": self.grade_level,
            "total_sheets": len(self.sheets_info),
            "subjects": subjects,
            "total_students": total,
            "sheets_detail": self.sheets_info,
        }

    def get_sheet_names(self):
        """Trả về danh sách tên sheet hợp lệ."""
        return [s["sheet_name"] for s in self.sheets_info]

    def get_preview_data(self, sheet_name, max_rows=50):
        """Trả về (headers, rows) cho preview."""
        if not self.wb or sheet_name not in self.wb.sheetnames:
            return [], []

        ws = self.wb[sheet_name]
        info = None
        for s in self.sheets_info:
            if s["sheet_name"] == sheet_name:
                info = s
                break
        if not info:
            return [], []

        # Headers
        headers = []
        for c in range(1, ws.max_column + 1):
            v = ws.cell(info["header_row"], c).value
            headers.append(str(v) if v else f"Col{c}")

        # Rows
        rows = []
        for r in range(info["data_start"], min(info["data_start"] + max_rows, ws.max_row + 1)):
            row = []
            for c in range(1, ws.max_column + 1):
                v = ws.cell(r, c).value
                row.append(str(v) if v is not None else "")
            rows.append(row)

        return headers, rows

    def process_sheet(self, sheet_name, comment_bank=None, cap="tieu_hoc",
                      forced_subject=None, overwrite=False, manual_config=None):
        """Điền nhận xét cho 1 sheet cụ thể. Trả về stats dict."""
        if not self.wb:
            raise ValueError("Chưa load file!")

        info = None
        for s in self.sheets_info:
            if s["sheet_name"] == sheet_name:
                info = s
                break
        if not info:
            raise ValueError(f"Không tìm thấy sheet: {sheet_name}")

        ws = self.wb[sheet_name]
        filled = 0
        skipped = 0
        errors = 0
        details = []

        # Xác định cột nhận xét cần điền (cột nhận xét cuối cùng = cuối kỳ)
        if manual_config and manual_config.enabled:
            comment_col = manual_config.comment_col
            data_start = manual_config.row_start
            data_end = manual_config.row_end
            score_col = info["score_col"]
        else:
            comment_col = info["comment_cols"][-1] if info["comment_cols"] else None
            data_start = info["data_start"]
            data_end = ws.max_row
            score_col = info["score_col"]

        if not comment_col:
            raise ValueError("Không xác định được cột nhận xét!")

        subject_for_bank = forced_subject or info["subject"]

        for r in range(data_start, data_end + 1):
            stt = ws.cell(r, 1).value
            if stt is None or str(stt).strip() == "":
                continue
            try:
                int(float(str(stt)))
            except (ValueError, TypeError):
                continue

            existing = ws.cell(r, comment_col).value
            if existing and str(existing).strip() and not overwrite:
                skipped += 1
                continue

            # Lấy điểm/mức từ score_col
            score_val = ws.cell(r, score_col).value if score_col else None
            # Lấy tên HS (cột 4 = index 3 in 0-based, col 4 in 1-based)
            name = ws.cell(r, 4).value or ""
            name = str(name).strip()
            short_name = name.split()[-1] if name.split() else ""

            comment = None
            # Ưu tiên 1: Kho nhận xét theo môn
            if comment_bank and cap and subject_for_bank:
                level = self._score_to_level(score_val, cap)
                if level:
                    comment = comment_bank.get_random_comment(cap, "mon_hoc", subject_for_bank, level)
                    if not comment:
                        comment = self._bank_fallback(comment_bank, cap, subject_for_bank, level)

            # Ưu tiên 2: Sinh nhận xét mặc định
            if not comment:
                comment = self._generate_default_comment(score_val, short_name, subject_for_bank)

            if comment:
                ws.cell(r, comment_col, value=comment)
                filled += 1
                details.append(f"{name}: {score_val} → {comment[:40]}...")
            else:
                errors += 1
                details.append(f"{name}: không có điểm, bỏ qua")

        return {
            "sheet": sheet_name,
            "subject": info["subject"],
            "total": info["total_students"],
            "filled": filled,
            "skipped": skipped,
            "errors": errors,
            "details": details,
        }

    def process_all(self, comment_bank=None, cap="tieu_hoc",
                    forced_subject=None, overwrite=False):
        """Điền nhận xét cho TẤT CẢ sheet. Trả về tổng hợp stats."""
        all_stats = []
        total_filled = 0
        total_skipped = 0
        total_errors = 0

        for info in self.sheets_info:
            subj = forced_subject if forced_subject else None
            stats = self.process_sheet(
                info["sheet_name"], comment_bank, cap, subj, overwrite
            )
            all_stats.append(stats)
            total_filled += stats["filled"]
            total_skipped += stats["skipped"]
            total_errors += stats["errors"]

        return {
            "total_sheets": len(all_stats),
            "total_filled": total_filled,
            "total_skipped": total_skipped,
            "total_errors": total_errors,
            "per_sheet": all_stats,
        }

    def save_output(self, output_path):
        """Lưu workbook ra file."""
        if self.wb:
            self.wb.save(output_path)

    def _score_to_level(self, score_val, cap):
        """Chuyển mức T/H/C hoặc điểm số sang level cho kho nhận xét."""
        if score_val is None:
            return None

        val = str(score_val).strip().upper()

        # SMAS thường dùng T/H/C
        if val in ("T", "TỐT", "HOÀN THÀNH TỐT"):
            return "T"
        if val in ("H", "HOÀN THÀNH"):
            return "H" if cap == "tieu_hoc" else "K"
        if val in ("C", "CHƯA HOÀN THÀNH", "CHT"):
            return "C" if cap == "tieu_hoc" else "CD"
        if val in ("Đ", "ĐẠT", "DAT"):
            return "T" if cap == "tieu_hoc" else "D"
        if val in ("CĐ", "CHƯA ĐẠT"):
            return "C" if cap == "tieu_hoc" else "CD"

        # Thử parse số
        try:
            num = float(str(score_val).replace(",", "."))
            if cap == "tieu_hoc":
                if num >= 9: return "T"
                elif num >= 5: return "H"
                else: return "C"
            else:
                if num >= 8.5: return "XS"
                elif num >= 6.5: return "T"
                elif num >= 5: return "K"
                elif num >= 3.5: return "D"
                else: return "CD"
        except (ValueError, TypeError):
            return None

    def _bank_fallback(self, comment_bank, cap, subject, level):
        """Tìm nhận xét fallback từ kho (môn gần giống hoặc chung)."""
        subject_lower = subject.lower()
        all_subjects = comment_bank.get_subjects(cap, "mon_hoc") if hasattr(comment_bank, 'get_subjects') else []
        for s in all_subjects:
            if subject_lower in s.lower() or s.lower() in subject_lower:
                c = comment_bank.get_random_comment(cap, "mon_hoc", s, level)
                if c:
                    return c
        return None

    def _generate_default_comment(self, score_val, short_name, subject=""):
        """Sinh nhận xét mặc định khi kho không có."""
        if score_val is None:
            return None

        val = str(score_val).strip().upper()
        name = short_name or "em"

        templates = {
            "T": [
                f"Hoàn thành tốt môn {subject}. {name} tích cực, chăm chỉ trong học tập.",
                f"{name} đạt kết quả tốt, nắm vững kiến thức môn {subject}.",
                f"{name} có tinh thần học tập tích cực, hoàn thành tốt các yêu cầu của môn {subject}.",
            ],
            "H": [
                f"Hoàn thành môn {subject}. {name} cần cố gắng hơn để đạt kết quả tốt hơn.",
                f"{name} đạt yêu cầu môn {subject}, cần tích cực phát biểu xây dựng bài.",
                f"{name} hoàn thành các nội dung cơ bản của môn {subject}.",
            ],
            "C": [
                f"Chưa hoàn thành môn {subject}. {name} cần nỗ lực nhiều hơn trong học tập.",
                f"{name} cần ôn luyện thêm để nắm vững kiến thức cơ bản môn {subject}.",
            ],
        }

        level_key = None
        if val in ("T", "TỐT", "HOÀN THÀNH TỐT"):
            level_key = "T"
        elif val in ("H", "HOÀN THÀNH", "Đ", "ĐẠT"):
            level_key = "H"
        elif val in ("C", "CHT", "CHƯA HOÀN THÀNH", "CĐ", "CHƯA ĐẠT"):
            level_key = "C"
        else:
            try:
                num = float(str(score_val).replace(",", "."))
                if num >= 9:
                    level_key = "T"
                elif num >= 5:
                    level_key = "H"
                else:
                    level_key = "C"
            except (ValueError, TypeError):
                return None

        if level_key and level_key in templates:
            return random.choice(templates[level_key])
        return None
