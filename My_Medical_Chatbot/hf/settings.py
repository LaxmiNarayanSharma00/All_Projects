# settings.py
import traceback
from datetime import datetime
from pathlib import Path
import os
import random
import string
import tempfile
import re
import io
import PyPDF2
import docx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from ai_config import load_model, openai_api_key, convert_text_to_speech
from knowledge_retrieval import setup_knowledge_retrieval, generate_report, get_next_response

# Initialize settings
current_datetime = datetime.now()
human_readable_datetime = current_datetime.strftime("%B %d, %Y at %H:%M")
current_date = current_datetime.strftime("%Y-%m-%d")

# Global variables
total_questions = 10  # Default number of questions, user can change this via UI
question_count = 0
interview_history = []
last_audio_path = None
initial_audio_path = None
language = None  # Will be set via UI
knowledge_base_connected = False
llm = None
interview_retrieval_chain = None
report_retrieval_chain = None
combined_retriever = None

# Initialize the model and retrieval chain
try:
    llm = load_model(openai_api_key)
    # Note: setup_knowledge_retrieval will be called later with language from UI
    knowledge_base_connected = True
    print("Successfully connected to the language model.")
except Exception as e:
    print(f"Error initializing the model: {str(e)}")
    knowledge_base_connected = False
    print("Falling back to basic mode without knowledge base.")

# Define the four fixed questions in English
FIXED_QUESTIONS = [
    "What is your name?",
    "What is your age?",
    "Where do you live?",
    "What is your current occupation?"
]

# Translation function using OpenAI LLM
def translate_text(text, target_language, source_language="english"):
    if target_language.lower() == source_language.lower():
        return text
    prompt = f"Translate the following text from {source_language} to {target_language}: {text}"
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Fallback to original text if translation fails

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def respond(chatbot, message, voice, selected_interviewer, audio_enabled, selected_language):
    global question_count, interview_history, combined_retriever, last_audio_path, initial_audio_path, language, interview_retrieval_chain, report_retrieval_chain

    if not isinstance(chatbot, list):
        chatbot = []
    if not isinstance(message, str):
        message = str(message)

    # Translate user input from selected language to English
    translated_message = translate_text(message, "english", selected_language)
    question_count += 1
    interview_history.append(f"A{question_count}: {translated_message}")
    history_str = "\n".join(interview_history)
    print("Processing question", question_count)

    try:
        if knowledge_base_connected:
            if question_count == 1:
                # Set language from UI parameter and initialize retrieval chain
                language = selected_language.strip().lower()
                interview_retrieval_chain, report_retrieval_chain, combined_retriever = setup_knowledge_retrieval(
                    llm, language, selected_interviewer, total_questions)
                question_english = FIXED_QUESTIONS[0]  # "What is your name?"
            elif question_count <= 4:
                question_english = FIXED_QUESTIONS[question_count - 1]  # Use fixed questions for 1-4
            else:
                if question_count % 5 == 0:
                    summary = generate_summary(interview_history, language)
                    interview_history.append(f"Summary at Q{question_count}: {summary}")
                    history_str = summary
                else:
                    history_str = "\n".join(interview_history)

                if question_count < total_questions:
                    question_english = get_next_response(interview_retrieval_chain, translated_message, history_str, question_count, total_questions)
                else:
                    question_english = "Thank you, I will now prepare your report."
                    speech_file_path = None

            # Translate question to selected language
            question = translate_text(question_english, selected_language)

            # Generate audio only if audio_enabled is True
            speech_file_path = None
            if question and question_count < total_questions and audio_enabled:
                random_suffix = generate_random_string()
                speech_file_path = Path(__file__).parent / f"question_{question_count}_{random_suffix}.mp3"
                convert_text_to_speech(question, speech_file_path, voice)  # Audio in selected language
                print(f"Question {question_count} saved as audio at {speech_file_path}")
                if last_audio_path and os.path.exists(last_audio_path):
                    os.remove(last_audio_path)
                last_audio_path = speech_file_path

        else:
            # Fallback mode (no knowledge base)
            if question_count <= 4:
                question_english = FIXED_QUESTIONS[question_count - 1]
            else:
                question_english = f"Can you elaborate on that?"
            question = translate_text(question_english, selected_language)

            speech_file_path = None
            if question_count < total_questions and audio_enabled:
                speech_file_path = Path(__file__).parent / f"question_{question_count}.mp3"
                convert_text_to_speech(question, speech_file_path, voice)
                print(f"Question {question_count} saved as audio at {speech_file_path}")
                if last_audio_path and os.path.exists(last_audio_path):
                    os.remove(last_audio_path)
                last_audio_path = speech_file_path

        if question_count < total_questions:
            interview_history.append(f"Q{question_count + 1}: {question_english}")  # Store English version for LLM

        response = [(None, question)]
        return response, speech_file_path

    except Exception as e:
        print(f"Error in retrieval chain: {str(e)}")
        return [(None, f"Error occurred: {str(e)}")], None

