
import React, { useState } from 'react';
import { BatchResult, StudentStatus } from '../types';
import { ClipboardIcon, CheckIcon } from './Icons';

interface BatchResultItemProps {
    result: BatchResult;
}

const typeStyles: Record<StudentStatus, string> = {
    [StudentStatus.EXCELLENT]: 'border-green-500',
    [StudentStatus.COMPLETED]: 'border-blue-500',
    [StudentStatus.INCOMPLETE]: 'border-yellow-500',
    [StudentStatus.ERROR]: 'border-red-500',
};

export const BatchResultItem: React.FC<BatchResultItemProps> = ({ result }) => {
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = () => {
        if (!result.content || result.type === StudentStatus.ERROR) return;
        navigator.clipboard.writeText(result.content).then(() => {
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 2000);
        });
    };

    return (
        <div className={`bg-slate-900/50 p-4 rounded-lg border-l-4 ${typeStyles[result.type]}`}>
            <div className="flex justify-between items-center mb-2">
                <h4 className="font-bold text-cyan-300">{result.name}</h4>
                <button 
                    onClick={handleCopy} 
                    disabled={!result.content || result.type === StudentStatus.ERROR} 
                    className="p-2 rounded-md hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed" 
                    title="Copy"
                >
                    {isCopied ? <CheckIcon className="h-4 w-4 text-green-400" /> : <ClipboardIcon className="h-4 w-4 text-gray-400" />}
                </button>
            </div>
            <p className={`text-sm whitespace-pre-wrap ${result.type === StudentStatus.ERROR ? 'text-red-400' : 'text-gray-300'}`}>
                {result.content}
            </p>
        </div>
    );
};
