students = []

class Student:
    def __init__(self, id: int, surName: str, lastName: str, group: str):
        self.id = id
        self.surName = surName
        self.lastName = lastName
        self.group = group

        students.append(self)


def getStudent(id: int):
    for student in students:
        if student.id == id:
            return student
    return None
