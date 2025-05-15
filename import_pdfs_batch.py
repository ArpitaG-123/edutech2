import json
import os
from utils import extract_text_from_pdf

# Directory containing PDFs
pdf_dir = os.path.join('static', 'textbooks')
pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

with open('textbooks.json', 'r', encoding='utf-8') as f:
    textbooks = json.load(f)

for pdf_filename in pdf_files:
    print(f'\nProcessing: {pdf_filename}')
    state = input('  Enter state: ')
    grade = input('  Enter grade: ')
    subject = input('  Enter subject: ')
    chapter = input('  Enter chapter: ')
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    text = extract_text_from_pdf(pdf_path)
    textbooks.setdefault(state, {}).setdefault(grade, {}).setdefault(subject, {})[chapter] = text
    print(f'  Imported {pdf_filename} to textbooks.json under {state} > {grade} > {subject} > {chapter}')

with open('textbooks.json', 'w', encoding='utf-8') as f:
    json.dump(textbooks, f, ensure_ascii=False, indent=2)

print('\nBatch import complete!') 