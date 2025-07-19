# skill_validation_system/app.py

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
# Import tempfile to work with Vercel's temporary directory
import tempfile

# --- Vercel Deployment Configuration ---
# Check if running on Vercel, and if so, use the /tmp directory which is writable
IS_VERCEL = os.environ.get('VERCEL') == '1'
if IS_VERCEL:
    # The only writable directory on Vercel is /tmp
    TMP_DIR = '/tmp'
    UPLOAD_FOLDER = os.path.join(TMP_DIR, 'static/uploads')
    DATA_DIR = os.path.join(TMP_DIR, 'data')
    # Update config paths
    from config import CANDIDATES_FILE, ASSESSMENTS_FILE, RESPONSES_FILE
    CANDIDATES_FILE = os.path.join(DATA_DIR, os.path.basename(CANDIDATES_FILE))
    ASSESSMENTS_FILE = os.path.join(DATA_DIR, os.path.basename(ASSESSMENTS_FILE))
    RESPONSES_FILE = os.path.join(DATA_DIR, os.path.basename(RESPONSES_FILE))
else:
    # Local development paths
    from config import UPLOAD_FOLDER, CANDIDATES_FILE, ASSESSMENTS_FILE, RESPONSES_FILE

from config import SECRET_KEY
from utils.file_handler import save_file
from utils.helpers import (
    get_all_candidates, get_candidate_by_id, save_candidate, update_candidate,
    get_assessment_by_id, save_assessments, get_responses_by_candidate_id,
    save_responses, get_response_by_id, update_response
)
from services.resume_parser import extract_skills_from_resume
from services.assessment_generator import generate_assessments_for_skills
from services.scoring_service import score_response
from models.candidate import Candidate
from models.response import Response

# --- App Initialization ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

# --- Helper to ensure directories exist on Vercel ---
def ensure_dirs():
    if IS_VERCEL:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)

# --- Applicant Routes ---
@app.route('/', methods=['GET', 'POST'])
def applicant_upload():
    ensure_dirs()
    if request.method == 'POST':
        if 'resume' not in request.files or not request.form.get('name') or not request.form.get('email'):
            flash('Please fill out all fields and select a resume file.', 'warning')
            return redirect(request.url)

        file = request.files['resume']
        if file.filename == '':
            flash('No resume file selected.', 'danger')
            return redirect(request.url)

        resume_path = save_file(file, app.config['UPLOAD_FOLDER'])
        # Vercel needs a relative path from the app's perspective
        relative_resume_path = os.path.relpath(resume_path, os.getcwd()) 

        candidate = Candidate(
            name=request.form['name'],
            email=request.form['email'],
            resume_path=relative_resume_path
        )
        save_candidate(candidate)
        flash(f'Successfully uploaded resume for {candidate.name}. Now processing...', 'success')

        try:
            skills = extract_skills_from_resume(resume_path)
            if not skills:
                flash('Processing failed: We could not identify any skills in your resume.', 'danger')
                return redirect(request.url)
            
            candidate.skills = skills
            update_candidate(candidate)

            assessments = generate_assessments_for_skills(skills)
            if not assessments:
                flash('Processing failed: An error occurred while generating assessment questions.', 'danger')
                return redirect(request.url)

            save_assessments(assessments)

            session['candidate_id'] = candidate.id
            session['assessment_ids'] = [a.id for a in assessments]
            
            return redirect(url_for('applicant_assessment'))
        except Exception as e:
            print(f"A critical error occurred during processing for candidate {candidate.id}: {e}")
            flash('A critical server error occurred during processing.', 'danger')
            return redirect(request.url)
            
    return render_template('applicant/upload.html')

# All other routes remain the same...

@app.route('/assessment', methods=['GET', 'POST'])
def applicant_assessment():
    ensure_dirs()
    candidate_id = session.get('candidate_id')
    assessment_ids = session.get('assessment_ids')

    if not candidate_id or not assessment_ids:
        flash('Your session has expired or is invalid. Please start over.', 'warning')
        return redirect(url_for('applicant_upload'))

    candidate = get_candidate_by_id(candidate_id)
    assessments = [get_assessment_by_id(aid) for aid in assessment_ids if get_assessment_by_id(aid) is not None]

    if request.method == 'POST':
        responses_to_save = []
        validated_skills = {}
        for i in range(len(assessments)):
            assessment_id = request.form.get(f'assessment_id_{i}')
            answer = request.form.get(f'answer_{assessment_id}')
            assessment = get_assessment_by_id(assessment_id)
            score = score_response(answer, assessment.model_answer)
            response = Response(candidate_id=candidate.id, assessment_id=assessment_id, answer=answer, score=score)
            responses_to_save.append(response)
            validated_skills[assessment.skill] = score
        
        save_responses(responses_to_save)
        candidate.validated_skills = validated_skills
        update_candidate(candidate)
        
        session['candidate_name'] = candidate.name
        session.pop('candidate_id', None)
        session.pop('assessment_ids', None)
        return redirect(url_for('applicant_thank_you'))

    return render_template('applicant/assessment.html', candidate=candidate, assessments=assessments)

@app.route('/thank-you')
def applicant_thank_you():
    candidate_name = session.pop('candidate_name', 'Applicant')
    return render_template('applicant/thank_you.html', candidate_name=candidate_name)

@app.route('/hr')
def hr_dashboard():
    ensure_dirs()
    candidates = get_all_candidates()
    for candidate in candidates:
        responses = get_responses_by_candidate_id(candidate.id)
        candidate.flagged_count = sum(1 for r in responses if r.flagged)
    return render_template('hr/dashboard.html', candidates=candidates)

@app.route('/hr/applicant/<candidate_id>')
def hr_applicant_detail(candidate_id):
    candidate = get_candidate_by_id(candidate_id)
    responses = get_responses_by_candidate_id(candidate_id)
    responses_data = []
    for r in responses:
        assessment = get_assessment_by_id(r.assessment_id)
        responses_data.append({'response': r, 'assessment': assessment})
    return render_template('hr/applicant_detail.html', candidate=candidate, responses_data=responses_data)

@app.route('/hr/flag_response/<response_id>', methods=['POST'])
def flag_response(response_id):
    data = request.get_json()
    response = get_response_by_id(response_id)
    if response and data is not None:
        response.flagged = data.get('flagged', False)
        update_response(response)
        return jsonify({'success': True, 'flagged': response.flagged})
    return jsonify({'success': False, 'error': 'Response not found or invalid data'}), 404

# Note: The main execution block is not needed for Vercel
# if __name__ == '__main__':
#     app.run(debug=True)
