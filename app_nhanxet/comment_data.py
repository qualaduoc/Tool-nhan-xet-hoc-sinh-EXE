# comment_data.py - Ngân hàng nhận xét mặc định
# Cấu trúc: { "cap_hoc": { "loai_nhan_xet": { "mon_hoc/nhom": { "muc": [list] } } } }

import json
import os
import random

DATA_FILE = "kho_nhan_xet.json"

def get_default_data():
    """Trả về toàn bộ kho nhận xét mặc định"""
    return {
        "tieu_hoc": {
            "mon_hoc": {
                "Tiếng Việt": {
                    "T": [
                        "Em đọc to, rõ ràng, lưu loát và diễn cảm. Viết đúng chính tả, chữ viết đẹp, trình bày sạch sẽ.",
                        "Em có khả năng đọc hiểu tốt, nắm vững nội dung bài học. Bài viết sáng tạo, diễn đạt mạch lạc.",
                        "Em tiếp thu bài nhanh, hăng hái phát biểu xây dựng bài. Vốn từ phong phú, viết câu đúng ngữ pháp.",
                        "Em đọc diễn cảm, trả lời câu hỏi chính xác. Có khả năng viết đoạn văn hay, giàu cảm xúc.",
                        "Em nghe hiểu tốt, nói rõ ràng, mạch lạc. Chữ viết sạch đẹp, đúng quy cách.",
                        "Em có năng khiếu viết văn, bài viết có cảm xúc chân thực. Đọc diễn cảm, phát âm chuẩn.",
                    ],
                    "H": [
                        "Em đọc đúng, rõ ràng. Viết đúng chính tả nhưng cần rèn thêm chữ viết đẹp hơn.",
                        "Em nắm được nội dung bài đọc, trả lời câu hỏi tương đối chính xác. Cần luyện viết đoạn văn dài hơn.",
                        "Em hoàn thành bài tập đúng yêu cầu. Cần tích cực hơn trong phát biểu và đọc diễn cảm.",
                        "Em biết nghe và nói theo chủ đề. Bài viết đạt yêu cầu, cần chú ý thêm về dấu câu.",
                        "Em có cố gắng trong học tập, đọc tương đối lưu loát. Cần rèn thêm kỹ năng viết đoạn văn.",
                    ],
                    "C": [
                        "Em cần rèn luyện đọc thêm ở nhà để đọc lưu loát hơn. Chữ viết cần cẩn thận, đúng mẫu.",
                        "Em chưa nắm vững nội dung bài đọc, cần tập trung hơn trong giờ học. Rèn viết chính tả nhiều hơn.",
                        "Em cần cố gắng nhiều hơn trong việc luyện đọc và viết. Gia đình hỗ trợ em đọc bài ở nhà.",
                    ],
                },
                "Toán": {
                    "T": [
                        "Em nắm vững kiến thức, tính toán nhanh và chính xác. Giải toán có lời văn rõ ràng, đúng phương pháp.",
                        "Em tư duy toán học tốt, sáng tạo trong giải bài tập. Luôn hoàn thành xuất sắc các bài kiểm tra.",
                        "Em hiểu bài nhanh, vận dụng tốt các công thức. Tích cực tham gia phát biểu xây dựng bài.",
                        "Em có khả năng tư duy logic tốt, giải quyết bài tập nhanh nhẹn. Trình bày bài sạch đẹp.",
                        "Em nắm chắc bảng cửu chương, tính nhẩm nhanh. Giải bài tập ứng dụng thực tế rất tốt.",
                    ],
                    "H": [
                        "Em nắm được kiến thức cơ bản, kỹ năng tính toán khá. Cần chú ý hơn ở dạng bài tập vận dụng cao.",
                        "Em hoàn thành các bài tập trong chương trình. Cần rèn luyện thêm kỹ năng giải toán có lời văn.",
                        "Em có ý thức học tập, cần chú ý hơn ở bài tập nâng cao. Trình bày bài tương đối sạch sẽ.",
                        "Em biết vận dụng kiến thức vào bài tập. Cần cẩn thận hơn để tránh sai sót trong tính toán.",
                    ],
                    "C": [
                        "Em chưa nắm vững kiến thức cơ bản, cần nỗ lực nhiều hơn. Rèn luyện thêm bảng cửu chương.",
                        "Em cần được bồi dưỡng thêm kiến thức nền. Gia đình hỗ trợ em ôn bài và luyện tập ở nhà.",
                        "Kỹ năng tính toán còn yếu, cần rèn luyện viết nhiều hơn. Cần tập trung hơn trong giờ học.",
                    ],
                },
                "Tự nhiên và Xã hội": {
                    "T": [
                        "Em hứng thú tìm hiểu tự nhiên, tích cực tham gia hoạt động. Nắm vững kiến thức bài học.",
                        "Em quan sát tốt, nhận biết được các hiện tượng tự nhiên. Ham tìm hiểu thế giới xung quanh.",
                        "Em biết vận dụng kiến thức vào thực tế cuộc sống. Tích cực tham gia các hoạt động nhóm.",
                        "Em yêu thích khám phá thiên nhiên, có ý thức bảo vệ môi trường sống xung quanh.",
                    ],
                    "H": [
                        "Em nắm được kiến thức cơ bản về tự nhiên và xã hội. Cần tích cực hơn trong thảo luận nhóm.",
                        "Em biết quan sát và mô tả các sự vật hiện tượng. Cần chủ động hơn trong tìm hiểu bài.",
                        "Em hoàn thành bài học đúng yêu cầu. Cần rèn thêm kỹ năng liên hệ thực tế.",
                    ],
                    "C": [
                        "Em cần chú ý lắng nghe bài giảng hơn. Rèn luyện kỹ năng quan sát và nhận biết sự vật.",
                        "Em chưa tích cực tham gia hoạt động nhóm, cần cố gắng hơn trong học tập.",
                    ],
                },
                "Đạo đức": {
                    "T": [
                        "Em ngoan ngoãn, lễ phép với thầy cô, yêu quý bạn bè. Luôn chấp hành tốt nội quy trường lớp.",
                        "Em có cách ứng xử đúng hành vi đạo đức trong thực tiễn. Biết yêu thương và giúp đỡ mọi người.",
                        "Em lễ phép, ngoan ngoãn với ông bà, cha mẹ, kính trọng thầy cô giáo. Luôn cảm ơn và xin lỗi kịp thời.",
                        "Em tiếp thu bài tốt, biết vận dụng kiến thức đã học vào cuộc sống. Có ý thức tự giác cao.",
                    ],
                    "H": [
                        "Em nắm được nội dung bài học và biết vận dụng kiến thức vào cuộc sống.",
                        "Em biết giữ gìn vệ sinh thân thể, có ý thức bảo vệ sức khỏe. Chấp hành nội quy trường lớp.",
                        "Em hoàn thành nội dung môn học. Cần mạnh dạn hơn trong giao tiếp với bạn bè.",
                    ],
                    "C": [
                        "Em cần rèn luyện thêm ý thức chấp hành nội quy. Cần lễ phép hơn với thầy cô và bạn bè.",
                        "Em cần cố gắng hơn trong việc giữ gìn vệ sinh và bảo vệ của công.",
                    ],
                },
                "Hoạt động trải nghiệm": {
                    "T": [
                        "Em tham gia tích cực các hoạt động trải nghiệm, có tinh thần trách nhiệm và hợp tác tốt.",
                        "Em biết áp dụng kiến thức đã học vào thực tiễn qua các hoạt động trải nghiệm.",
                        "Em có tinh thần hợp tác, giúp đỡ bạn bè trong học tập. Tích cực và sáng tạo trong hoạt động.",
                        "Em rất hứng thú và chủ động khi tham gia làm việc nhóm và hoạt động thực hành.",
                        "Em biết sắp xếp góc học tập, sinh hoạt gọn gàng ngăn nắp. Biết quý trọng và tiết kiệm.",
                    ],
                    "H": [
                        "Em tham gia các hoạt động trải nghiệm đầy đủ, hoàn thành nhiệm vụ được giao.",
                        "Em biết phối hợp với bạn trong nhóm. Cần tích cực hơn trong các hoạt động tập thể.",
                        "Em hoàn thành nội dung môn học. Cần chủ động và sáng tạo hơn trong hoạt động.",
                    ],
                    "C": [
                        "Em cần tích cực tham gia các hoạt động trải nghiệm hơn. Rèn luyện kỹ năng làm việc nhóm.",
                        "Em chưa chủ động trong hoạt động, cần cố gắng và hợp tác với bạn bè nhiều hơn.",
                    ],
                },
            },
            "nlpc": {
                "nang_luc_chung": {
                    "T": [
                        "Em biết tự thực hiện tốt các nhiệm vụ học tập.",
                        "Em có khả năng tự thực hiện các nhiệm vụ học tập.",
                        "Em biết lắng nghe và tôn trọng ý kiến của bạn.",
                        "Em biết thực hiện các nhiệm vụ học tập cô giáo giao.",
                        "Em chủ động, tích cực trong học tập và sinh hoạt.",
                        "Em có ý thức tự giác cao, luôn chủ động hoàn thành bài vở đúng hạn.",
                        "Em có kỹ năng giao tiếp tốt, diễn đạt rõ ràng, lưu loát.",
                        "Em thường xuyên phát hiện và đặt được các câu hỏi có giá trị.",
                    ],
                    "D": [
                        "Em thực hiện nhiệm vụ học tập đầy đủ và đúng hạn.",
                        "Em giải quyết vấn đề học tập phù hợp với yêu cầu.",
                        "Em hợp tác tốt với bạn bè khi làm việc nhóm.",
                        "Em giải quyết được các tình huống học tập quen thuộc.",
                        "Em hoàn thành các nhiệm vụ học tập được giao.",
                        "Em biết tự thực hiện các nhiệm vụ học tập khi có hướng dẫn.",
                        "Em thân thiện, hòa đồng và biết phối hợp với bạn.",
                    ],
                    "C": [
                        "Em cần cố gắng hơn để tự hoàn thành nhiệm vụ.",
                        "Em cần rèn luyện thêm kỹ năng tự học và tự chủ.",
                        "Em cần chủ động hơn trong học tập và giao tiếp với bạn bè.",
                        "Em vẫn cần nhiều sự đôn đốc, nhắc nhở từ thầy cô và gia đình.",
                        "Em còn rụt rè, cần mạnh dạn trình bày ý kiến cá nhân.",
                    ],
                },
                "nang_luc_dac_thu": {
                    "T": [
                        "Hứng thú tìm hiểu tự nhiên, tích cực tham gia hoạt động.",
                        "Biết ứng xử thích hợp trong một số tình huống có liên quan đến vấn đề bản thân.",
                        "Thích khám phá các hoạt động, vận dụng tốt kiến thức đã học.",
                        "Em có năng lực đặc thù tốt, thể hiện qua kết quả học tập các môn.",
                        "Em phát huy tốt khả năng ngôn ngữ, tính toán và tìm hiểu khoa học.",
                    ],
                    "D": [
                        "Em nắm được kiến thức cơ bản các môn học đặc thù.",
                        "Em hoàn thành các bài tập vận dụng ở mức cơ bản.",
                        "Em có ý thức học tập, cần phát huy thêm năng lực đặc thù.",
                    ],
                    "C": [
                        "Em cần cố gắng rèn luyện thêm các kỹ năng đặc thù.",
                        "Em cần nỗ lực nhiều hơn trong việc phát triển năng lực môn học.",
                    ],
                },
                "pham_chat": {
                    "T": [
                        "Con tự tin trong học tập, trung thực, đoàn kết, yêu quý bạn bè.",
                        "Con chấp hành tốt nội quy lớp học.",
                        "Con tích cực trong học tập ở lớp.",
                        "Con ngoan ngoãn, lễ phép, biết yêu thương và giúp đỡ bạn bè.",
                        "Con có ý thức tự giác cao, luôn chấp hành tốt nội quy trường lớp.",
                        "Con chăm chỉ, trung thực và có trách nhiệm trong học tập.",
                    ],
                    "D": [
                        "Con có ý thức chấp hành nội quy, biết giữ gìn vệ sinh.",
                        "Con biết yêu thương bạn bè, hoàn thành nhiệm vụ được giao.",
                        "Con ngoan ngoãn, có cố gắng trong rèn luyện phẩm chất.",
                    ],
                    "C": [
                        "Con cần rèn luyện thêm ý thức kỷ luật và tự giác trong học tập.",
                        "Con cần chăm chỉ hơn và chấp hành tốt nội quy trường lớp.",
                    ],
                },
            },
        },
        "thcs": {
            "mon_hoc": {
                "Ngữ văn": {
                    "XS": [
                        "Cảm thụ văn học sâu sắc, bài viết sáng tạo, lập luận sắc bén.",
                        "Diễn đạt truyền cảm, bố cục chặt chẽ, văn phong đặc sắc.",
                        "Năng lực phân tích tác phẩm văn học xuất sắc, ngôn ngữ phong phú.",
                    ],
                    "T": [
                        "Cảm thụ văn học tốt, bài viết mạch lạc, diễn đạt trôi chảy.",
                        "Nắm vững phương pháp làm văn, diễn đạt trôi chảy.",
                        "Hiểu sâu nội dung tác phẩm, phân tích nhân vật tốt.",
                        "Bài viết rõ ý, từ ngữ phong phú, cảm xúc chân thực.",
                    ],
                    "K": [
                        "Diễn đạt khá, nắm vững nội dung tác phẩm đã học.",
                        "Bài viết đủ ý, cần chú ý hơn về cách dùng từ gợi cảm.",
                        "Nắm được phương pháp, cần rèn luyện thêm kỹ năng đặt câu.",
                    ],
                    "D": [
                        "Bài viết cơ bản đạt yêu cầu, cần chú ý hơn về lỗi diễn đạt.",
                        "Nắm được nội dung chính, cần rèn luyện thêm kỹ năng viết đoạn văn.",
                    ],
                    "CD": [
                        "Khả năng diễn đạt còn hạn chế, cần rèn luyện viết nhiều hơn.",
                        "Chưa nắm vững phương pháp làm văn, cần đọc thêm nhiều sách báo.",
                    ],
                },
                "Toán": {
                    "XS": [
                        "Tư duy toán học xuất sắc, giải bài sáng tạo và chính xác.",
                        "Nắm vững kiến thức nâng cao, suy luận logic sắc bén.",
                    ],
                    "T": [
                        "Nắm vững kiến thức toán học, tính toán nhanh và chính xác.",
                        "Kết quả tốt, tích cực tham gia phát biểu xây dựng bài.",
                        "Hiểu và vận dụng tốt các công thức, giải bài tập thành thạo.",
                    ],
                    "K": [
                        "Nắm được kiến thức cơ bản, kỹ năng tính toán khá.",
                        "Có ý thức học tập, cần chú ý hơn ở dạng bài tập vận dụng cao.",
                    ],
                    "D": [
                        "Đạt yêu cầu môn học, cần rèn luyện thêm kỹ năng tính toán.",
                        "Nắm được kiến thức trọng tâm, cần nỗ lực hơn ở bài tập nâng cao.",
                    ],
                    "CD": [
                        "Chưa nắm vững kiến thức cơ bản, cần nỗ lực nhiều hơn.",
                        "Kỹ năng tính toán còn yếu, cần được bồi dưỡng thêm kiến thức nền.",
                    ],
                },
                "Ngoại ngữ 1": {
                    "XS": ["Phát âm chuẩn, vốn từ phong phú, giao tiếp tự tin và lưu loát."],
                    "T": ["Nắm vững ngữ pháp, kỹ năng nghe nói đọc viết tốt."],
                    "K": ["Có cố gắng, cần rèn thêm kỹ năng nghe và nói."],
                    "D": ["Đạt yêu cầu cơ bản, cần luyện tập thêm từ vựng và ngữ pháp."],
                    "CD": ["Kiến thức còn yếu, cần bồi dưỡng thêm và luyện tập thường xuyên."],
                },
            },
            "muc_chung": {
                "XS": {
                    "diem_min": 9, "diem_max": 10, "ma": "XS",
                    "nhan_xet": [
                        "Kết quả học tập xuất sắc, nắm vững kiến thức nâng cao.",
                        "Tư duy sáng tạo, giải quyết tốt các bài tập khó.",
                        "Luôn tích cực, sáng tạo và hỗ trợ tốt bạn bè trong học tập.",
                        "Nỗ lực tuyệt vời, đạt thành tích cao nhất môn học.",
                    ],
                },
                "T": {
                    "diem_min": 8, "diem_max": 8.9, "ma": "T",
                    "nhan_xet": [
                        "Có tiến bộ rõ rệt, nắm vững kiến thức trọng tâm.",
                        "Kết quả học tập tốt, tích cực xây dựng bài.",
                        "Tư duy logic tốt, vận dụng kiến thức linh hoạt.",
                        "Chăm chỉ, sáng tạo, có tinh thần hợp tác nhóm tốt.",
                    ],
                },
                "K": {
                    "diem_min": 6.5, "diem_max": 7.9, "ma": "K",
                    "nhan_xet": [
                        "Hoàn thành tốt các nhiệm vụ học tập, có cố gắng.",
                        "Nắm được kiến thức cơ bản, cần phát huy hơn nữa.",
                        "Có ý thức học tập tốt, cần rèn luyện thêm bài tập nâng cao.",
                    ],
                },
                "D": {
                    "diem_min": 5, "diem_max": 6.4, "ma": "D",
                    "nhan_xet": [
                        "Đạt yêu cầu cơ bản, cần cố gắng thêm trong học tập.",
                        "Nắm được kiến thức trọng tâm nhưng cần rèn luyện nhiều hơn.",
                    ],
                },
                "CD": {
                    "diem_min": 0, "diem_max": 4.9, "ma": "CD",
                    "nhan_xet": [
                        "Chưa đạt yêu cầu, cần nỗ lực rèn luyện thêm nhiều.",
                        "Kiến thức còn hạn chế, cần được hỗ trợ bồi dưỡng thêm.",
                    ],
                },
            },
        },
    }


