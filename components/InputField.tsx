
import React from 'react';

type InputFieldProps = {
    label: string;
} & React.InputHTMLAttributes<HTMLInputElement>;

export const InputField: React.FC<InputFieldProps> = ({ label, ...props }) => (
    <div>
        <label className="block text-sm font-medium text-gray-400 mb-2">{label}</label>
        <input {...props} className="w-full bg-slate-900 border border-slate-600 rounded-md px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 transition-all" />
    </div>
);
