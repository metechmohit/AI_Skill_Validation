# skill_validation_system/services/assessment_generator.py

import json
from services.openai_service import generate_text
from models.assessment import Assessment

def generate_assessments_for_skills(skills):
    """
    Analyzes a list of skills, selects the 15-20 most relevant ones, and generates a
    varied set of assessment questions (coding, mcq, subjective) for them in a single API call.

    Args:
        skills (list): A list of all skills extracted from the resume.

    Returns:
        list: A list of Assessment objects for the most relevant skills.
    """
    if not skills:
        return []

    # Convert the list of skills into a comma-separated string for the prompt
    skill_list_str = ", ".join(skills)

    # This new, more intelligent prompt asks the AI to select the most important skills first
    # and then create a mixed-type assessment for them.
    prompt = f"""
    You are an expert technical recruiter and hiring manager.
    From the following complete list of a candidate's skills:
    ---
    {skill_list_str}
    ---

    Your task is to create a comprehensive skill assessment. To do this:
    1. First, identify the 15 to 20 most important and representative skills from the list that provide the best overview of the candidate's capabilities.
    2. For this selected subset of skills, generate a varied set of assessment questions. The questions must be a mix of the following types: 'coding', 'mcq' (multiple-choice question), and 'subjective' (for soft skills or high-level concepts).
    3. For 'mcq' questions, embed the options (e.g., A, B, C, D) directly within the 'question' text. The 'model_answer' for an mcq should be only the correct letter (e.g., "C").
    
    Return your response as a single, minified JSON array containing 15 to 20 assessment objects. Each object in the array must have four keys: "skill", "question", "question_type", and "model_answer".
    Ensure the output is only the JSON array and nothing else.

    Example output for a candidate skilled in Python and Project Management:
    [{{"skill":"Python","question":"Write a Python list comprehension to return all even numbers from 0 to 20.","question_type":"coding","model_answer":"[x for x in range(21) if x % 2 == 0]"}},{{"skill":"Project Management","question":"What is the critical path in project management?\\nA) The longest sequence of tasks in a project plan.\\nB) The shortest sequence of tasks.\\nC) The most expensive tasks.\\nD) The tasks with the highest risk.","question_type":"mcq","model_answer":"A"}},{{"skill":"Communication","question":"Describe a time you had to explain a complex technical topic to a non-technical stakeholder. How did you approach it?","question_type":"subjective","model_answer":"A good answer would describe using analogies, focusing on business impact rather than technical details, checking for understanding, and tailoring the message to the audience. It demonstrates empathy and effective communication."}}]

    Now, generate the assessment JSON array for the skills listed above.
    """

    assessments = []
    # Call the AI model once to get the JSON array for all selected assessments
    response_str = generate_text(prompt)

    if not response_str:
        print("Failed to get a response from the assessment generation API.")
        return []

    try:
        # The AI might occasionally wrap the JSON in markdown, so we clean it up.
        if response_str.startswith("```json"):
            response_str = response_str.strip()[7:-4].strip()
        elif response_str.startswith("`"):
             response_str = response_str.strip()[1:-1].strip()
            
        # Parse the JSON string which should be a list of assessment dictionaries
        assessment_data_list = json.loads(response_str)
        
        # Iterate through the list of dictionaries from the JSON response
        for assessment_data in assessment_data_list:
            # Ensure the data is a dictionary before creating an object
            if isinstance(assessment_data, dict):
                assessment = Assessment(
                    skill=assessment_data.get("skill"),
                    question=assessment_data.get("question"),
                    question_type=assessment_data.get("question_type"),
                    model_answer=assessment_data.get("model_answer")
                )
                assessments.append(assessment)
    except (json.JSONDecodeError, AttributeError, TypeError) as e:
        # Error handling in case the AI model returns a malformed response
        print(f"Could not parse the assessment JSON array. Error: {e}")
        print(f"Received response: {response_str}")

    return assessments
