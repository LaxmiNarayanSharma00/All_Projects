# knowledge_retrieval.py
import random
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever
from ai_config import openai_api_key
from prompt_instructions import get_interview_prompt_sarah, get_interview_prompt_aaron, get_report_prompt

def setup_knowledge_retrieval(llm, language='english', voice='Sarah', total_questions=10):
    """
    Set up the retrieval chains for interview and report generation.
    
    Args:
        llm: Language model instance
        language: Selected language for the interview (default: 'english')
        voice: Interviewer persona ('Sarah' or 'Aaron', default: 'Sarah')
        total_questions: Number of questions chosen by the user (default: 10)
    
    Returns:
        tuple: (interview_retrieval_chain, report_retrieval_chain, combined_retriever)
    """
    # Load the FAISS index with embeddings
    embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
    documents_faiss_index = FAISS.load_local(
        "knowledge/faiss_index_all_documents",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    documents_retriever = documents_faiss_index.as_retriever()

    # Combine retrievers (currently just one, but EnsembleRetriever allows future expansion)
    combined_retriever = EnsembleRetriever(retrievers=[documents_retriever])

    # Select the appropriate interview prompt based on the interviewer
    if voice == 'Sarah':
        interview_prompt = ChatPromptTemplate.from_messages([
            ("system", get_interview_prompt_sarah(language, total_questions)),
            ("human", "{input}")
        ])
    else:
        interview_prompt = ChatPromptTemplate.from_messages([
            ("system", get_interview_prompt_aaron(language, total_questions)),
            ("human", "{input}")
        ])

    # Define the report prompt
    report_prompt = ChatPromptTemplate.from_messages([
        ("system", get_report_prompt(language)),
        ("human", "Please provide a concise clinical report based on the interview.")
    ])

    # Create the chains for interview and report generation
    interview_chain = create_stuff_documents_chain(llm, interview_prompt)
    report_chain = create_stuff_documents_chain(llm, report_prompt)

    interview_retrieval_chain = create_retrieval_chain(combined_retriever, interview_chain)
    report_retrieval_chain = create_retrieval_chain(combined_retriever, report_chain)

    return interview_retrieval_chain, report_retrieval_chain, combined_retriever

def get_next_response(interview_chain, message, history, question_count, total_questions):
    """
    Generate the next question based on the patient's response and interview history.
    
    Args:
        interview_chain: The retrieval chain for generating questions
        message: The patient's last response
        history: The full interview history or a summary
        question_count: Current question number
        total_questions: Total number of questions chosen by the user
    
    Returns:
        str: The next question to ask
    """
    # If the interview is complete, signal the end
    if question_count >= total_questions:
        return "Thank you for your responses. I will now prepare a report."

    # Combine history into a string if it's a list
    combined_history = history if isinstance(history, str) else "\n".join(history)

    # Invoke the chain to generate a unique, context-aware question
    result = interview_chain.invoke({
        "input": f"Based on the patient's last response: '{message}', and considering the interview history or summary: '{combined_history}', ask a specific, detailed question that hasn’t been asked before and is relevant to the patient’s situation. Ensure the question is unique.",
        "history": combined_history,
        "question_number": question_count + 1
    })

    next_question = result.get("answer", "Could you provide more details on your current situation?")
    
    # Ensure the question is unique by checking against history
    if isinstance(history, list):
        while any(f"Q{num}: {next_question}" in combined_history for num in range(1, question_count + 1)):
            result = interview_chain.invoke({
                "input": f"The question '{next_question}' was already asked. Generate a new, unique question based on the patient's last response: '{message}' and the history or summary: '{combined_history}'",
                "history": combined_history,
                "question_number": question_count + 1
            })
            next_question = result.get("answer", "Can you tell me something new about your experience?")
    
    return next_question

def generate_report(report_chain, history, language):
    """
    Generate a clinical report based on the interview history.
    
    Args:
        report_chain: The retrieval chain for generating reports
        history: The full interview history
        language: The language for the report
    
    Returns:
        str: The generated clinical report
    """
    combined_history = "\n".join(history)

    result = report_chain.invoke({
        "input": "Please provide a clinical report based on the interview.",
        "history": combined_history,
        "language": language
    })

    return result.get("answer", "Unable to generate report due to insufficient information.")

def get_initial_question(interview_chain):
    """
    Generate the first question for the interview (optional utility function).
    
    Args:
        interview_chain: The retrieval chain for generating questions
    
    Returns:
        str: The initial question
    """
    result = interview_chain.invoke({
        "input": "What should be the first question in a clinical psychology interview?",
        "history": "",
        "question_number": 1
    })
    return result.get("answer", "Could you tell me a little bit about yourself and what brings you here today?")