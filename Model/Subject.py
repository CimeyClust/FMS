subjects = []


class Subject:
    def __init__(self, id: int, subjectTitle: str, temporary: bool = False):
        self.id = id
        self.subjectTitle = subjectTitle

        if not temporary:
            subjects.append(self)


def getSubject(id: int):
    for subject in subjects:
        if subject.id == id:
            return subject
    return None

def getSubjectByName(name: str):
    for subject in subjects:
        if subject.subjectTitle == name:
            return subject
    return None
