class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def _average_grade(self):
        all_grades = [
            grade
            for grades_list in self.grades.values()
            for grade in grades_list
        ]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)   

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        in_progress = ', '.join(self.courses_in_progress)
        finished = ', '.join(self.finished_courses)
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: '
            f'{round(self._average_grade(), 1)}\n'
            f'Курсы в процессе изучения: {in_progress}\n'
            f'Завершенные курсы: {finished}'
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        all_grades = [
            grade
            for grades_list in self.grades.values()
            for grade in grades_list
        ]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: '
            f'{round(self._average_grade(), 1)}'
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'    

def average_hw_grade(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades += student.grades[course]
    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 1)


def average_lecture_grade(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades += lecturer.grades[course]
    if not all_grades:
        return 0
    return round(sum(all_grades) / len(all_grades), 1)


if __name__ == '__main__':
    # Создаём студентов
    student_1 = Student('Ольга', 'Алёхина', 'Ж')
    student_1.courses_in_progress += ['Python', 'Java']
    student_1.finished_courses += ['Введение в программирование']

    student_2 = Student('Иван', 'Сидоров', 'М')
    student_2.courses_in_progress += ['Python', 'Java']
    student_2.finished_courses += ['Git']

    # Создаём лекторов
    lecturer_1 = Lecturer('Иван', 'Иванов')
    lecturer_1.courses_attached += ['Python']

    lecturer_2 = Lecturer('Пётр', 'Петров')
    lecturer_2.courses_attached += ['Java']

    # Создаём ревьюеров
    reviewer_1 = Reviewer('Сергей', 'Смирнов')
    reviewer_1.courses_attached += ['Python']

    reviewer_2 = Reviewer('Анна', 'Кузнецова')
    reviewer_2.courses_attached += ['Java']

    # Ревьюеры ставят оценки студентам
    reviewer_1.rate_hw(student_1, 'Python', 9)
    reviewer_1.rate_hw(student_1, 'Python', 10)
    reviewer_1.rate_hw(student_2, 'Python', 8)
    reviewer_2.rate_hw(student_1, 'Java', 7)
    reviewer_2.rate_hw(student_2, 'Java', 9)
    reviewer_2.rate_hw(student_2, 'Java', 10)

    # Студенты ставят оценки лекторам
    student_1.rate_lecture(lecturer_1, 'Python', 10)
    student_1.rate_lecture(lecturer_1, 'Python', 9)
    student_2.rate_lecture(lecturer_1, 'Python', 8)
    student_1.rate_lecture(lecturer_2, 'Java', 7)
    student_2.rate_lecture(lecturer_2, 'Java', 9)

    # Печатаем информацию
    print(student_1)
    print()
    print(student_2)
    print()
    print(lecturer_1)
    print()
    print(lecturer_2)
    print()
    print(reviewer_1)
    print()
    print(reviewer_2)
    print()

    # Сравнения
    print(f'Студент 1 > Студент 2: {student_1 > student_2}')
    print(f'Студент 1 == Студент 2: {student_1 == student_2}')
    print(f'Лектор 1 > Лектор 2: {lecturer_1 > lecturer_2}')
    print(f'Лектор 1 < Лектор 2: {lecturer_1 < lecturer_2}')

    # Демонстрация ситуаций, когда оценка не может быть выставлена
    # Студент пытается оценить лектора по курсу, который не изучает
    result_1 = student_1.rate_lecture(lecturer_1, 'C++', 9)
    print(f'Студент оценивает лектора по чужому курсу: {result_1}')
    # Ревьюер пытается поставить оценку по курсу, к которому не прикреплён
    result_2 = reviewer_1.rate_hw(student_1, 'Java', 10)
    print(f'Ревьюер ставит оценку не по своему курсу: {result_2}')

    # Средние оценки по курсам
    students = [student_1, student_2]
    lecturers = [lecturer_1, lecturer_2]

    print(
        f'\nСредняя оценка студентов по Python: '
        f'{average_hw_grade(students, "Python")}'
    )
    print(
        f'Средняя оценка студентов по Java: '
        f'{average_hw_grade(students, "Java")}'
    )
    print(
        f'Средняя оценка лекторов по Python: '
        f'{average_lecture_grade(lecturers, "Python")}'
    )
    print(
        f'Средняя оценка лекторов по Java: '
        f'{average_lecture_grade(lecturers, "Java")}'
    )