# skill_validation_system/models/assessment.py

import uuid

class Assessment:
    """
    Represents an assessment for a specific skill.
    """
    def __init__(self, skill, question, question_type, model_answer=None, id=None):
        """
        Initializes an Assessment object.

        Args:
            skill (str): The skill being assessed.
            question (str): The assessment question.
            question_type (str): The type of question (e.g., 'coding', 'case_study', 'scenario').
            model_answer (str, optional): A model answer for scoring purposes. Defaults to None.
            id (str, optional): The unique identifier for the assessment. Defaults to a new UUID.
        """
        self.id = id or str(uuid.uuid4())
        self.skill = skill
        self.question = question
        self.question_type = question_type
        self.model_answer = model_answer

    def to_dict(self):
        """Converts the Assessment object to a dictionary."""
        return {
            "id": self.id,
            "skill": self.skill,
            "question": self.question,
            "question_type": self.question_type,
            "model_answer": self.model_answer
        }

    @staticmethod
    def from_dict(data):
        """Creates an Assessment object from a dictionary."""
        return Assessment(
            id=data.get("id"),
            skill=data.get("skill"),
            question=data.get("question"),
            question_type=data.get("question_type"),
            model_answer=data.get("model_answer")
        )
