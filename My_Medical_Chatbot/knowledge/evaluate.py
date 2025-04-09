import json
import os
from typing import List
import PyPDF2

# Directory where PDF reports and text chats are stored
REPORT_DIR = "report_da"  # Update this to your actual folder path

def get_report(patient_text: str) -> str:
    """
    Retrieve the chatbot's report from a PDF file based on patient_text.
    Assumes PDF filenames include a unique identifier (e.g., timestamp) linked to patient_text.
    """
    # Generate a simple identifier from patient_text (e.g., first few words hashed)
    # In practice, you might use a timestamp or ID from your chatbot's logic
    identifier = "_".join(patient_text.split()[:3]).lower().replace(" ", "_")
    
    # Look for a matching PDF file in the directory
    for filename in os.listdir(REPORT_DIR):
        if filename.endswith(".pdf") and identifier in filename:
            pdf_path = os.path.join(REPORT_DIR, filename)
            try:
                # Extract text from PDF
                with open(pdf_path, "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                
                # Assuming report has "Symptoms:" followed by a list
                if "Symptoms:" in text:
                    symptom_line = text.split("Symptoms:")[1].split("\n")[0].strip()
                    return f"Symptoms: {symptom_line}"
                else:
                    return "Symptoms: "  # Return empty symptom list if not found
            except Exception as e:
                print(f"Error reading PDF {pdf_path}: {e}")
                return "Symptoms: "
    
    # If no matching report is found
    print(f"No report found for identifier: {identifier}")
    return "Symptoms: "

def parse_symptoms(report_text: str) -> List[str]:
    # Simple parsing assuming "Symptoms:" followed by comma-separated list
    if "Symptoms:" in report_text:
        symptoms_str = report_text.split("Symptoms:")[1].strip()
        return [s.strip() for s in symptoms_str.split(",") if s.strip()]
    return []

def map_symptoms_to_umls(symptoms: List[str]) -> List[str]:
    # Dummy mapping; replace with actual UMLS mapping or API call
    umls_mapping = {
        "cough": "C0010200",
        "fever": "C0015967",
        "headache": "C0018681",
        "fatigue": "C0015672"
    }
    return [umls_mapping.get(symptom.lower(), "") for symptom in symptoms]

# Load MediTOD dataset (adjust path as needed)
with open("path/to/medi_tod_dataset.json", "r") as f:
    data = json.load(f)

total_TP = 0
total_FP = 0
num_dialogues = 0

for dialogue in data["dialogues"]:
    patient_utterances = [turn["text"] for turn in dialogue["turns"] if turn["speaker"] == "patient"]
    patient_text = " ".join(patient_utterances)
    report_text = get_report(patient_text)
    system_symptoms = parse_symptoms(report_text)
    system_umls_ids = map_symptoms_to_umls(system_symptoms)
    ground_truth_positive_umls = [symptom["umls_id"] for symptom in dialogue["symptoms"] if symptom["status"] == "positive"]
    TP = len(set(system_umls_ids) & set(ground_truth_positive_umls))
    FP = len([s for s in system_umls_ids if s not in ground_truth_positive_umls])
    total_TP += TP
    total_FP += FP
    num_dialogues += 1

if total_TP + total_FP > 0:
    average_precision = total_TP / (total_TP + total_FP)
else:
    average_precision = 1.0  # Handle edge case
print(f"Average precision: {average_precision:.2f}")