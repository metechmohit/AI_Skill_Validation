# skill_validation_system/utils/helpers.py

from utils.file_handler import read_json, write_json
from config import CANDIDATES_FILE, ASSESSMENTS_FILE, RESPONSES_FILE
from models.candidate import Candidate
from models.assessment import Assessment
from models.response import Response

# --- Candidate Helpers ---

def get_all_candidates():
    """Retrieves all candidates from the JSON data file."""
    candidates_data = read_json(CANDIDATES_FILE)
    return [Candidate.from_dict(c) for c in candidates_data]

def get_candidate_by_id(candidate_id):
    """Retrieves a single candidate by their unique ID."""
    for candidate in get_all_candidates():
        if candidate.id == candidate_id:
            return candidate
    return None

def save_candidate(candidate):
    """Adds a new candidate to the data file."""
    candidates = [c.to_dict() for c in get_all_candidates()]
    candidates.append(candidate.to_dict())
    write_json(CANDIDATES_FILE, candidates)

def update_candidate(updated_candidate):
    """Finds a candidate by ID and updates their data."""
    candidates = get_all_candidates()
    updated_list = [
        updated_candidate if c.id == updated_candidate.id else c for c in candidates
    ]
    write_json(CANDIDATES_FILE, [c.to_dict() for c in updated_list])

# --- Assessment Helpers ---

def get_all_assessments():
    """Retrieves all assessments from the JSON data file."""
    assessments_data = read_json(ASSESSMENTS_FILE)
    return [Assessment.from_dict(a) for a in assessments_data]

def get_assessment_by_id(assessment_id):
    """Retrieves a single assessment by its unique ID."""
    for assessment in get_all_assessments():
        if assessment.id == assessment_id:
            return assessment
    return None

def save_assessments(assessments_to_save):
    """Adds a list of new assessments to the data file."""
    all_assessments = [a.to_dict() for a in get_all_assessments()]
    all_assessments.extend([a.to_dict() for a in assessments_to_save])
    write_json(ASSESSMENTS_FILE, all_assessments)

# --- Response Helpers ---

def get_all_responses():
    """Retrieves all responses from the JSON data file."""
    responses_data = read_json(RESPONSES_FILE)
    return [Response.from_dict(r) for r in responses_data]

def get_responses_by_candidate_id(candidate_id):
    """Retrieves all responses submitted by a specific candidate."""
    return [r for r in get_all_responses() if r.candidate_id == candidate_id]
    
def get_response_by_id(response_id):
    """Retrieves a single response by its unique ID."""
    for response in get_all_responses():
        if response.id == response_id:
            return response
    return None

def save_responses(responses_to_save):
    """Adds a list of new responses to the data file."""
    all_responses = [r.to_dict() for r in get_all_responses()]
    all_responses.extend([r.to_dict() for r in responses_to_save])
    write_json(RESPONSES_FILE, all_responses)

def update_response(updated_response):
    """Finds a response by ID and updates its data."""
    responses = get_all_responses()
    updated_list = [
        updated_response if r.id == updated_response.id else r for r in responses
    ]
    write_json(RESPONSES_FILE, [r.to_dict() for r in updated_list])
