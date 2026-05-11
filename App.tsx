
import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import SingleLetterComposer from './components/SingleLetterComposer';
import BatchLetterComposer from './components/BatchLetterComposer';
import { AppMode, TeacherInfo } from './types';
import { AIPopup } from './components/common/AIPopup';
import { InstructionsModal } from './components/common/InstructionsModal';


const App: React.FC = () => {
    const [activeMode, setActiveMode] = useState<AppMode>(AppMode.SINGLE);
    const [teacherInfo, setTeacherInfo] = useState<TeacherInfo>({ name: '', position: '', phone: '' });
    const [isInitialized, setIsInitialized] = useState<boolean>(false);
    const [showAIPopup, setShowAIPopup] = useState(false);
    const [showInstructions, setShowInstructions] = useState(false);

    useEffect(() => {
        try {
            const storedTeacherInfo = localStorage.getItem('eta_connect_teacher_info_v3');
            if (storedTeacherInfo) {
                setTeacherInfo(JSON.parse(storedTeacherInfo));
            }
        } catch (error) {
            console.error("Error accessing localStorage:", error);
        }
        setIsInitialized(true);
    }, []);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShowAIPopup(true);
        }, 40000); // 40 seconds

        return () => clearTimeout(timer);
    }, []);

    const handleSaveTeacherInfo = (info: TeacherInfo) => {
        setTeacherInfo(info);
        try {
            localStorage.setItem('eta_connect_teacher_info_v3', JSON.stringify(info));
        } catch (error) {
            console.error("Error saving teacher info to localStorage:", error);
        }
    };
    
    const handleShowInstructions = () => setShowInstructions(true);
    const handleCloseInstructions = () => setShowInstructions(false);

    if (!isInitialized) {
        return (
            <div className="bg-slate-900 flex justify-center items-center h-screen">
                <div className="w-12 h-12 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="bg-slate-900 text-gray-200 min-h-screen font-sans flex flex-col">
            <Header 
                activeMode={activeMode} 
                setActiveMode={setActiveMode}
                onShowInstructions={handleShowInstructions}
            />
            
            <main className="flex-grow container mx-auto p-4 md:p-8">
                {activeMode === AppMode.SINGLE ? (
                    <SingleLetterComposer 
                        teacherInfo={teacherInfo}
                        onSaveTeacherInfo={handleSaveTeacherInfo}
                    /> 
                ) : (
                    <BatchLetterComposer 
                        teacherInfo={teacherInfo}
                    />
                )}
            </main>
            <Footer />
            
            {showAIPopup && <AIPopup onClose={() => setShowAIPopup(false)} />}
            {showInstructions && <InstructionsModal onClose={handleCloseInstructions} />}
        </div>
    );
};

export default App;