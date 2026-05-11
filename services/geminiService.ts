
import { GoogleGenAI } from "@google/genai";
import { SingleLetterFormData, TeacherInfo, StudentStatus } from '../types';

const apiKey = import.meta.env.VITE_API_KEY;

if (!apiKey) {
    throw new Error("VITE_API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey });
const model = 'gemini-2.5-flash';

const systemPrompt = "You are a pedagogical communication expert AI, specializing in drafting letters to parents. Your tone must be professional, constructive, positive, and tactful. Always start by praising the student's good points before mentioning areas for improvement (the sandwich method). Conclude with a call for positive collaboration and a professional signature.";

const formatSignature = (teacherInfo: TeacherInfo): string => {
    return `
Trân trọng,
${teacherInfo.name || '[Tên giáo viên/nhà trường]'}
${teacherInfo.position || '[Chức vụ]'}
${teacherInfo.phone ? `SĐT: ${teacherInfo.phone}` : ''}`.trim();
};

export const generateSingleLetter = async (formData: SingleLetterFormData, teacherInfo: TeacherInfo): Promise<string> => {
    const signature = formatSignature(teacherInfo);
    const userQuery = `
Instruction: Compose a letter to a parent based on the following information:
- Letter Type: ${formData.letterType}
- Student's Name: ${formData.studentName}
- Positive points to praise: ${formData.positivePoints.length > 0 ? formData.positivePoints.map(p => `- ${p}`).join('\n') : "(None)"}
- Issues for feedback/improvement: ${formData.negativePoints.length > 0 ? formData.negativePoints.map(p => `- ${p}`).join('\n') : "(None)"}
- Required tone: ${formData.tone}
- Signature at the end of the letter:
${signature}

Please write a complete, coherent, natural, and professional letter. Do not include asterisks or markdown formatting in the final output.
    `.trim();

    try {
        const response = await ai.models.generateContent({
            model,
            contents: userQuery,
            config: {
                systemInstruction: systemPrompt,
            }
        });
        return response.text.trim();
    } catch (error) {
        console.error("Error during Gemini API call for single letter:", error);
        throw new Error("Failed to generate letter. Please check the console for details.");
    }
};

export const generateBatchLetter = async (studentName: string, status: StudentStatus, teacherInfo: TeacherInfo): Promise<string> => {
    const signature = formatSignature(teacherInfo);
    let specificInstruction = '';
    switch (status) {
        case StudentStatus.EXCELLENT:
            specificInstruction = 'Write a very warm letter to PRAISE and RECOGNIZE the student\'s excellent efforts.';
            break;
        case StudentStatus.COMPLETED:
            specificInstruction = 'Write a letter to PRAISE the student\'s efforts, while also ENCOURAGING them to continue developing further.';
            break;
        case StudentStatus.INCOMPLETE:
            specificInstruction = 'Write a very TACTFUL and constructive letter. Start with a small compliment, then GENTLY PROVIDE FEEDBACK on areas needing improvement, and conclude with confidence and a call for family cooperation.';
            break;
        default:
            return "Invalid student status provided.";
    }

    const userQuery = `
Instruction: Compose a letter to a parent based on the following information:
- Student's Name: ${studentName}
- General Assessment: ${status}
- Content Requirement: ${specificInstruction}
- Signature at the end of the letter:
${signature}

Please write a complete, coherent, natural, and professional letter. Do not include asterisks or markdown formatting in the final output.
    `.trim();

    try {
        const response = await ai.models.generateContent({
            model,
            contents: userQuery,
            config: {
                systemInstruction: systemPrompt,
            }
        });
        return response.text.trim();
    } catch (error) {
        console.error(`Error during Gemini API call for batch letter (${studentName}):`, error);
        throw new Error(`Failed to generate letter for ${studentName}.`);
    }
};
