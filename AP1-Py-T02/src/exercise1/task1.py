import time
from multiprocessing import Process, Queue
import queue
import random
import os
import sys
from prettytable import PrettyTable


# реализовать перерывы экзаменаторов

class Man:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender

    def __repr__(self):
        return f'<Имя:{self.name}, Пол:{self.gender}>'


class Student(Man):
    def __init__(self, name: str, gender: str):
        super().__init__(name, gender)
        self.waiting = True
        self.succes = None

    def choosing_answer(self, male=True):
        pass


class Examiner(Man):
    def __init__(self, name: str, gender: str):
        super().__init__(name, gender)
        # self.queue = Queue()  # неправильно, если сформировать очередь сразу, но и ограничить очередь одним студентом, тоже?
        self.mood = self.set_mood()
        self.work_time = 0
        self.current_exam = None
        self.all_examined_students = 0
        self.all_failed_students = 0

    @staticmethod
    def set_mood():
        # 0 - нейтральное настроение
        # 1 - плохое настроение
        # 2 - хорошее настроение
        return random.choice(([0, 1, 0, 2, 0, 2, 0, 0]))

    def time_of_exam(self):
        len_of_name = len(self.name)
        return random.choice(list(range(len_of_name - 1, len_of_name + 1)))

    def start_exam(self, student: Student):
        student.waiting = False
        self.current_exam = student
        exam_time = self.time_of_exam()
        self.work_time += exam_time
        time.sleep(exam_time)
        # проставляем оценку и отправляем студента домой
        self.current_exam = None

    def choosing_question(self, male=True):
        pass


class Question:
    def __init__(self, question):
        self.question = question

    def __repr__(self):
        return f'<Вопрос: {self.question}>'


class Exam:
    TEXT_OUTPUT_ONE = "Осталось в очереди: "
    TEXT_OUTPUT_TWO = "Время с момента начала экзамена: "
    TIME_TO_LUNCH = 30
    BREAKTIME_RANGE = (12, 18)
    GOLDEN_RATIO = 1.618
    DICT_OF_FILES = {Examiner: "examiners.txt", Question: "questions.txt", Student: "students.txt"}
    DICT_OF_SELF = {Examiner: "list_of_examiners", Question: "list_of_questions", Student: "list_of_students"}

    def __init__(self):
        self.list_of_examiners = []
        self.list_of_students = []
        self.list_of_questions = []
        self.time_from_start = 0.00

    def scan_file(self, class_name, split_text=True):
        with open(self.DICT_OF_FILES[class_name], "r", encoding="utf-8") as f_in:
            if split_text:
                objects = [class_name(*line.strip().split()) for line in f_in]
            else:
                objects = [class_name(line.strip()) for line in f_in]
        setattr(self, self.DICT_OF_SELF[class_name], objects)

    def load_data(self):
        for class_name in self.DICT_OF_FILES:
            split_text = class_name is not Question
            self.scan_file(class_name, split_text)

    def start_exam(self):
        while not self.list_of_students:
            for examiner in self.list_of_examiners:
                if not examiner.current_exam:
                    examiner.start_exam(self.list_of_students.pop())

        # self.list_of_students.close()

    def start(self):
        self.load_data()
        self.start_exam()

        self.print_student_table()
        self.print_examine_table()

        print(f'{self.TEXT_OUTPUT_ONE}{0} из {0:.2f}')
        print(f'{self.TEXT_OUTPUT_TWO}{self.time_from_start}')

    def print_student_table(self):
        student_table = PrettyTable()
        student_table.field_names = ["Студент", "Статус"]
        for student in self.list_of_students:
            if student.waiting:
                status = "Очередь"
            else:
                if student.succes:
                    status = "Сдал"
                else:
                    status = "Провалил"
            student_table.add_row([student.name, status])
        print(student_table)

    def print_examine_table(self):
        examiner_table = PrettyTable()
        examiner_table.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы "]
        for examiner in self.list_of_examiners:
            examiner_table.add_row(
                [examiner.name, examiner.current_exam, examiner.all_examined_students, examiner.all_failed_students,
                 examiner.work_time])
        print(examiner_table)

    def print_finish_examiner_table(self):
        pass

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_screen2(self, output_data):
        sys.stdout.write(f'\r{output_data}')
        sys.stdout.flush()


if __name__ == "__main__":
    exam = Exam()
    exam.start()
