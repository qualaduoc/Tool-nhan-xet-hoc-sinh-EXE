
import React from 'react';
import { AppMode } from '../types';
import { UserIcon, FileUpIcon, HelpCircleIcon } from './Icons';

interface HeaderProps {
    activeMode: AppMode;
    setActiveMode: (mode: AppMode) => void;
    onShowInstructions: () => void;
}

export const Header: React.FC<HeaderProps> = ({ activeMode, setActiveMode, onShowInstructions }) => (
    <header className="bg-slate-900/80 backdrop-blur-sm border-b border-cyan-500/20 p-4 shadow-lg sticky top-0 z-10">
        <div className="container mx-auto flex justify-between items-center">
            <div className="flex items-center gap-3">
                <img src="https://dangkyhoc.com/logo.png" alt="ETA Logo" className="h-8 w-auto" />
                <h1 className="text-xl md:text-2xl font-bold text-cyan-400 tracking-wider">ETA Connect</h1>
            </div>
            <div className="flex items-center gap-4">
                <button 
                    onClick={onShowInstructions}
                    className="px-3 py-1.5 text-sm font-semibold rounded-md flex items-center gap-2 transition-all duration-200 text-gray-300 bg-slate-800 hover:bg-slate-700"
                    aria-label="Xem hướng dẫn sử dụng"
                >
                    <HelpCircleIcon className="h-4 w-4"/> Hướng dẫn
                </button>
                <div className="bg-slate-800 p-1 rounded-lg flex gap-1">
                    <button 
                        onClick={() => setActiveMode(AppMode.SINGLE)} 
                        className={`px-3 py-1.5 text-sm font-semibold rounded-md flex items-center gap-2 transition-all duration-200 ${activeMode === AppMode.SINGLE ? 'bg-cyan-600 text-white shadow-md' : 'text-gray-300 hover:bg-slate-700'}`}
                    >
                        <UserIcon className="h-4 w-4"/>Soạn Thư Đơn
                    </button>
                    <button 
                        onClick={() => setActiveMode(AppMode.BATCH)} 
                        className={`px-3 py-1.5 text-sm font-semibold rounded-md flex items-center gap-2 transition-all duration-200 ${activeMode === AppMode.BATCH ? 'bg-cyan-600 text-white shadow-md' : 'text-gray-300 hover:bg-slate-700'}`}
                    >
                        <FileUpIcon className="h-4 w-4"/>Soạn Thư Hàng Loạt
                    </button>
                </div>
            </div>
        </div>
    </header>
);
