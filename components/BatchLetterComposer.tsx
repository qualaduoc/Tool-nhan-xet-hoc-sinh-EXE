
import React, { useState } from 'react';
import { TeacherInfo, AnalyzedStudents, BatchResult, StudentStatus } from '../types';
import { generateBatchLetter } from '../services/geminiService';
import { StudentList } from './StudentList';
import { BatchResultItem } from './BatchResultItem';
import { LoaderIcon, ListChecksIcon, BotIcon } from './Icons';

interface BatchLetterComposerProps {
    teacherInfo: TeacherInfo;
}

const BatchLetterComposer: React.FC<BatchLetterComposerProps> = ({ teacherInfo }) => {
    const [pastedData, setPastedData] = useState('');
    const [analyzedStudents, setAnalyzedStudents] = useState<AnalyzedStudents | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState('');
    const [batchResults, setBatchResults] = useState<BatchResult[]>([]);
    const [progress, setProgress] = useState(0);

    const handleAnalyze = () => {
        setIsAnalyzing(true);
        setError('');
        setAnalyzedStudents(null);
        setBatchResults([]);
        try {
            const rows = pastedData.trim().split('\n').filter(row => row.trim() !== '');
            const students: AnalyzedStudents = { excellent: [], completed: [], incomplete: [], invalid: [] };
            rows.forEach(row => {
                const parts = row.split('\t');
                const name = parts[0]?.trim();
                const status = parts[1]?.trim();
                if (name && status) {
                    const trimmedStatus = status.toLowerCase();
                    if (trimmedStatus.includes('hoàn thành tốt')) students.excellent.push(name);
                    else if (trimmedStatus.includes('chưa hoàn thành')) students.incomplete.push(name);
                    else if (trimmedStatus.includes('hoàn thành')) students.completed.push(name);
                    else students.invalid.push({ name, status });
                } else if (name) {
                     students.invalid.push({ name, status: status || "Thiếu đánh giá" });
                }
            });
            if (students.excellent.length === 0 && students.completed.length === 0 && students.incomplete.length === 0) {
                throw new Error("Không tìm thấy dữ liệu hợp lệ. Vui lòng kiểm tra định dạng: Cột A là Tên, Cột B là Đánh giá.");
            }
            setAnalyzedStudents(students);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setIsAnalyzing(false);
        }
    };
    
    const handleGenerateBatch = async () => {
        if (!analyzedStudents) {
            setError("Vui lòng phân tích dữ liệu trước khi tạo thư.");
            return;
        }
        setIsLoading(true);
        setError('');
        setBatchResults([]);
        setProgress(0);

        const allStudents = [
            ...analyzedStudents.excellent.map(name => ({ name, type: StudentStatus.EXCELLENT })),
            ...analyzedStudents.completed.map(name => ({ name, type: StudentStatus.COMPLETED })),
            ...analyzedStudents.incomplete.map(name => ({ name, type: StudentStatus.INCOMPLETE }))
        ];

        const totalStudents = allStudents.length;

        for (let i = 0; i < totalStudents; i++) {
            const student = allStudents[i];
            try {
                const content = await generateBatchLetter(student.name, student.type, teacherInfo);
                setBatchResults(prev => [...prev, { name: student.name, content, type: student.type }]);
            } catch (e: any) {
                setBatchResults(prev => [...prev, { name: student.name, content: `Lỗi khi tạo thư: ${e.message}`, type: StudentStatus.ERROR }]);
            }
            setProgress(i + 1);
        }
        
        setIsLoading(false);
    };

    const totalStudentCount = analyzedStudents ? analyzedStudents.excellent.length + analyzedStudents.completed.length + analyzedStudents.incomplete.length : 0;

    return (
        <div className="flex flex-col gap-6 animate-fade-in">
            <div className="bg-slate-800/50 p-6 rounded-lg border border-cyan-500/10">
                <h2 className="text-xl font-bold text-cyan-400 pb-3">Bước 1: Nhập dữ liệu từ Excel</h2>
                <textarea 
                    value={pastedData}
                    onChange={e => setPastedData(e.target.value)}
                    placeholder="Mở file Excel, chọn 2 cột (Tên học sinh, Đánh giá), sau đó copy (Ctrl+C) và dán (Ctrl+V) vào đây."
                    className="w-full h-40 bg-slate-900 border border-slate-600 rounded-md p-3 text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500 custom-scrollbar"
                />
                <button onClick={handleAnalyze} disabled={isAnalyzing || !pastedData} className="mt-4 px-6 py-2 bg-cyan-700 text-white font-semibold rounded-md hover:bg-cyan-600 flex items-center justify-center gap-2 disabled:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
                    {isAnalyzing ? <LoaderIcon className="animate-spin h-5 w-5"/> : <ListChecksIcon className="h-5 w-5"/>} {isAnalyzing ? 'Đang phân tích...' : 'Phân Tích Dữ Liệu'}
                </button>
            </div>

            {analyzedStudents && (
                <div className="bg-slate-800/50 p-6 rounded-lg border border-cyan-500/10 animate-fade-in">
                    <h2 className="text-xl font-bold text-cyan-400 pb-3">Bước 2: Kiểm tra & Tạo thư</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <StudentList title="Hoàn thành tốt" students={analyzedStudents.excellent} status={StudentStatus.EXCELLENT}/>
                        <StudentList title="Hoàn thành" students={analyzedStudents.completed} status={StudentStatus.COMPLETED}/>
                        <StudentList title="Cần cố gắng" students={analyzedStudents.incomplete} status={StudentStatus.INCOMPLETE}/>
                    </div>
                     {analyzedStudents.invalid.length > 0 && <p className="text-red-400 text-sm mt-4">Cảnh báo: {analyzedStudents.invalid.length} dòng dữ liệu không hợp lệ đã bị bỏ qua.</p>}
                    <button onClick={handleGenerateBatch} disabled={isLoading || totalStudentCount === 0} className="mt-6 w-full max-w-md mx-auto py-3 bg-cyan-600 text-white font-bold rounded-md hover:bg-cyan-500 flex items-center justify-center gap-2 disabled:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed text-base transition-all">
                        {isLoading ? <LoaderIcon className="animate-spin h-5 w-5" /> : <BotIcon className="h-5 w-5" />} {isLoading ? `Đang tạo ${progress}/${totalStudentCount} thư...` : 'Tạo Toàn Bộ Thư'}
                    </button>
                </div>
            )}
            
            {(isLoading || batchResults.length > 0) && (
                <div className="bg-slate-800/50 p-6 rounded-lg border border-cyan-500/10 animate-fade-in">
                    <h2 className="text-xl font-bold text-cyan-400 pb-3">Bước 3: Kết quả</h2>
                    <div className="space-y-4">
                        {batchResults.map((result, index) => <BatchResultItem key={index} result={result} />)}
                        {isLoading && batchResults.length === 0 && <div className="flex justify-center p-8"><LoaderIcon className="animate-spin text-cyan-400 h-8 w-8"/></div>}
                    </div>
                </div>
            )}
            {error && <p className="text-red-400 text-lg mt-4 text-center">{error}</p>}
        </div>
    );
};

export default BatchLetterComposer;