class CommentBank:
    """Quản lý kho nhận xét: load, save, thêm, xóa, random"""

    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = get_default_data()
        else:
            self.data = get_default_data()
            self.save()

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def reset(self):
        self.data = get_default_data()
        self.save()

    def get_random_comment(self, cap, loai, mon_or_nhom, muc):
        """Lấy ngẫu nhiên 1 nhận xét theo đường dẫn"""
        try:
            pool = self.data[cap][loai][mon_or_nhom][muc]
            if isinstance(pool, dict) and "nhan_xet" in pool:
                pool = pool["nhan_xet"]
            if pool:
                return random.choice(pool)
        except (KeyError, IndexError):
            pass
        return ""

    def get_comments(self, cap, loai, mon_or_nhom, muc):
        """Lấy toàn bộ nhận xét theo đường dẫn"""
        try:
            pool = self.data[cap][loai][mon_or_nhom][muc]
            if isinstance(pool, dict) and "nhan_xet" in pool:
                return pool["nhan_xet"]
            return pool if isinstance(pool, list) else []
        except (KeyError, IndexError):
            return []

    def add_comment(self, cap, loai, mon_or_nhom, muc, text):
        """Thêm 1 nhận xét mới"""
        self.data.setdefault(cap, {})
        self.data[cap].setdefault(loai, {})
        self.data[cap][loai].setdefault(mon_or_nhom, {})
        node = self.data[cap][loai][mon_or_nhom]
        if muc not in node:
            node[muc] = []
        target = node[muc]
        if isinstance(target, dict) and "nhan_xet" in target:
            target["nhan_xet"].append(text)
        elif isinstance(target, list):
            target.append(text)
        self.save()

    def remove_comment(self, cap, loai, mon_or_nhom, muc, index):
        """Xóa 1 nhận xét theo index"""
        try:
            target = self.data[cap][loai][mon_or_nhom][muc]
            if isinstance(target, dict) and "nhan_xet" in target:
                target["nhan_xet"].pop(index)
            elif isinstance(target, list):
                target.pop(index)
            self.save()
        except (KeyError, IndexError):
            pass

    def add_subject(self, cap, loai, subject_name):
        """Thêm môn học mới"""
        self.data.setdefault(cap, {})
        self.data[cap].setdefault(loai, {})
        if subject_name not in self.data[cap][loai]:
            self.data[cap][loai][subject_name] = {}
            self.save()
            return True
        return False

    def remove_subject(self, cap, loai, subject_name):
        """Xóa môn học"""
        try:
            del self.data[cap][loai][subject_name]
            self.save()
            return True
        except KeyError:
            return False
