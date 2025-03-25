import gradio as gr
import tempfile
import os
from pathlib import Path
from io import BytesIO
from settings import (
    respond,
    generate_random_string,
    reset_interview,
    generate_interview_report,
    generate_report_from_file,
    interview_history,
    question_count,
    language,
    total_questions,
    translate_text  # Import the new translate_text function
)
from ai_config import convert_text_to_speech, transcribe_audio
from prompt_instructions import get_interview_initial_message_sarah, get_interview_initial_message_aaron

# Global variables
temp_audio_files = []
initial_audio_path = None
selected_interviewer = "Sarah"
audio_enabled = False  # Audio output disabled by default
selected_language = "English"  # Default language

def reset_interview_action(voice, total_questions_value, language_choice):
    global question_count, interview_history, selected_interviewer, selected_language
    selected_interviewer = voice
    selected_language = language_choice  # Set language from dropdown
    question_count = 0
    interview_history.clear()

    if voice == "Sarah":
        initial_message_english = get_interview_initial_message_sarah(selected_language, total_questions_value)
        voice_setting = "alloy"
    else:
        initial_message_english = get_interview_initial_message_aaron(selected_language, total_questions_value)
        voice_setting = "onyx"

    # Translate initial message to selected language
    initial_message = translate_text(initial_message_english, selected_language, "english")

    # Only generate audio if audio_enabled is True
    audio_output = None
    if audio_enabled:
        initial_audio_buffer = BytesIO()
        convert_text_to_speech(initial_message, initial_audio_buffer, voice_setting)
        initial_audio_buffer.seek(0)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_audio_path = temp_file.name
            temp_file.write(initial_audio_buffer.getvalue())
        temp_audio_files.append(temp_audio_path)
        audio_output = gr.Audio(value=temp_audio_path, label=voice, autoplay=True, visible=False)
    else:
        audio_output = gr.Audio(value=None, label=voice, visible=False)

    return (
        [{"role": "assistant", "content": initial_message}],
        audio_output,
        ""  # Reset textbox value, keeping it editable
    )

