import fitz  # PyMuPDF
import re
import os
import json

# User: set these variables
pdf_filename = '6 math1.pdf'  # The PDF file in static/textbooks/
state = 'Karnataka'
grade = 'Primary'
subject = 'Math'

# Adjusted regex to match headings like '1. SOURCES 1'
heading_pattern = r'^(\d+)\.\s*([A-Z ]+\d*)$'

pdf_path = os.path.join('static', 'textbooks', pdf_filename)
doc = fitz.open(pdf_path)
chapters = {}
current_chapter = None
current_text = []
heading_regex = re.compile(heading_pattern)

for page in doc:
    text = page.get_text()
    lines = text.splitlines()
    for line in lines:
        match = heading_regex.match(line.strip())
        if match:
            # Save previous chapter
            if current_chapter and current_text:
                chapters[current_chapter] = '\n'.join(current_text).strip()
            # Start new chapter
            chapter_title = match.group(2).strip() or match.group(0).strip()
            current_chapter = chapter_title if chapter_title else match.group(0).strip()
            current_text = [line]
        else:
            if current_chapter:
                current_text.append(line)
# Save last chapter
if current_chapter and current_text:
    chapters[current_chapter] = '\n'.join(current_text).strip()

if not chapters:
    print('No chapters found. Printing first 5 lines of each page for debugging:')
    for page in doc:
        lines = page.get_text().splitlines()
        print(lines[:5])

print('Found chapters:')
for chapter in chapters:
    print(f'- {chapter}')

# Add to textbooks.json
with open('textbooks.json', 'r', encoding='utf-8') as f:
    textbooks = json.load(f)
for chapter, content in chapters.items():
    textbooks.setdefault(state, {}).setdefault(grade, {}).setdefault(subject, {})[chapter] = content
with open('textbooks.json', 'w', encoding='utf-8') as f:
    json.dump(textbooks, f, ensure_ascii=False, indent=2)
print('Chapters imported to textbooks.json!') 