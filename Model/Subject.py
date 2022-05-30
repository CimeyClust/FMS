subjects = []


class Subject:
    def __init__(self, id: int, subjectTitle: str):
        self.id = id
        self.subjectTitle = subjectTitle

        subjects.append(self)


def getSubject(id: int):
    for subject in subjects:
        if subject.id == id:
            return subject
    return None

def getSubjectByName(name: str):
    for subject in subjects:
        if subjects.id == id():
            return subject
    return None