def create_app():
    global initial_audio_path, selected_interviewer, audio_enabled, selected_language

    with gr.Blocks(title="AI Medical Interviewer") as demo:
        gr.Markdown(
            """
            # Medical Interviewer
            This chatbot conducts medical interviews based on medical knowledge.
            The interviewer will prepare a medical report based on the interview.
            """
        )

        with gr.Tab("Interview"):
            with gr.Row():
                reset_button = gr.Button("Start Interview", size='sm', scale=1)
                end_button = gr.Button("End Interview", size='sm', scale=1)
                with gr.Accordion("Settings", open=False):
                    audio_toggle = gr.Checkbox(label="Enable Audio Output", value=False)
                    interviewer_dropdown = gr.Dropdown(
                        choices=["Sarah", "Aaron"],
                        label="Interviewer",
                        value="Sarah"
                    )
                    language_dropdown = gr.Dropdown(
                        choices=["English", "Spanish", "French", "German", "Italian", "Hindi"],  # Added Hindi
                        label="Language",
                        value="English"
                    )
                    questions_dropdown = gr.Dropdown(
                        choices=[str(i) for i in range(10, 26)],
                        label="Number of Questions",
                        value="10"  # Default value set to 10
                    )

            with gr.Row():
                audio_output = gr.Audio(
                    label="Sarah",
                    scale=3,
                    autoplay=True,
                    visible=False,
                    show_download_button=False,
                )

            chatbot = gr.Chatbot(
                value=[],
                label="Medical Interview📋",
                type='messages',
                height=300
            )
            with gr.Row():
                msg = gr.Textbox(label="Type your message here...", scale=3, interactive=True)
                audio_input = gr.Audio(sources=["microphone"], label="Record your message", type="filepath", scale=1)
            send_button = gr.Button("Send")
            pdf_output = gr.File(label="Download Report", visible=False)

            def user(user_message, audio, history):
                if audio is not None:
                    user_message = transcribe_audio(audio)  # Transcribe audio in selected language
                # Translate user input from selected language to English
                translated_message = translate_text(user_message, "English", selected_language) if user_message else ""
                return "", None, history + [{"role": "user", "content": translated_message}]

            def bot_response(chatbot, message):
                global question_count, temp_audio_files, selected_interviewer, audio_enabled, selected_language
                question_count += 1

                last_user_message = chatbot[-1]["content"] if chatbot and chatbot[-1]["role"] == "user" else message

                voice = "alloy" if selected_interviewer == "Sarah" else "onyx"
                # Pass selected_language to respond for translation
                response, audio_path = respond(chatbot, last_user_message, voice, selected_interviewer, audio_enabled, selected_language)

                # Response is already translated in respond function
                for bot_message in response:
                    chatbot.append({"role": "assistant", "content": bot_message[1]})

                # Process audio only if audio_enabled is True and an audio_path is returned
                if audio_enabled and audio_path:
                    with open(audio_path, 'rb') as audio_file:
                        audio_buffer = BytesIO(audio_file.read())
                    temp_audio_path = audio_path
                    audio_output = gr.Audio(value=temp_audio_path, label=selected_interviewer, autoplay=True, visible=False)
                else:
                    audio_output = gr.Audio(value=None, label=selected_interviewer, visible=False)

                if question_count >= total_questions:
                    conclusion_message_english = "Thank you for participating in this interview. We have reached the end of our session. I hope this conversation has been helpful. Take care!"
                    conclusion_message = translate_text(conclusion_message_english, selected_language, "english")
                    chatbot.append({"role": "assistant", "content": conclusion_message})

                    if audio_enabled:
                        conclusion_audio_buffer = BytesIO()
                        convert_text_to_speech(conclusion_message, conclusion_audio_buffer, voice)
                        conclusion_audio_buffer.seek(0)
                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                            temp_audio_path = temp_file.name
                            temp_file.write(conclusion_audio_buffer.getvalue())
                        temp_audio_files.append(temp_audio_path)
                        audio_output = gr.Audio(value=temp_audio_path, label=selected_interviewer, autoplay=True, visible=False)

                    report_content, pdf_path = generate_interview_report(interview_history, selected_language)
                    chatbot.append({"role": "assistant", "content": f"Interview Report:\n\n{report_content}"})

                    return chatbot, audio_output, gr.File(visible=True, value=pdf_path), ""

                return chatbot, audio_output, gr.File(visible=False), ""

            def start_interview(interviewer, questions, language):
                global total_questions
                total_questions = int(questions)  # Update the global total_questions from dropdown
                return reset_interview_action(interviewer, total_questions, language)

            def end_interview(chatbot):
                end_message_english = "The interview has been ended by the user."
                end_message = translate_text(end_message_english, selected_language, "english")
                chatbot.append({"role": "assistant", "content": end_message})
                return chatbot, gr.Audio(visible=False), ""

            def update_settings(audio_status, interviewer_choice, language_choice, questions_choice):
                global audio_enabled, selected_interviewer, selected_language, total_questions
                audio_enabled = audio_status
                selected_interviewer = interviewer_choice
                selected_language = language_choice
                total_questions = int(questions_choice)
                return reset_interview_action(selected_interviewer, total_questions, selected_language)

            # Event handlers
            reset_button.click(
                start_interview,
                inputs=[interviewer_dropdown, questions_dropdown, language_dropdown],
                outputs=[chatbot, audio_output, msg]
            )

            end_button.click(
                end_interview,
                inputs=[chatbot],
                outputs=[chatbot, audio_output, msg]
            )

            send_button.click(
                fn=user,
                inputs=[msg, audio_input, chatbot],
                outputs=[msg, audio_input, chatbot]
            ).then(
                fn=bot_response,
                inputs=[chatbot, msg],
                outputs=[chatbot, audio_output, pdf_output, msg]
            )

            audio_toggle.change(
                update_settings,
                inputs=[audio_toggle, interviewer_dropdown, language_dropdown, questions_dropdown],
                outputs=[chatbot, audio_output, msg]
            )
            interviewer_dropdown.change(
                update_settings,
                inputs=[audio_toggle, interviewer_dropdown, language_dropdown, questions_dropdown],
                outputs=[chatbot, audio_output, msg]
            )
            language_dropdown.change(
                update_settings,
                inputs=[audio_toggle, interviewer_dropdown, language_dropdown, questions_dropdown],
                outputs=[chatbot, audio_output, msg]
            )
            questions_dropdown.change(
                update_settings,
                inputs=[audio_toggle, interviewer_dropdown, language_dropdown, questions_dropdown],
                outputs=[chatbot, audio_output, msg]
            )

        with gr.Tab("Upload Document"):
            gr.Markdown('Please upload a document that contains content written about a patient or by the patient.')
            file_input = gr.File(label="Upload a TXT, PDF, or DOCX file")
            language_input = gr.Dropdown(
                choices=["English", "Spanish", "French", "German", "Italian", "Hindi"],  # Added Hindi
                label="Select Language",
                value="English"
            )
            generate_button = gr.Button("Generate Report")
            report_output = gr.Textbox(label="Generated Report", lines=10, visible=False)
            pdf_output = gr.File(label="Download Report", visible=False)

            def generate_report_and_pdf(file, language):
                report_content, pdf_path = generate_report_from_file(file, language)
                return (
                    gr.update(value=report_content, visible=True),
                    gr.update(value=pdf_path, visible=True)
                )

            generate_button.click(
                generate_report_and_pdf,
                inputs=[file_input, language_input],
                outputs=[report_output, pdf_output]
            )

        with gr.Tab("Description"):
            with open('hf/appendix/description.txt', 'r', encoding='utf-8') as file:
                description_txt = file.read()
            gr.Markdown(description_txt)
            gr.Image("hf/appendix/diagram.png", label="System Architecture", width=600)

    return demo

def cleanup():
    global temp_audio_files, initial_audio_path
    for audio_file in temp_audio_files:
        if os.path.exists(audio_file):
            os.unlink(audio_file)
    temp_audio_files.clear()

    if initial_audio_path and os.path.exists(initial_audio_path):
        os.unlink(initial_audio_path)

if __name__ == "__main__":
    app = create_app()
    try:
        app.launch(server_name="0.0.0.0", server_port=7860)

    finally:
        cleanup()