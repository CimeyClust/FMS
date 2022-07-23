students = []

class Student:
    def __init__(self, id: int, name: str, surname: str, schoolClass: str, temporary: bool = False):
        self.id = id
        self.name = name
        self.surname = surname
        self.schoolClass = schoolClass

        if not temporary:
            students.append(self)


def getStudent(id: int):
    for student in students:
        if student.id == id:
            return student
    return None

def getStudentByAttributes(name: str, surname: str, group: str = None):
    if group is None:
        for student in students:
            if student.name == name and student.surname == surname:
                return student
    else:
        for student in students:
            if student.name == name and student.surname == surname \
                    and student.schoolClass == group:
                return student
