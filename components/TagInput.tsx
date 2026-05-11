
import React from 'react';
import { XIcon } from './Icons';

interface TagInputProps {
    label: string;
    tags: string[];
    inputValue: string;
    onInputChange: (value: string) => void;
    onAddTag: () => void;
    onRemoveTag: (index: number) => void;
    borderColor: string;
    icon: React.ReactNode;
    placeholder?: string;
}

export const TagInput: React.FC<TagInputProps> = ({ label, tags, inputValue, onInputChange, onAddTag, onRemoveTag, borderColor, icon, placeholder }) => (
    <div>
        <label className="text-sm font-medium text-gray-400 mb-2 block">{label}</label>
        <div className={`flex items-center bg-slate-900 border border-slate-600 rounded-md px-3 py-2 focus-within:ring-1 ${borderColor} focus-within:border-transparent transition-all`}>
            {icon}
            <input 
                type="text" 
                value={inputValue} 
                placeholder={placeholder} 
                onChange={e => onInputChange(e.target.value)} 
                onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); onAddTag(); }}} 
                className="flex-grow bg-transparent text-white placeholder-slate-500 focus:outline-none ml-2"
            />
        </div>
        <div className="flex flex-wrap gap-2 mt-2 min-h-[2.25rem]">
            {tags.map((tag, index) => (
                <div key={index} className="flex items-center bg-slate-700 rounded-full px-3 py-1 text-sm animate-fade-in">
                    <span>{tag}</span>
                    <button onClick={() => onRemoveTag(index)} className="ml-2 text-gray-400 hover:text-white rounded-full hover:bg-slate-600 p-0.5">
                        <XIcon className="h-3.5 w-3.5" />
                    </button>
                </div>
            ))}
        </div>
    </div>
);
