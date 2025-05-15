import json
import os
from utils import extract_text_from_pdf

# User: set these variables for your import
pdf_filename = '6 math1.pdf'  # The PDF file in static/textbooks/
state = 'Karnataka'
grade = 'Primary'
subject = 'Math'
chapter = 'Numbers'

pdf_path = os.path.join('static', 'textbooks', pdf_filename)
text = extract_text_from_pdf(pdf_path)

with open('textbooks.json', 'r', encoding='utf-8') as f:
    textbooks = json.load(f)

# Insert or update the content
textbooks.setdefault(state, {}).setdefault(grade, {}).setdefault(subject, {})[chapter] = text

with open('textbooks.json', 'w', encoding='utf-8') as f:
    json.dump(textbooks, f, ensure_ascii=False, indent=2)

print(f"Imported {pdf_filename} to textbooks.json under {state} > {grade} > {subject} > {chapter}") 