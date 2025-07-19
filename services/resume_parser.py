# skill_validation_system/services/resume_parser.py

from services.openai_service import generate_text
from utils.file_handler import read_file_content

def extract_skills_from_resume(resume_path):
    """
    Extracts skills from a resume using an AI model.

    Args:
        resume_path (str): The file path to the resume.

    Returns:
        list: A list of extracted skills.
    """
    # Read the text content from the uploaded resume file (PDF or DOCX)
    resume_content = read_file_content(resume_path)
    if not resume_content:
        return []

    # Create a prompt for the AI model to extract skills
    prompt = f"""
    From the following resume text, please identify and extract a list of key technical and soft skills.
    The output should be a single line of comma-separated values.
    For example: Python, Java, SQL, Project Management, Team Leadership, Communication

    Resume Content:
    ---
    {resume_content}
    ---
    Skills:
    """
    
    # Use the OpenAI service to get the skills list
    skills_text = generate_text(prompt)
    
    # Process the returned string into a list of skills
    if skills_text:
        # Split the comma-separated string and strip whitespace from each skill
        return [skill.strip() for skill in skills_text.split(',')]
        
    return []
