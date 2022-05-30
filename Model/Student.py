students = []


class Student:
    def __init__(self, id: int, name: str, surname: str, school_class: str):
        self.id = id
        self.name = name
        self.surname = surname
        self.school_class = school_class

        students.append(self)


def getStudent(id: int):
    for student in students:
        if student.id == id:
            return student
    return None
