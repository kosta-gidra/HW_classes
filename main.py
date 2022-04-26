class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lec(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def grade_mid(self):
        grade_sum = 0
        count = 0
        for grade in self.grades.values():
            grade_m = sum(grade) / len(grade)
            grade_sum += grade_m
            count += 1
        return grade_sum / count

    def __str__(self):
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        res = f'Имя: {self.name} \nФамилия: {self.surname} ' \
              f'\nСредняя оценка за домашние задания: {Student.grade_mid(self)} ' \
              f'\nКурсы в процессе изучения: {courses_in_progress_str}' \
              f'\nЗавершенные курсы:{finished_courses_str}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('not a Student')
            # print(f'{other} не студент')   #Как сделать чтобы other выводился не как его содержимое, а как имя?
            return
        return Student.grade_mid(self) < Student.grade_mid(other)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    # def rate_hw(self, student, course, grade):
    #     if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
    #         if course in student.grades:
    #             student.grades[course] += [grade]
    #         else:
    #             student.grades[course] = [grade]
    #     else:
    #         return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        self.grades = {}  # как добавить grades иначе? у меня получилось, что весь смысл наследования потерялся.

    def grade_mid(self):
        grade_sum = 0
        count = 0
        for grade in self.grades.values():
            grade_m = sum(grade) / len(grade)
            grade_sum += grade_m
            count += 1
        return grade_sum / count

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {Lecturer.grade_mid(self)}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('not a Lecturer')
            return
        return Lecturer.grade_mid(self) < Lecturer.grade_mid(other)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname}'
        return res


peter_student = Student('Peter', 'Parker', 'male')
peter_student.courses_in_progress += ['Python']
peter_student.courses_in_progress += ['Git']

miles_student = Student('Miles', 'Morales', 'male')
miles_student.courses_in_progress += ['Python']
miles_student.courses_in_progress += ['Git']

stiven_reviewer = Reviewer('Stiven', 'Strange')
stiven_reviewer.courses_attached += ['Python']
stiven_reviewer.courses_attached += ['Git']

bruce_reviewer = Reviewer('Bruce', 'Banner')
bruce_reviewer.courses_attached += ['Python']
bruce_reviewer.courses_attached += ['Git']

tony_lecturer = Lecturer('Tony', 'Stark')
tony_lecturer.courses_attached += ['Python']

clint_lecturer = Lecturer('Clint', 'Barton')
clint_lecturer.courses_attached += ['Git']

stiven_reviewer.rate_hw(peter_student, 'Python', 7)
bruce_reviewer.rate_hw(peter_student, 'Python', 7)
stiven_reviewer.rate_hw(miles_student, 'Python', 5)
bruce_reviewer.rate_hw(miles_student, 'Python', 4)
stiven_reviewer.rate_hw(peter_student, 'Git', 8)
bruce_reviewer.rate_hw(peter_student, 'Git', 9)
stiven_reviewer.rate_hw(miles_student, 'Git', 6)
bruce_reviewer.rate_hw(miles_student, 'Git', 8)

peter_student.rate_lec(tony_lecturer, 'Python', 10)
miles_student.rate_lec(tony_lecturer, 'Python', 9)
peter_student.rate_lec(clint_lecturer, 'Git', 10)
miles_student.rate_lec(clint_lecturer, 'Git', 8)

tanos_lecturer = Lecturer('Tanos', 'Titan')
tanos_lecturer.courses_attached += ['Python']
peter_student.rate_lec(tanos_lecturer, 'Python', 3)
miles_student.rate_lec(tanos_lecturer, 'Python', 2)


# print(miles_student)
# print()
# print(peter_student < miles_student)

# print(tony_lecturer)
# print()
# print(clint_lecturer < tony_lecturer)

def hw_mid_grade(course):
    enter_status = None
    count = 0
    grade_sum = 0
    for student in students:
        if isinstance(student, Student) and course in student.courses_in_progress:
            enter_status = True
        else:
            enter_status = False
            break
    if enter_status:
        for student in students:
            count += 1  # счетчик кл-ва студентов
            for course_stud, grade in student.grades.items():
                if course_stud == course:
                    grade_mid_stud = sum(grade) / len(grade)  # средний бал студента на курсе
                    grade_sum += grade_mid_stud  # сумма средних баллов всех студентов на курсе
        grade_sum = grade_sum / count
    else:
        print('Неверно указаны студенты или курс')
    return grade_sum


def lec_mid_grade(course):
    enter_status = None
    count = 0
    grade_sum = 0
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            enter_status = True
        else:
            enter_status = False
            break
    if enter_status:
        for lecturer in lecturers:
            count += 1
            for course_lec, grade in lecturer.grades.items():
                if course_lec == course:
                    grade_mid_lec = sum(grade) / len(grade)
                    grade_sum += grade_mid_lec
        grade_sum = grade_sum / count
    else:
        print('Неверно указаны лекторы или курс')
    return grade_sum


students = [peter_student, miles_student]
print(hw_mid_grade('Python'))

lecturers = [tanos_lecturer, tony_lecturer]
print(lec_mid_grade('Python'))