def generate_summary(history, language):
    """Generate a concise summary of the conversation so far."""
    combined_history = "\n".join(history)
    summary_prompt = f"""Summarize the following interview history concisely in {language}, focusing on key points:
    {combined_history}"""
    
    result = llm.invoke(summary_prompt)
    return result.content if hasattr(result, 'content') else str(result)

def reset_interview():
    """Reset the interview state."""
    global question_count, interview_history, last_audio_path, initial_audio_path
    question_count = 0
    interview_history = []
    if last_audio_path and os.path.exists(last_audio_path):
        os.remove(last_audio_path)
    last_audio_path = None
    initial_audio_path = None

def read_file(file):
    if file is None:
        return "No file uploaded"

    if isinstance(file, str):
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()

    if hasattr(file, 'name'):  # Check if it's a file-like object
        if file.name.endswith('.txt'):
            return file.content
        elif file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.content))
            return "\n".join(page.extract_text() for page in pdf_reader.pages)
        elif file.name.endswith('.docx'):
            doc = docx.Document(io.BytesIO(file.content))
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        else:
            return "Unsupported file format"

    return "Unable to read file"

def generate_report_from_file(file, language):
    try:
        file_content = read_file(file)
        if file_content in ["No file uploaded", "Unsupported file format", "Unable to read file"]:
            return file_content, None

        file_content = file_content[:100000]
        report_language = language.strip().lower() if language else "english"
        print(f"Generating report in language: {report_language}")

        # Reinitialize the report chain with the new language
        _, report_retrieval_chain, _ = setup_knowledge_retrieval(llm, report_language)

        result = report_retrieval_chain.invoke({
            "input": "Please provide a clinical report based on the following content:",
            "history": file_content,
            "language": report_language
        })
        report_content = result.get("answer", "Unable to generate report due to insufficient information.")
        pdf_path = create_pdf(report_content)
        return report_content, pdf_path
    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}", None

def generate_interview_report(interview_history, language):
    try:
        report_language = language.strip().lower() if language else "english"
        print(f"Preferred report language: {report_language}")
        _, report_retrieval_chain, _ = setup_knowledge_retrieval(llm, report_language)

        result = report_retrieval_chain.invoke({
            "input": "Please provide a clinical report based on the following interview:",
            "history": "\n".join(interview_history),
            "language": report_language
        })
        report_content = result.get("answer", "Unable to generate report due to insufficient information.")
        pdf_path = create_pdf(report_content)
        return report_content, pdf_path
    except Exception as e:
        return f"An error occurred while generating the report: {str(e)}", None

def create_pdf(content):
    random_string = generate_random_string()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_report_{random_string}.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()

    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], alignment=TA_JUSTIFY)

    flowables = []
    for line in content.split('\n'):
        parts = re.split(r'(\*\*.*?\*\*)', line)
        paragraph_parts = []
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                bold_text = part.strip('**')
                paragraph_parts.append(Paragraph(bold_text, bold_style))
            else:
                paragraph_parts.append(Paragraph(part, normal_style))
        flowables.extend(paragraph_parts)
        flowables.append(Spacer(1, 12))

    doc.build(flowables)
    return temp_file.name