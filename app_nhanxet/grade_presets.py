# grade_presets.py - Mẫu nhận xét theo cấp học (TT27/TT22)
# Nguyên tắc: Mỗi mức dùng từ chỉ mức độ riêng biệt để phân biệt rõ ràng
# - Mức cao nhất: "luôn luôn", "rất", "xuất sắc", "nổi bật", "thành thạo"
# - Mức giữa: "tương đối", "cơ bản", "ổn định"
# - Mức thấp: "cần", "chưa", "hạn chế"

GRADE_PRESETS = {
    "tieu_hoc": {
        "label": "Tiểu học (TT27/2020)",
        "numeric": {
            "level1": {
                "name": "Hoàn thành tốt",
                "code": "T",
                "min": 9.0,
                "templates": [
                    "Luôn luôn hoàn thành xuất sắc nhiệm vụ học tập, nắm rất vững kiến thức",
                    "Rất tích cực phát biểu xây dựng bài, luôn đạt kết quả cao",
                    "Em luôn chủ động trong học tập, thể hiện năng lực nổi bật",
                    "Nắm rất vững kiến thức, luôn vận dụng thành thạo vào thực hành",
                    "Luôn hoàn thành xuất sắc các bài kiểm tra, rất đáng khen",
                    "Em rất chăm chỉ và sáng tạo, luôn đạt kết quả vượt trội",
                    "Tiếp thu bài rất nhanh, luôn vận dụng kiến thức linh hoạt",
                    "Luôn tích cực tham gia mọi hoạt động, kết quả rất xuất sắc",
                    "Em luôn thể hiện năng lực vượt trội, rất đáng ghi nhận",
                    "Rất chăm chỉ tự học, luôn hoàn thành vượt yêu cầu môn học",
                    "Luôn luôn đạt kết quả cao, có tinh thần tự giác rất tốt",
                    "Em rất nổi bật trong học tập, luôn là tấm gương cho các bạn",
                    "Nắm kiến thức rất chắc chắn, luôn hoàn thành tốt mọi bài tập",
                    "Luôn luôn tích cực, rất sáng tạo trong các hoạt động học tập",
                    "Em rất xuất sắc, luôn duy trì thành tích học tập ổn định ở mức cao",
                ]
            },
            "level2": {
                "name": "Hoàn thành",
                "code": "H",
                "min": 5.0,
                "templates": [
                    "Hoàn thành nhiệm vụ học tập, nắm được kiến thức cơ bản",
                    "Em đạt yêu cầu môn học, cần cố gắng hơn để tiến bộ",
                    "Nắm được kiến thức cơ bản, cần rèn luyện thêm kỹ năng",
                    "Có cố gắng trong học tập, cần chăm chỉ hơn nữa",
                    "Hoàn thành các bài tập, cần nỗ lực để đạt kết quả tốt hơn",
                    "Em tiếp thu bài ở mức cơ bản, cần tích cực hơn",
                    "Hoàn thành yêu cầu môn học, cần phát huy tinh thần học tập",
                    "Kết quả ở mức hoàn thành, em cần ôn tập thêm ở nhà",
                    "Em có cố gắng, cần chú ý lắng nghe bài giảng hơn",
                    "Đạt yêu cầu cơ bản, cần rèn luyện để nâng cao kết quả",
                    "Hoàn thành nhiệm vụ, em cần chủ động hơn trong học tập",
                    "Có tiến bộ trong học tập, cần duy trì và phát huy",
                    "Em đã hoàn thành môn học, cần luyện tập nhiều hơn",
                    "Kết quả ổn định, em cần nỗ lực hơn để đạt mức tốt",
                    "Hoàn thành bài kiểm tra, cần chú trọng ôn bài thường xuyên",
                ]
            },
            "level3": {
                "name": "Chưa hoàn thành",
                "code": "C",
                "min": 0,
                "templates": [
                    "Chưa hoàn thành yêu cầu môn học, cần được hỗ trợ thêm",
                    "Em cần cố gắng nhiều hơn, tích cực ôn tập bài cũ",
                    "Chưa nắm vững kiến thức cơ bản, cần rèn luyện thêm",
                    "Kết quả chưa đạt yêu cầu, em cần sự giúp đỡ của thầy cô và gia đình",
                    "Cần chú ý lắng nghe bài giảng và làm bài tập đầy đủ",
                    "Em chưa hoàn thành nhiệm vụ học tập, cần nỗ lực hơn",
                    "Chưa đạt yêu cầu, cần ôn tập và rèn luyện thường xuyên",
                    "Em cần được phụ đạo thêm để nắm vững kiến thức",
                    "Kết quả chưa đạt, gia đình cần phối hợp hỗ trợ em",
                    "Chưa hoàn thành, em cần tập trung và chăm chỉ hơn",
                ]
            }
        },
        "text": {
            "dat": {
                "name": "Hoàn thành",
                "values": ["T", "H", "Đ", "đ", "D", "d", "Dat", "dat"],
                "templates": [
                    "Hoàn thành nhiệm vụ học tập",
                    "Tích cực tham gia hoạt động, đạt yêu cầu",
                    "Em đạt yêu cầu môn học, có tinh thần học tập tốt",
                    "Hoàn thành tốt các hoạt động học tập",
                    "Em tham gia tích cực, hoàn thành nhiệm vụ",
                ]
            },
            "chuadat": {
                "name": "Chưa hoàn thành",
                "values": ["C", "CĐ", "cđ", "CD", "KĐ"],
                "templates": [
                    "Chưa hoàn thành yêu cầu, cần cố gắng thêm",
                    "Em cần tích cực hơn trong hoạt động học tập",
                    "Chưa đạt yêu cầu, cần sự hỗ trợ của thầy cô",
                ]
            }
        }
    },

    "thcs": {
        "label": "THCS (TT22/2021)",
        "numeric": {
            "level1": {
                "name": "Giỏi",
                "code": "G",
                "min": 8.0,
                "templates": [
                    "Luôn nắm rất vững kiến thức, hoàn thành xuất sắc nhiệm vụ học tập",
                    "Rất tích cực trong mọi hoạt động, luôn đạt kết quả cao",
                    "Em luôn chủ động tìm tòi, thể hiện năng lực nổi bật",
                    "Nắm rất chắc kiến thức, luôn vận dụng linh hoạt và sáng tạo",
                    "Luôn hoàn thành xuất sắc các bài kiểm tra, rất đáng khen",
                    "Em rất tích cực phát biểu, luôn là tấm gương học tập tốt",
                    "Có tư duy rất tốt, luôn giải quyết vấn đề nhanh và chính xác",
                    "Luôn luôn đạt thành tích cao, rất chăm chỉ và nghiêm túc",
                    "Em luôn thể hiện năng lực vượt trội, kết quả rất đáng ghi nhận",
                    "Rất chủ động tự học, luôn tìm hiểu sâu kiến thức bài học",
                    "Luôn hoàn thành vượt yêu cầu, có tinh thần tự giác rất cao",
                    "Em rất nổi bật trong lớp, luôn duy trì kết quả ổn định ở mức giỏi",
                    "Luôn vận dụng rất tốt lý thuyết vào thực hành, sáng tạo trong bài làm",
                    "Rất chăm chỉ và có phương pháp học tập tốt, luôn đạt kết quả xuất sắc",
                    "Em luôn luôn tích cực, rất xứng đáng được tuyên dương",
                ]
            },
            "level2": {
                "name": "Khá",
                "code": "K",
                "min": 6.5,
                "templates": [
                    "Nắm tương đối tốt kiến thức, cần phát huy hơn nữa",
                    "Có cố gắng trong học tập, kết quả khá ổn định",
                    "Hoàn thành nhiệm vụ học tập, cần nỗ lực thêm để đạt mức giỏi",
                    "Em đạt kết quả khá, cần chủ động hơn trong học tập",
                    "Nắm kiến thức tương đối, cần rèn luyện thêm kỹ năng",
                    "Kết quả khá, em cần ôn tập thường xuyên hơn",
                    "Có tinh thần học tập, cần tích cực phát biểu hơn",
                    "Em cần cải thiện kỹ năng làm bài để đạt kết quả tốt hơn",
                    "Hoàn thành bài kiểm tra ở mức khá, cần cố gắng thêm",
                    "Có cố gắng nhưng chưa đều, cần duy trì nỗ lực học tập",
                    "Em đạt mức khá, có tiềm năng tiến bộ nếu chăm chỉ hơn",
                    "Kết quả tương đối ổn định, em cần phấn đấu để đạt mức giỏi",
                    "Nắm được bài nhưng chưa sâu, cần đầu tư thời gian ôn tập",
                    "Có tiến bộ so với đầu năm, cần phát huy",
                    "Em cần chú ý làm bài tập về nhà để củng cố kiến thức",
                ]
            },
            "level3": {
                "name": "Đạt",
                "code": "Đ",
                "min": 5.0,
                "templates": [
                    "Đạt yêu cầu cơ bản, cần nỗ lực hơn trong học tập",
                    "Kết quả ở mức trung bình, em cần cố gắng thêm",
                    "Nắm được một phần kiến thức, cần ôn tập nhiều hơn",
                    "Em cần chú ý lắng nghe và ghi chép bài đầy đủ",
                    "Đạt yêu cầu nhưng chưa vững, cần rèn luyện thêm",
                    "Kết quả chưa cao, em cần tích cực hơn trong học tập",
                    "Cần chăm chỉ làm bài tập để nâng cao kết quả",
                    "Em đạt mức trung bình, cần sự hỗ trợ để tiến bộ",
                    "Hoàn thành ở mức cơ bản, cần ôn bài thường xuyên",
                    "Em cần tập trung hơn trong giờ học để tiếp thu tốt hơn",
                ]
            },
            "level4": {
                "name": "Chưa đạt",
                "code": "CĐ",
                "min": 0,
                "templates": [
                    "Chưa đạt yêu cầu môn học, cần được hỗ trợ thêm",
                    "Kết quả còn hạn chế, em cần cố gắng rất nhiều",
                    "Chưa nắm vững kiến thức cơ bản, cần ôn tập và phụ đạo",
                    "Em cần sự giúp đỡ của thầy cô và gia đình để cải thiện",
                    "Kết quả còn yếu, cần rèn luyện nhiều hơn để đạt yêu cầu",
                    "Chưa hoàn thành nhiệm vụ, cần nỗ lực và tập trung hơn",
                    "Em cần tập trung học tập và ôn bài thường xuyên",
                    "Chưa đạt yêu cầu, cần tích cực cải thiện kết quả",
                    "Kết quả chưa đạt, gia đình cần phối hợp hỗ trợ em",
                    "Em cần được phụ đạo thêm để nắm vững kiến thức cơ bản",
                ]
            }
        },
        "text": {
            "dat": {
                "name": "Đạt",
                "values": ["Đ", "đ", "Dat", "dat", "D", "d"],
                "templates": [
                    "Đạt yêu cầu môn học, tích cực tham gia hoạt động",
                    "Hoàn thành nhiệm vụ học tập",
                    "Em đạt yêu cầu, có tinh thần học tập tốt",
                    "Tham gia tích cực các hoạt động, đạt yêu cầu",
                    "Hoàn thành tốt nhiệm vụ, có ý thức tự giác",
                ]
            },
            "chuadat": {
                "name": "Chưa đạt",
                "values": ["CĐ", "cđ", "CD", "KĐ"],
                "templates": [
                    "Chưa đạt yêu cầu, cần cố gắng thêm",
                    "Em cần tích cực hơn trong hoạt động học tập",
                    "Chưa hoàn thành yêu cầu, cần sự hỗ trợ thêm",
                ]
            }
        }
    },

    "thpt": {
        "label": "THPT (TT22/2021)",
        "numeric": {
            "level1": {
                "name": "Tốt",
                "code": "T",
                "min": 8.0,
                "templates": [
                    "Luôn nắm rất vững kiến thức, hoàn thành xuất sắc nhiệm vụ học tập",
                    "Rất tích cực và chủ động, luôn thể hiện năng lực vượt trội",
                    "Có tư duy phân tích rất tốt, luôn đạt kết quả cao",
                    "Em luôn chủ động tìm tòi, rất tích cực trong việc mở rộng kiến thức",
                    "Luôn hoàn thành xuất sắc các bài kiểm tra, có ý thức tự học rất cao",
                    "Nắm rất chắc kiến thức, luôn vận dụng thành thạo vào thực hành",
                    "Luôn luôn đạt kết quả tốt, rất xứng đáng được ghi nhận",
                    "Em rất nổi bật trong lớp, luôn là tấm gương học tập cho các bạn",
                    "Rất chăm chỉ và sáng tạo, luôn hoàn thành vượt yêu cầu môn học",
                    "Luôn đạt kết quả xuất sắc, thể hiện sự nỗ lực rất đáng khen",
                    "Em có tư duy logic rất tốt, luôn giải quyết vấn đề linh hoạt",
                    "Luôn duy trì kết quả ổn định ở mức cao, rất đáng tuyên dương",
                    "Rất tích cực tham gia mọi hoạt động, luôn đạt thành tích cao",
                    "Luôn thể hiện năng lực tự học và nghiên cứu rất tốt",
                    "Em luôn luôn tiến bộ, rất chủ động và sáng tạo trong học tập",
                ]
            },
            "level2": {
                "name": "Khá",
                "code": "K",
                "min": 6.5,
                "templates": [
                    "Nắm tương đối tốt kiến thức, cần phát huy hơn nữa",
                    "Kết quả khá ổn định, em cần chủ động hơn trong học tập",
                    "Có cố gắng, cần nâng cao kỹ năng phân tích và tổng hợp",
                    "Hoàn thành nhiệm vụ học tập, cần nỗ lực thêm để đạt mức tốt",
                    "Em đạt mức khá, có tiềm năng đạt kết quả tốt hơn",
                    "Cần ôn tập thường xuyên để củng cố kiến thức",
                    "Kết quả tương đối khá, em cần chú trọng rèn luyện thêm",
                    "Có tinh thần học tập, cần tích cực phát biểu hơn",
                    "Em cần đầu tư thời gian ôn tập để cải thiện kết quả",
                    "Nắm kiến thức tương đối, cần rèn kỹ năng làm bài",
                    "Có tiến bộ, cần duy trì và phấn đấu đạt mức tốt",
                    "Em cần cải thiện phương pháp học tập để đạt hiệu quả cao hơn",
                    "Kết quả tương đối ổn định, em cần phấn đấu hơn nữa",
                    "Hoàn thành bài kiểm tra ở mức khá, cần cố gắng thêm",
                    "Em có cố gắng nhưng chưa đều, cần nỗ lực hơn",
                ]
            },
            "level3": {
                "name": "Đạt",
                "code": "Đ",
                "min": 5.0,
                "templates": [
                    "Đạt yêu cầu cơ bản, cần nỗ lực hơn trong học tập",
                    "Kết quả ở mức trung bình, em cần cố gắng thêm",
                    "Nắm được một phần kiến thức, cần ôn tập nhiều hơn",
                    "Em cần tập trung hơn trong giờ học",
                    "Đạt yêu cầu nhưng chưa vững, cần rèn luyện thêm",
                    "Cần chăm chỉ làm bài tập để nâng cao kết quả",
                    "Em đạt mức đạt, cần cải thiện phương pháp học tập",
                    "Kết quả chưa cao, cần sự hỗ trợ để tiến bộ",
                    "Hoàn thành ở mức cơ bản, cần ôn bài thường xuyên",
                    "Em cần lập kế hoạch học tập rõ ràng để cải thiện",
                ]
            },
            "level4": {
                "name": "Chưa đạt",
                "code": "CĐ",
                "min": 0,
                "templates": [
                    "Chưa đạt yêu cầu môn học, cần được hỗ trợ thêm",
                    "Kết quả còn hạn chế, em cần nỗ lực rất nhiều để cải thiện",
                    "Chưa nắm vững kiến thức cơ bản, cần ôn tập và phụ đạo",
                    "Em cần sự giúp đỡ của thầy cô và gia đình",
                    "Kết quả còn yếu, cần rèn luyện nhiều hơn để đạt yêu cầu",
                    "Chưa hoàn thành nhiệm vụ, cần thay đổi phương pháp học",
                    "Em cần tập trung học tập và ôn bài thường xuyên hơn",
                    "Chưa đạt, cần tích cực cải thiện kết quả học tập",
                    "Gia đình cần phối hợp với nhà trường hỗ trợ em",
                    "Em cần được phụ đạo thêm để nắm vững kiến thức",
                ]
            }
        },
        "text": {
            "dat": {
                "name": "Đạt",
                "values": ["Đ", "đ", "Dat", "dat", "D", "d"],
                "templates": [
                    "Đạt yêu cầu môn học, tích cực tham gia hoạt động",
                    "Hoàn thành nhiệm vụ học tập",
                    "Em đạt yêu cầu, có ý thức tự giác trong học tập",
                    "Tham gia đầy đủ các hoạt động, đạt yêu cầu",
                    "Hoàn thành tốt nhiệm vụ được giao",
                ]
            },
            "chuadat": {
                "name": "Chưa đạt",
                "values": ["CĐ", "cđ", "CD", "KĐ"],
                "templates": [
                    "Chưa đạt yêu cầu, cần cố gắng thêm",
                    "Em cần tích cực hơn trong hoạt động học tập",
                    "Chưa hoàn thành yêu cầu, cần sự hỗ trợ thêm",
                ]
            }
        }
    }
}


def get_preset_as_settings(grade_key):
    """Chuyển preset của cấp học thành format settings cho processor"""
    preset = GRADE_PRESETS.get(grade_key, GRADE_PRESETS["thcs"])

    numeric = {}
    for level_key, level_data in preset["numeric"].items():
        numeric[level_key] = {
            "name": level_data["name"],
            "min": level_data["min"],
            "templates": level_data["templates"]
        }

    text = {}
    for text_key, text_data in preset["text"].items():
        text[text_key] = {
            "name": text_data.get("name", text_key),
            "values": text_data["values"],
            "templates": text_data["templates"]
        }

    return {"numeric": numeric, "text": text, "grade": grade_key}
