# skill_validation_system/app.py

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from config import UPLOAD_FOLDER, SECRET_KEY
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

# --- Helper to ensure directories exist ---
# This is good practice for Render's persistent disks
def ensure_dirs():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Assuming data files are in a 'data' directory relative to the app
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)


# --- Applicant Routes ---
@app.route('/', methods=['GET', 'POST'])
def applicant_upload():
    ensure_dirs() # Make sure directories exist on service start
    if request.method == 'POST':
        if 'resume' not in request.files or not request.form.get('name') or not request.form.get('email'):
            flash('Please fill out all fields and select a resume file.', 'warning')
            return redirect(request.url)

        file = request.files['resume']
        if file.filename == '':
            flash('No resume file selected.', 'danger')
            return redirect(request.url)

        resume_path = save_file(file, app.config['UPLOAD_FOLDER'])
        candidate = Candidate(
            name=request.form['name'],
            email=request.form['email'],
            resume_path=os.path.relpath(resume_path, 'static')
        )
        save_candidate(candidate)
        flash(f'Successfully uploaded resume for {candidate.name}. Now processing...', 'success')

        try:
            skills = extract_skills_from_resume(resume_path)
            if not skills:
                flash('Processing failed: We could not identify any skills in your resume. Please check the file and try again.', 'danger')
                return redirect(request.url)
            
            candidate.skills = skills
            update_candidate(candidate)

            assessments = generate_assessments_for_skills(skills)
            if not assessments:
                flash('Processing failed: An error occurred while generating assessment questions. Please try again later.', 'danger')
                return redirect(request.url)

            save_assessments(assessments)
            session['candidate_id'] = candidate.id
            session['assessment_ids'] = [a.id for a in assessments]
            
            return redirect(url_for('applicant_assessment'))

        except Exception as e:
            print(f"A critical error occurred during processing for candidate {candidate.id}: {e}")
            flash('A critical server error occurred during processing. The technical team has been notified.', 'danger')
            return redirect(request.url)
            
    return render_template('applicant/upload.html')


@app.route('/assessment', methods=['GET', 'POST'])
def applicant_assessment():
    candidate_id = session.get('candidate_id')
    assessment_ids = session.get('assessment_ids')

    if not candidate_id or not assessment_ids:
        flash('Your session has expired or is invalid. Please start over by uploading your resume.', 'warning')
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

# --- HR Routes ---
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

# This block is not needed for Render deployment but is fine to keep for local testing
if __name__ == '__main__':
    ensure_dirs()
    app.run(debug=False)
