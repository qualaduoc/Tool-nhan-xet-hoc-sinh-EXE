import React from 'react';
import { XIcon, UsersIcon, ExternalLinkIcon } from '../Icons';

export const AIPopup: React.FC<{ onClose: () => void }> = ({ onClose }) => {
    const groups = [
        { name: "Nhóm ứng dụng AI vào SKKN", url: "https://zalo.me/g/yqeoug502" },
        { name: "Nhóm ứng dụng AI tạo VIDEO", url: "https://zalo.me/g/ewkybv680" },
        { name: "Nhóm ứng dụng AI vào giảng dạy", url: "https://zalo.me/g/vaubpb682" },
        { name: "Nhóm tạo Video từ SGK", url: "https://zalo.me/g/tncmdq530" },
        { name: "Nhóm nhận học liệu, học tập", url: "https://zalo.me/g/uditpr888" },
    ];
    return (
        <div className="fixed bottom-5 right-5 w-96 bg-gradient-to-br from-slate-800 to-slate-900 border border-cyan-400/50 rounded-xl shadow-2xl shadow-cyan-500/10 p-5 z-50 animate-slide-in-fade-in">
            <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                    <div className="bg-cyan-500/10 p-2 rounded-full">
                        <UsersIcon className="h-6 w-6 text-cyan-400" />
                    </div>
                    <div>
                        <h3 className="font-bold text-lg text-cyan-300">Học tập và trao đổi</h3>
                        <p className="text-sm text-gray-400">Kết nối, học hỏi và chia sẻ kinh nghiệm.</p>
                    </div>
                </div>
                <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors" aria-label="Đóng popup">
                    <XIcon className="h-6 w-6" />
                </button>
            </div>
            
            <div className="space-y-2">
                {groups.map((group, index) => (
                    <a 
                        key={index} 
                        href={group.url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="flex items-center justify-between text-sm text-gray-300 bg-slate-800/50 hover:bg-slate-700/70 hover:text-cyan-300 transition-all duration-200 rounded-md p-3 group"
                    >
                       <span>{group.name}</span>
                       <ExternalLinkIcon className="h-4 w-4 text-gray-400 group-hover:text-cyan-400 transition-colors"/>
                    </a>
                ))}
            </div>
        </div>
    );
};
