from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        session['user_name'] = request.form['user_name']
        session['school_type'] = request.form['school_type']
        session['state'] = request.form['state']
        session['grade'] = request.form['grade']
        session['avatar'] = request.form['avatar']
        return redirect(url_for('select_subject'))
    return render_template('onboarding.html')

@app.route('/select-subject', methods=['GET', 'POST'])
def select_subject():
    state = session.get('state')
    grade = session.get('grade')
    if not state or not grade:
        return redirect(url_for('onboarding'))

    # Load subjects from syllabus.json
    syllabus_path = os.path.join(os.path.dirname(__file__), 'syllabus.json')
    with open(syllabus_path, 'r', encoding='utf-8') as f:
        syllabus = json.load(f)
    subjects = syllabus.get(state, {}).get(grade, [])

    if request.method == 'POST':
        selected_subject = request.form.get('subject')
        if selected_subject in subjects:
            session['subject'] = selected_subject
            return redirect(url_for('syllabus'))
    return render_template('select_subject.html', subjects=subjects)

@app.route('/syllabus')
def syllabus():
    subject = session.get('subject')
    if not subject:
        return redirect(url_for('select_subject'))
    return f"<h1>Syllabus for {subject}</h1>"

@app.route('/chapters')
def chapters():
    state = session.get('state')
    grade = session.get('grade')
    subject = session.get('subject')
    if not (state and grade and subject):
        return redirect(url_for('onboarding'))
    syllabus_path = os.path.join(os.path.dirname(__file__), 'syllabus.json')
    with open(syllabus_path, 'r', encoding='utf-8') as f:
        syllabus = json.load(f)
    chapters = syllabus.get(state, {}).get(grade, {}).get(subject, [])
    return render_template('chapters.html', subject=subject, chapters=chapters)

@app.route('/lesson/<int:chapter_id>')
def lesson(chapter_id):
    state = session.get('state')
    grade = session.get('grade')
    subject = session.get('subject')
    if not (state and grade and subject):
        return redirect(url_for('onboarding'))
    syllabus_path = os.path.join(os.path.dirname(__file__), 'syllabus.json')
    with open(syllabus_path, 'r', encoding='utf-8') as f:
        syllabus = json.load(f)
    chapters = syllabus.get(state, {}).get(grade, {}).get(subject, [])
    if 0 <= chapter_id < len(chapters):
        chapter_name = chapters[chapter_id]
    else:
        chapter_name = 'Unknown Chapter'
        return f"<h1>Lesson: {chapter_name}</h1>"

    # Load lesson data from lessons.json
    lessons_path = os.path.join(os.path.dirname(__file__), 'lessons.json')
    lesson_data = None
    if os.path.exists(lessons_path):
        with open(lessons_path, 'r', encoding='utf-8') as f:
            lessons = json.load(f)
        lesson_data = lessons.get(state, {}).get(grade, {}).get(subject, {}).get(chapter_name, None)
    return render_template('lesson.html', chapter_name=chapter_name, lesson=lesson_data)

@app.route('/upload-voice', methods=['POST'])
def upload_voice():
    if 'audio' not in request.files:
        return 'No audio file', 400
    audio = request.files['audio']
    if audio.filename == '':
        return 'No selected file', 400
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, audio.filename)
    audio.save(save_path)
    return 'OK', 200

def generate_animated_video(text):
    # Stub: In production, call an AI video generation API
    # Here, return a placeholder video URL (could be a static video)
    return url_for('static', filename='videos/placeholder.mp4')

def generate_audio_summary(text, language):
    # Stub: In production, call a TTS API
    # Here, return a placeholder audio URL (could be a static audio)
    return url_for('static', filename='audios/placeholder.mp3')

@app.route('/modules/<subject>/<chapter>')
def module_video(subject, chapter):
    state = session.get('state')
    grade = session.get('grade')
    language = session.get('language', 'en')
    if not (state and grade and subject and chapter):
        return redirect(url_for('onboarding'))
    # Load chapter text from textbooks.json
    textbooks_path = os.path.join(os.path.dirname(__file__), 'textbooks.json')
    with open(textbooks_path, 'r', encoding='utf-8') as f:
        textbooks = json.load(f)
    content_text = textbooks.get(state, {}).get(grade, {}).get(subject, {}).get(chapter, None)
    video_url = None
    audio_url = None
    if content_text:
        video_url = generate_animated_video(content_text)
        audio_url = generate_audio_summary(content_text, language)
    return render_template('module_video.html', subject=subject, chapter=chapter, content_text=content_text, video_url=video_url, audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True) 