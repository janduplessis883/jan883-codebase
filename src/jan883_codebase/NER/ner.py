import PyPDF2
from tqdm import tqdm

# Function to read PDF content
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in tqdm(range(len(reader.pages))):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

# Replace 'your_pdf_file.pdf' with your actual PDF file path
pdf_content = read_pdf('/Users/janduplessis/Library/CloudStorage/OneDrive-NHS/PatientPlus/patient4.pdf')
# pdf_content = read_pdf('/Volumes/JanBackupDrive/eBooks/NLP Transformers.pdf')

from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_large-v2.1")

# pii_categories = [
#     "Anatomical Structures",
#     "Diseases and Disorders",
#     "Symptoms and Signs",
#     "Medications and Drugs",
#     "Procedures and Treatments",
#     "Laboratory Tests",
#     "Microorganisms",
#     "Chemical Substances",
#     "Genes and Proteins",
#     "Medical Devices",
#     "Patient Demographics",
#     "Body Measurements",
#     "Temporal Expressions",
#     "Dosages and Quantities",
#     "Clinical Findings",
#     "Allergens",
#     "Medical Professionals",
#     "Healthcare Facilities",
#     "Medical Specialties",
#     "Body Fluids and Substances",
#     "Pathological Processes",
#     "Lifestyle Factors",
#     "Family History",
#     "Medical Abbreviations",
#     "Adverse Events and Complications",
#     "Research Entities",
#     "Treatment Outcomes",
#     "Geographical Locations",
#     "Health Indicators",
#     "SNOMED CT",
# ]

pii_categories = [
    "Laboratory Tests",
    "Diseases and Disorders",
    "Microorganisms",
    "Body Measurements",
    "quantity with unit",
    "date time",
]

import re
import textwrap

def chunk_text(text, max_length=1000):
    return textwrap.wrap(text, max_length, break_long_words=False, replace_whitespace=False)

def remove_pii_from_chunk(chunk_text):
    entities = model.predict_entities(chunk_text, pii_categories, flat_ner=False, threshold=0.3)

    # Sort entities by 'start' in reverse to handle index consistency during replacements
    entities = sorted(entities, key=lambda x: x['start'], reverse=True)

    identified_entities = []

    for entity in entities:
        entity_label = entity.get('label', 'REDACTED').upper().replace(' ', '_')
        entity_value = chunk_text[entity['start']:entity['end']]
        identified_entities.append(f"{entity_label} 🔸 {entity_value}")
        replacement_text = f"[{entity_label}]"
        chunk_text = chunk_text[:entity['start']] + replacement_text + chunk_text[entity['end']:]

    for identified in identified_entities:
        print(identified)

    return re.sub(r'\*{2,}', '[REDACTED]', chunk_text)

# Chunk the input text
chunks = chunk_text(pdf_content)

# Process each chunk to remove PII
redacted_chunks = [remove_pii_from_chunk(chunk) for chunk in chunks]

# Combine the redacted chunks back into a single text
result = '\n'.join(redacted_chunks)
