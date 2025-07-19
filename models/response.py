import uuid

class Response:
    """
    Represents a candidate's response to an assessment.
    """
    def __init__(self, candidate_id, assessment_id, answer, score=0.0, flagged=False, id=None):
        """
        Initializes a Response object.

        Args:
            candidate_id (str): The ID of the candidate.
            assessment_id (str): The ID of the assessment.
            answer (str): The candidate's answer.
            score (float, optional): The score of the response. Defaults to 0.0.
            flagged (bool, optional): Whether the response is flagged for review. Defaults to False.
            id (str, optional): The unique identifier for the response. Defaults to a new UUID.
        """
        self.id = id or str(uuid.uuid4())
        self.candidate_id = candidate_id
        self.assessment_id = assessment_id
        self.answer = answer
        self.score = score
        self.flagged = flagged

    def to_dict(self):
        """Converts the Response object to a dictionary."""
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "assessment_id": self.assessment_id,
            "answer": self.answer,
            "score": self.score,
            "flagged": self.flagged
        }

    @staticmethod
    def from_dict(data):
        """Creates a Response object from a dictionary."""
        return Response(
            id=data.get("id"),
            candidate_id=data.get("candidate_id"),
            assessment_id=data.get("assessment_id"),
            answer=data.get("answer"),
            score=data.get("score"),
            flagged=data.get("flagged")
        )
