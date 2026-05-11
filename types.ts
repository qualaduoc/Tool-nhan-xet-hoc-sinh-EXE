
export enum AppMode {
    SINGLE = 'single',
    BATCH = 'batch',
}

export enum LetterType {
    PRAISE = 'Khen ngợi',
    FEEDBACK = 'Góp ý',
    ANNOUNCEMENT = 'Thông báo chung',
}

export enum Tone {
    FRIENDLY = 'Thân thiện',
    FORMAL = 'Trang trọng',
}

export interface TeacherInfo {
    name: string;
    position: string;
    phone: string;
}

export interface SingleLetterFormData {
    letterType: LetterType;
    studentName: string;
    positivePoints: string[];
    negativePoints: string[];
    tone: Tone;
}

export interface AnalyzedStudents {
    excellent: string[];
    completed: string[];
    incomplete: string[];
    invalid: { name: string; status: string }[];
}

export enum StudentStatus {
    EXCELLENT = 'excellent',
    COMPLETED = 'completed',
    INCOMPLETE = 'incomplete',
    ERROR = 'error',
}

export interface BatchResult {
    name: string;
    content: string;
    type: StudentStatus;
}
