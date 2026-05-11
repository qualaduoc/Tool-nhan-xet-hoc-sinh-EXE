
import React, { useState } from 'react';
import { LetterType, Tone, TeacherInfo, SingleLetterFormData } from '../types';
import { generateSingleLetter } from '../services/geminiService';
import { InputField } from './InputField';
import { TagInput } from './TagInput';
import { ResultBox } from './ResultBox';
import { ThumbsUpIcon, AlertCircleIcon, UsersIcon, SendIcon, LoaderIcon } from './Icons';

interface SingleLetterComposerProps {
    teacherInfo: TeacherInfo;
    onSaveTeacherInfo: (info: TeacherInfo) => void;
}

const SingleLetterComposer: React.FC<SingleLetterComposerProps> = ({ teacherInfo, onSaveTeacherInfo }) => {
    const [formData, setFormData] = useState<SingleLetterFormData>({
        letterType: LetterType.FEEDBACK,
        studentName: '',
        positivePoints: [],
        negativePoints: [],
        tone: Tone.FRIENDLY,
    });
    const [currentPositivePoint, setCurrentPositivePoint] = useState('');
    const [currentNegativePoint, setCurrentNegativePoint] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState('');
    const [localTeacherInfo, setLocalTeacherInfo] = useState<TeacherInfo>(teacherInfo);

    const handleAddTag = (type: 'positive' | 'negative') => {
        if (type === 'positive' && currentPositivePoint.trim()) {
            setFormData(prev => ({...prev, positivePoints: [...prev.positivePoints, currentPositivePoint.trim()]}));
            setCurrentPositivePoint('');
        }
        if (type === 'negative' && currentNegativePoint.trim()) {
            setFormData(prev => ({...prev, negativePoints: [...prev.negativePoints, currentNegativePoint.trim()]}));
            setCurrentNegativePoint('');
        }
    };

    const handleRemoveTag = (type: 'positive' | 'negative', index: number) => {
        if (type === 'positive') setFormData(prev => ({...prev, positivePoints: prev.positivePoints.filter((_, i) => i !== index)}));
        if (type === 'negative') setFormData(prev => ({...prev, negativePoints: prev.negativePoints.filter((_, i) => i !== index)}));
    };

    const handleSubmit = async () => {
        if (!formData.studentName.trim()) { setError('Vui lòng nhập tên học sinh.'); return; }
        if (formData.positivePoints.length === 0 && formData.negativePoints.length === 0) { setError('Vui lòng nhập ít nhất một điểm tích cực hoặc một vấn đề cần góp ý.'); return; }
        
        setIsLoading(true); 
        setError(''); 
        setResult('');

        try {
            const content = await generateSingleLetter(formData, localTeacherInfo);
            setResult(content);
        } catch (e: any) { 
            setError(e.message || "An unknown error occurred."); 
        } finally { 
            setIsLoading(false); 
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-full animate-fade-in">
            <div className="flex flex-col gap-5 bg-slate-800/50 p-6 rounded-lg border border-cyan-500/10">
                <h2 className="text-xl font-bold text-cyan-400 border-b-2 border-cyan-500/20 pb-3">Thông Tin Soạn Thư</h2>
                <div>
                    <label className="text-sm font-medium text-gray-400 mb-2 block">1. Mục đích thư</label>
                    <div className="grid grid-cols-3 gap-2">
                        {/* FIX: Correctly iterate over enum values. The previous implementation had a type error and a runtime bug from misusing Object.values with an incorrect type cast. This now iterates directly over the enum's string values, which is cleaner and correct. */}
                        {Object.values(LetterType).map((typeValue) => (
                            <button key={typeValue} onClick={() => setFormData({...formData, letterType: typeValue})} className={`text-sm py-2 px-3 rounded-md flex items-center justify-center gap-2 transition-all ${formData.letterType === typeValue ? 'bg-cyan-600 text-white shadow-lg' : 'bg-slate-700 hover:bg-slate-600'}`}>
                                {typeValue === LetterType.PRAISE && <ThumbsUpIcon className="h-4 w-4"/>}
                                {typeValue === LetterType.FEEDBACK && <AlertCircleIcon className="h-4 w-4"/>}
                                {typeValue === LetterType.ANNOUNCEMENT && <UsersIcon className="h-4 w-4"/>}
                                {typeValue}
                            </button>
                        ))}
                    </div>
                </div>
                <InputField label="2. Tên học sinh" value={formData.studentName} onChange={e => setFormData({...formData, studentName: e.target.value})} placeholder="Ví dụ: Nguyễn Văn An" />
                <TagInput label="3. Các điểm tích cực (nhấn Enter để thêm)" tags={formData.positivePoints} inputValue={currentPositivePoint} onInputChange={setCurrentPositivePoint} onAddTag={() => handleAddTag('positive')} onRemoveTag={(index) => handleRemoveTag('positive', index)} borderColor="border-green-500" icon={<ThumbsUpIcon className="text-green-500 h-5 w-5"/>} placeholder="VD: Hăng hái phát biểu..."/>
                <TagInput label="4. Các vấn đề cần góp ý (nhấn Enter để thêm)" tags={formData.negativePoints} inputValue={currentNegativePoint} onInputChange={setCurrentNegativePoint} onAddTag={() => handleAddTag('negative')} onRemoveTag={(index) => handleRemoveTag('negative', index)} borderColor="border-yellow-500" icon={<AlertCircleIcon className="text-yellow-500 h-5 w-5"/>} placeholder="VD: Còn nói chuyện riêng..."/>
                <div>
                     <label className="text-sm font-medium text-gray-400 mb-2 block">5. Giọng văn</label>
                     <div className="flex gap-2">
                        <button onClick={() => setFormData({...formData, tone: Tone.FRIENDLY})} className={`flex-1 py-2 px-3 text-sm rounded-md transition-all ${formData.tone === Tone.FRIENDLY ? 'bg-cyan-600 text-white shadow-lg' : 'bg-slate-700 hover:bg-slate-600'}`}>Thân thiện & Gần gũi</button>
                        <button onClick={() => setFormData({...formData, tone: Tone.FORMAL})} className={`flex-1 py-2 px-3 text-sm rounded-md transition-all ${formData.tone === Tone.FORMAL ? 'bg-cyan-600 text-white shadow-lg' : 'bg-slate-700 hover:bg-slate-600'}`}>Trang trọng & Chuyên nghiệp</button>
                     </div>
                </div>
                <div className="border-t border-cyan-500/20 pt-4 space-y-3">
                    <h3 className="text-base font-semibold text-gray-300">Thông tin người gửi</h3>
                    <InputField label="Tên giáo viên / Nhà trường" value={localTeacherInfo.name} onChange={e => setLocalTeacherInfo({...localTeacherInfo, name: e.target.value})} onBlur={() => onSaveTeacherInfo(localTeacherInfo)} placeholder="Nguyễn Thành Được"/>
                    <InputField label="Chức vụ" value={localTeacherInfo.position} onChange={e => setLocalTeacherInfo({...localTeacherInfo, position: e.target.value})} onBlur={() => onSaveTeacherInfo(localTeacherInfo)} placeholder="Giáo viên chủ nhiệm lớp 5A"/>
                    <InputField label="SĐT liên hệ (tùy chọn)" value={localTeacherInfo.phone} onChange={e => setLocalTeacherInfo({...localTeacherInfo, phone: e.target.value})} onBlur={() => onSaveTeacherInfo(localTeacherInfo)} placeholder="0904059866"/>
                </div>
                <button onClick={handleSubmit} disabled={isLoading} className="w-full mt-2 py-3 bg-cyan-600 text-white font-bold rounded-md hover:bg-cyan-500 flex items-center justify-center gap-2 disabled:bg-slate-600 disabled:cursor-not-allowed disabled:opacity-50 text-base transition-all">
                    {isLoading ? <LoaderIcon className="animate-spin h-5 w-5" /> : <SendIcon className="h-5 w-5" />} {isLoading ? 'Đang soạn thư...' : 'Soạn Thư Thông Minh'}
                </button>
                {error && <p className="text-red-400 text-sm mt-2 text-center">{error}</p>}
            </div>
            <div className="flex flex-col h-full min-h-[70vh] lg:min-h-0"><ResultBox title="Bản nháp thư gửi phụ huynh" content={result} isLoading={isLoading} /></div>
        </div>
    );
};

export default SingleLetterComposer;
