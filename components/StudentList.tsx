
import React from 'react';
import { StudentStatus } from '../types';
import { ThumbsUpIcon, CheckIcon, AlertCircleIcon } from './Icons';

interface StudentListProps {
    title: string;
    students: string[];
    status: StudentStatus;
}

const statusConfig = {
    [StudentStatus.EXCELLENT]: { color: 'text-green-400', icon: <ThumbsUpIcon className="h-5 w-5"/> },
    [StudentStatus.COMPLETED]: { color: 'text-blue-400', icon: <CheckIcon className="h-5 w-5"/> },
    [StudentStatus.INCOMPLETE]: { color: 'text-yellow-400', icon: <AlertCircleIcon className="h-5 w-5"/> },
    [StudentStatus.ERROR]: { color: 'text-red-400', icon: <AlertCircleIcon className="h-5 w-5"/> },
};

export const StudentList: React.FC<StudentListProps> = ({ title, students, status }) => {
    const config = statusConfig[status];

    return (
        <div className="bg-slate-900/50 p-3 rounded-md">
            <h3 className={`font-semibold ${config.color} flex items-center gap-2 mb-2`}>
                {config.icon} {title} ({students.length})
            </h3>
            <ul className="text-sm space-y-1 max-h-32 overflow-y-auto custom-scrollbar pr-2">
                {students.length > 0 ? (
                    students.map((name, i) => <li key={i}>{name}</li>)
                ) : (
                    <li className="text-gray-500 italic">Không có</li>
                )}
            </ul>
        </div>
    );
};
