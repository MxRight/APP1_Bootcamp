import time
from multiprocessing import Process, Queue, Event, Manager
import queue
import random
import os
import sys
from prettytable import PrettyTable
from functools import wraps
from io import StringIO


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


class Examiner(Man):
    def __init__(self, name: str, gender: str):
        super().__init__(name, gender)
        self.mood = None  # настроение на весь день или на экзамен?
        self.active = True  # для перерыва
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
        manager = Manager()

        self.dict_of_examiners = manager.dict()
        self.dict_of_students = manager.dict()
        self.dict_of_questions = manager.dict()

        self.tasks = Queue()
        self.stop_flag = Event()
        self.workers = []
        self.time_start = None
        self.time_from_start = None
        self.all_student = None
        self.all_passed_students = 0

    def scan_file(self, class_name, split_text=True):
        with open(self.DICT_OF_FILES[class_name], "r", encoding="utf-8") as f_in:
            if split_text:
                objects = [class_name(*line.strip().split()) for line in f_in]
            else:
                objects = [class_name(line.strip()) for line in f_in]
        setattr(self, self.DICT_OF_SELF[class_name], objects)

    def load_data(self): # пока не используем
        for class_name in self.DICT_OF_FILES:
            split_text = class_name is not Question
            self.scan_file(class_name, split_text)

    def start_exam(self, examiner_name, student):
        # Берём копии из manager-словарей
        student_obj = self.dict_of_students[student]
        examiner_obj = self.dict_of_examiners[examiner_name]

        # Отмечаем: студент сдал документы и зашёл
        student_obj.waiting = False
        examiner_obj.current_exam = student
        self.dict_of_examiners[examiner_name] = examiner_obj

        # Время экзамена зависит от длины имени экзаменатора
        exam_time = random.randint(len(examiner_name) - 1, len(examiner_name) + 1)

        self.dict_of_examiners[examiner_name] = examiner_obj

        time.sleep(exam_time)

        # Определяем результат (пока используем заглушку)
        student_obj.succes = random.choice([True, False])

        # Обновляем статистику экзаменатора
        examiner_obj.current_exam = None
        examiner_obj.work_time += exam_time
        examiner_obj.all_examined_students += 1
        if not student_obj.succes:
            examiner_obj.all_failed_students += 1

        # Перезаписываем оба объекта обратно в manager
        self.dict_of_students[student] = student_obj
        self.dict_of_examiners[examiner_name] = examiner_obj

    def worker(self, examiner_name, stop_flag):
        while True:
            try:
                student = self.tasks.get()
            except queue.Empty:
                continue
            if student is None:
                break
            self.start_exam(examiner_name, student)

    def add_task(self, item):
        self.tasks.put(item)

    def set_elapsed_time(self):
        self.time_from_start = time.time() - self.time_start

    def start_workers(self):
        for p in self.workers:
            p.start()

    def load_demo(self):
        students = {
            "Андрей": Student("Андрей", "М"),
            "Максим": Student("Максим", "М"),
            "Алексей": Student("Алексей", "М"),
            "Евгения": Student("Евгения", "Ж"),
            "Мария": Student("Мария", "Ж"),
            "Елена": Student("Евгения", "Ж"),
            "Маргарита": Student("Мария", "Ж"),
        }
        examiners = {
            "Александр": Examiner("Александр", "М"),
            "Дмитрий": Examiner("Дмитрий", "М"),
            "Михаил": Examiner("Михаил", "М"),
        }

        for name, student in students.items():
            self.dict_of_students[name] = student

        for name, examiner in examiners.items():
            self.dict_of_examiners[name] = examiner

    def start(self):
        self.load_demo()
        self.workers = [
            Process(target=self.worker, args=(examiner, self.stop_flag))
            for examiner in self.dict_of_examiners.keys()
        ]

        # заполняем очередь студентами
        self.all_student = len(self.dict_of_students)
        for student in self.dict_of_students.keys():
            self.add_task(student)
        self.time_start = time.time()
        self.start_workers()

    def stop(self):
        for _ in self.workers:
            self.tasks.put(None)
        self.stop_flag.set()
        for p in self.workers:
            p.join()

    def clean_screen(func):
        last_height = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_height
            import contextlib
            buffer = StringIO()
            with contextlib.redirect_stdout(buffer):
                func(*args, **kwargs)
            output = buffer.getvalue()
            lines = output.count("\n") + 1
            if last_height:
                sys.stdout.write(f"\033[{last_height}F")
                sys.stdout.write("\033[J")

            sys.stdout.write(output)
            sys.stdout.flush()

            last_height = lines

        return wrapper

    def print_data(self):
        self.set_elapsed_time()
        print(
            f'\r{self.TEXT_OUTPUT_ONE} {self.tasks.qsize()} из {self.all_student}\n{self.TEXT_OUTPUT_TWO} {self.time_from_start:.2f}')

    def print_student_table(self):
        student_table = PrettyTable()
        student_table.field_names = ["Студент", "Статус"]
        for student_name, student in self.dict_of_students.items():
            if getattr(student, "waiting", False):
                status = "Очередь"
            elif getattr(student, "succes", False):
                status = "Сдал"
            else:
                status = "Провалил"

            student_table.add_row([student_name, status])

        print(student_table)

    def print_examine_table(self, finish=False):
        examiner_table = PrettyTable()
        if finish:
            examiner_table.field_names = [
                "Экзаменатор",
                "Всего студентов",
                "Завалил",
                "Время работы"
            ]
        else:

            examiner_table.field_names = [
                "Экзаменатор",
                "Текущий студент",
                "Всего студентов",
                "Завалил",
                "Время работы"
            ]

        for examiner_name in self.dict_of_examiners.keys():
            examiner = self.dict_of_examiners[examiner_name]

            if finish:
                examiner_table.add_row([
                    examiner.name,
                    examiner.all_examined_students,
                    examiner.all_failed_students,
                    examiner.work_time
                ])
            else:
                current_student = examiner.current_exam if examiner.current_exam is not None else "-"

                examiner_table.add_row([
                    examiner.name,
                    current_student,
                    examiner.all_examined_students,
                    examiner.all_failed_students,
                    examiner.work_time
                ])

        print(examiner_table)

    @clean_screen
    def print_double_tables(self, finish=False):
        self.print_student_table()
        print()
        self.print_examine_table(finish=finish)
        print()
        self.print_data()


if __name__ == "__main__":
    exam = Exam()
    exam.start()
    sys.stdout.write("\033[H")
    while not exam.tasks.empty():
        time.sleep(0.1)
        exam.print_double_tables()
    exam.stop()
    exam.print_double_tables(finish=True)
