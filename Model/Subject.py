subjects = []

class Subject:
    def __init__(self, id: int, subjectTitle: str):
        self.id = id
        self.subjectTitle = subjectTitle

        subjects.append(self)