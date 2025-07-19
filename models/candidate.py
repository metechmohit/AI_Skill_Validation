# skill_validation_system/models/candidate.py

import uuid

class Candidate:
    """
    Represents a candidate in the system.
    """
    def __init__(self, name, email, resume_path, skills=None, validated_skills=None, id=None):
        """
        Initializes a Candidate object.

        Args:
            name (str): The candidate's name.
            email (str): The candidate's email.
            resume_path (str): The file path to the candidate's resume.
            skills (list, optional): A list of skills claimed by the candidate. Defaults to None.
            validated_skills (dict, optional): A dictionary of validated skills and their scores. Defaults to None.
            id (str, optional): The unique identifier for the candidate. Defaults to a new UUID.
        """
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.resume_path = resume_path
        self.skills = skills or []
        self.validated_skills = validated_skills or {}

    def to_dict(self):
        """Converts the Candidate object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "resume_path": self.resume_path,
            "skills": self.skills,
            "validated_skills": self.validated_skills
        }

    @staticmethod
    def from_dict(data):
        """Creates a Candidate object from a dictionary."""
        return Candidate(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            resume_path=data.get("resume_path"),
            skills=data.get("skills"),
            validated_skills=data.get("validated_skills")
        )
