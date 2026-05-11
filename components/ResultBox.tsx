
import React, { useState } from 'react';
import { ClipboardIcon, CheckIcon, LoaderIcon } from './Icons';

interface ResultBoxProps {
    title: string;
    content: string;
    isLoading: boolean;
}

export const ResultBox: React.FC<ResultBoxProps> = ({ title, content, isLoading }) => {
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = () => {
        if (!content) return;
        navigator.clipboard.writeText(content).then(() => {
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 2000);
        });
    };

    return (
        <div className="relative flex-1 flex flex-col bg-slate-900/70 rounded-lg border border-slate-700 p-4 h-full">
            <div className="flex justify-between items-center mb-2 flex-shrink-0">
                <h4 className="text-md font-semibold text-cyan-300">{title}</h4>
                <button 
                    onClick={handleCopy} 
                    disabled={!content || isLoading} 
                    className="p-2 rounded-md hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all" 
                    title="Copy"
                >
                    {isCopied ? <CheckIcon className="h-4 w-4 text-green-400" /> : <ClipboardIcon className="h-4 w-4 text-gray-400" />}
                </button>
            </div>
            <div className="flex-grow w-full bg-transparent text-gray-300 text-sm whitespace-pre-wrap overflow-y-auto pr-2 custom-scrollbar">
                {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                        <LoaderIcon className="animate-spin text-cyan-500 h-8 w-8"/>
                    </div>
                ) : (
                    content || <span className="text-gray-500 italic">Kết quả sẽ hiển thị tại đây...</span>
                )}
            </div>
        </div>
    );
};
