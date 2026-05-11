import React from 'react';
import { XIcon } from '../Icons';

export const InstructionsModal: React.FC<{ onClose: () => void }> = ({ onClose }) => {
    return (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4 animate-fade-in" onClick={onClose}>
            <div className="bg-slate-800 border border-cyan-500/30 rounded-lg shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col" onClick={e => e.stopPropagation()}>
                <div className="flex justify-between items-center p-4 border-b border-slate-700">
                    <h2 className="text-xl font-bold text-cyan-400">Hướng dẫn sử dụng ETA Connect</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-white" aria-label="Đóng hướng dẫn">
                        <XIcon className="h-6 w-6" />
                    </button>
                </div>
                <div className="p-6 overflow-y-auto custom-scrollbar text-gray-300 space-y-6">
                    <div className="space-y-3">
                        <h3 className="text-lg font-semibold text-cyan-300">I. Chế độ "Soạn Thư Đơn"</h3>
                        <p>Chế độ này giúp bạn tạo một lá thư cá nhân hóa cho từng học sinh dựa trên các nhận xét cụ thể.</p>
                        <ol className="list-decimal list-inside space-y-2 pl-4">
                            <li><strong>Chọn mục đích thư:</strong> Chọn 1 trong 3 loại: <span className="text-cyan-400">Khen ngợi</span>, <span className="text-cyan-400">Góp ý</span>, hoặc <span className="text-cyan-400">Thông báo chung</span>.</li>
                            <li><strong>Nhập tên học sinh:</strong> Điền đầy đủ họ và tên của học sinh.</li>
                            <li><strong>Thêm điểm tích cực:</strong> Nhập từng điểm tốt của học sinh vào ô "Các điểm tích cực" và nhấn Enter. Bạn có thể thêm nhiều điểm.</li>
                            <li><strong>Thêm vấn đề cần góp ý:</strong> Tương tự, nhập các vấn đề cần cải thiện vào ô "Các vấn đề cần góp ý" và nhấn Enter.</li>
                            <li><strong>Chọn giọng văn:</strong> Lựa chọn giữa <span className="text-cyan-400">Thân thiện & Gần gũi</span> hoặc <span className="text-cyan-400">Trang trọng & Chuyên nghiệp</span>.</li>
                            <li><strong>Kiểm tra thông tin người gửi:</strong> Đảm bảo tên, chức vụ, và SĐT (nếu có) của bạn là chính xác. Thông tin này sẽ được lưu lại cho lần sau.</li>
                            <li><strong>Soạn thư:</strong> Nhấn nút "Soạn Thư Thông Minh". AI sẽ phân tích thông tin và tạo một bản nháp thư ở khung bên phải.</li>
                            <li><strong>Sử dụng kết quả:</strong> Bạn có thể đọc, chỉnh sửa, và nhấn nút <span className="text-cyan-400">Copy</span> để sao chép nội dung thư.</li>
                        </ol>
                    </div>
                    <div className="space-y-3">
                        <h3 className="text-lg font-semibold text-cyan-300">II. Chế độ "Soạn Thư Hàng Loạt"</h3>
                        <p>Chế độ này cho phép bạn tạo nhanh thư cho nhiều học sinh cùng lúc từ danh sách có sẵn (ví dụ: file Excel).</p>
                        <ol className="list-decimal list-inside space-y-2 pl-4">
                            <li><strong>Chuẩn bị dữ liệu:</strong> Trong file Excel, chuẩn bị 2 cột: Cột A là <span className="text-cyan-400">Tên học sinh</span>, Cột B là <span className="text-cyan-400">Đánh giá</span> (VD: Hoàn thành tốt, Hoàn thành, Chưa hoàn thành).</li>
                            <li><strong>Copy & Dán:</strong> Quét chọn và sao chép (Ctrl+C) 2 cột dữ liệu từ Excel. Sau đó, dán (Ctrl+V) vào ô nhập liệu lớn trong ứng dụng.</li>
                            <li><strong>Phân tích dữ liệu:</strong> Nhấn nút "Phân Tích Dữ Liệu". Hệ thống sẽ tự động đọc và phân loại học sinh vào 3 nhóm: <span className="text-green-400">Hoàn thành tốt</span>, <span className="text-blue-400">Hoàn thành</span>, và <span className="text-yellow-400">Cần cố gắng</span>.</li>
                            <li><strong>Kiểm tra danh sách:</strong> Xem lại danh sách học sinh đã được phân loại. Các dòng dữ liệu không hợp lệ sẽ được thông báo.</li>
                            <li><strong>Tạo toàn bộ thư:</strong> Nhấn nút "Tạo Toàn Bộ Thư". AI sẽ lần lượt soạn thư cho tất cả học sinh trong danh sách. Quá trình này có thể mất vài phút tùy vào số lượng.</li>
                            <li><strong>Xem và sao chép kết quả:</strong> Các lá thư sau khi tạo xong sẽ hiện ra bên dưới. Bạn có thể xem lại và sao chép nội dung của từng thư một cách riêng biệt.</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    );
};
