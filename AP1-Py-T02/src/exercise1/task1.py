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
        self.exam_is_successful = None
        self.time_of_exam = None


class Examiner(Man):
    def __init__(self, name: str, gender: str):
        super().__init__(name, gender)
        self.mood = None
        self.is_active = True
        self.breaktime = False
        self.work_time = 0
        self.current_exam = None
        self.all_examined_students = 0
        self.all_failed_students = 0

    def set_mood(self):
        # 0 - нейтральное настроение
        # 1 - плохое настроение
        # 2 - хорошее настроение
        self.mood = random.choice(([0, 1, 0, 2, 0, 2, 0, 0]))


class Question:
    def __init__(self, question):
        self.question = question
        self.score_points = 0

    def __repr__(self):
        return f'<Вопрос: {self.question}>'


class Exam:
    TEXT_OUTPUT_ONE = "Осталось в очереди: "
    TEXT_OUTPUT_TWO = "Время с момента начала экзамена: "
    TEXT_OUTPUT_BREAK = "-"
    TEXT_OUTPUT_ALL_TIME = "Время с момента начала экзамена и до момента и его завершения: "
    TEXT_OUTPUT_BEST_STUDENTS = "Имена лучших студентов: "
    TEXT_OUTPUT_BEST_EXAMINERS = "Имена лучших экзаменаторов: "
    TEXT_OUTPUT_POOR_STUDENTS = "Имена студентов, которых после экзамена отчислят: "
    TEXT_OUTPUT_FINAL = "Вывод: экзамен"
    TEXT_OUTPUT_BEST_QUESTIONS = "Лучшие вопросы: "
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

    def scan_file(self, class_name, split_text=True):
        with open(self.DICT_OF_FILES[class_name], "r", encoding="utf-8") as f_in:
            if split_text:
                objects = [class_name(*line.strip().split()) for line in f_in]
            else:
                objects = [class_name(line.strip()) for line in f_in]
        setattr(self, self.DICT_OF_SELF[class_name], objects)

    def load_data(self):  # пока не используем
        for class_name in self.DICT_OF_FILES:
            split_text = class_name is not Question
            self.scan_file(class_name, split_text)

    def start_break(self, examiner_name):
        examiner_obj = self.dict_of_examiners[examiner_name]
        examiner_obj.current_exam = self.TEXT_OUTPUT_BREAK
        examiner_obj.is_active = False
        self.dict_of_examiners[examiner_name] = examiner_obj
        break_time = random.randint(*self.BREAKTIME_RANGE)
        time.sleep(break_time)
        examiner_obj.is_active = True
        examiner_obj.breaktime = True
        self.dict_of_examiners[examiner_name] = examiner_obj

    def start_exam(self, examiner_name, student):
        student_obj = self.dict_of_students[student]
        examiner_obj = self.dict_of_examiners[examiner_name]
        student_obj.waiting = False
        examiner_obj.current_exam = student
        examiner_obj.set_mood()
        self.dict_of_examiners[examiner_name] = examiner_obj
        exam_time = random.randint(len(examiner_name) - 1, len(examiner_name) + 1)
        self.dict_of_examiners[examiner_name] = examiner_obj
        student_obj.exam_is_successful = self.choosing_answers(examiner_name,
                                                               student)
        time.sleep(exam_time)
        # Обновляем статистику экзаменатора
        examiner_obj.current_exam = None
        examiner_obj.work_time += exam_time
        examiner_obj.all_examined_students += 1
        if not student_obj.exam_is_successful:
            examiner_obj.all_failed_students += 1

        student_obj.time_of_exam = exam_time

        # Перезаписываем оба объекта обратно в manager
        self.dict_of_students[student] = student_obj
        self.dict_of_examiners[examiner_name] = examiner_obj

    def worker(self, examiner_name):
        while True:
            examinator = self.dict_of_examiners[examiner_name]
            if examinator.is_active and not examinator.breaktime and examinator.work_time > self.TIME_TO_LUNCH:
                self.start_break(examiner_name)
                continue
            try:
                student = self.tasks.get(timeout=1)
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
            "Елена": Examiner("Михаил", "Ж"),
        }

        questions = {
            "Там стоит стол": Question("Там стоит стол"),
            "Человек собаке друг": Question("Человек собаке друг"),
            "Солнечные затмения влияют на людей": Question("Солнечные затмения влияют на людей"),
            "Программирование интересное занятие": Question("Программирование интересное занятие")}

        for name, student in students.items():
            self.dict_of_students[name] = student

        for name, examiner in examiners.items():
            self.dict_of_examiners[name] = examiner

        for question, ex_class in questions.items():
            self.dict_of_questions[question] = ex_class

    def start(self):
        self.load_demo()
        self.workers = [
            Process(target=self.worker, args=(examiner,))
            for examiner in self.dict_of_examiners.keys()
        ]

        self.all_student = len(self.dict_of_students)
        for student in self.dict_of_students.keys():
            self.add_task(student)
        self.time_start = time.time()
        self.start_workers()

    def choosing_answers(self, examiner_name, student_name):
        student = self.dict_of_students[student_name]
        examiner = self.dict_of_examiners[examiner_name]

        phi = self.GOLDEN_RATIO

        # три случайных вопроса
        questions = random.sample(list(self.dict_of_questions.values()), k=3)
        correct_total = 0
        wrong_total = 0

        for question_obj in questions:
            words = question_obj.question.split()
            n = len(words)
            if n == 0:
                continue

            probs = []
            remaining = 1.0
            for _ in range(n):
                p = remaining / phi
                probs.append(p)
                remaining -= p
            probs[-1] += remaining

            if student.gender == "Ж":
                probs = list(reversed(probs))

            student_answer = random.choices(words, weights=probs, k=1)[0]

            examiner_probs = list(reversed(probs)) if examiner.gender == "Ж" else probs
            correct_answers = []
            available = words[:]

            while available:
                picked = random.choices(available, weights=examiner_probs[:len(available)], k=1)[0]
                correct_answers.append(picked)
                idx = available.index(picked)
                available.pop(idx)
                examiner_probs.pop(idx)
                if random.random() > 1 / 3:
                    break

            if student_answer in correct_answers:
                correct_total += 1
                question_obj.score_points += 1
                self.dict_of_questions[question_obj.question] = question_obj

            else:
                wrong_total += 1

        if examiner.mood == 0:
            return correct_total > wrong_total
        elif examiner.mood == 1:
            return False
        elif examiner.mood == 2:
            return True

    def stop(self):
        for _ in self.workers:
            self.tasks.put(None)
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

    def print_data(self, finish=False):
        self.set_elapsed_time()
        text = self.TEXT_OUTPUT_ALL_TIME
        if not finish:
            text = self.TEXT_OUTPUT_TWO
            print(f'{self.TEXT_OUTPUT_ONE} {self.tasks.qsize()} из {self.all_student}')
        print(f'{text} {self.time_from_start:.2f}')

    @staticmethod
    def comma_join(items):
        return ', '.join(str(i) for i in items) if items else ''

    @staticmethod
    def sort_key(item):
        name, s = item
        if s.waiting:
            order = 0  # очередь
        elif s.exam_is_successful:
            order = 1  # сдал
        else:
            order = 2  # провалил
        return (order, name)

    def print_student_table(self):
        student_table = PrettyTable()
        student_table.field_names = ["Студент", "Статус"]

        for student_name, student in sorted(self.dict_of_students.items(), key=self.sort_key):
            if getattr(student, "waiting", False):
                status = "Очередь"
            elif getattr(student, "exam_is_successful", False):
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
        self.print_data(finish=finish)

    def print_statistics(self):
        max_points_questions = max((q.score_points for q in self.dict_of_questions.values()), default=None)
        best_questions = [
            q.question for q in self.dict_of_questions.values()
            if q.score_points == max_points_questions
        ]

        best_time = min((s.time_of_exam for s in self.dict_of_students.values() if s.exam_is_successful), default=None)
        poor_time = min((s.time_of_exam for s in self.dict_of_students.values() if not s.exam_is_successful),
                        default=None)
        best_students = []
        poor_students = []
        all_passed_students = 0

        for s in self.dict_of_students.values():
            if s.exam_is_successful:
                all_passed_students += 1
                if s.time_of_exam == best_time:
                    best_students.append(s.name)
            elif s.time_of_exam == poor_time and not s.exam_is_successful:
                poor_students.append(s.name)

        low_examiner_percent = min((
            e.all_failed_students / e.all_examined_students for e in
            self.dict_of_examiners.values() if e.all_examined_students > 0), default=None)

        best_examiners = []

        for e in self.dict_of_examiners.values():
            if e.all_examined_students > 0 and e.all_failed_students / e.all_examined_students <= low_examiner_percent:
                best_examiners.append(e.name)

        print(f'{self.TEXT_OUTPUT_BEST_STUDENTS} {self.comma_join(sorted(best_students))}')
        print(f'{self.TEXT_OUTPUT_BEST_EXAMINERS}{self.comma_join(sorted(best_examiners))}')
        print(f'{self.TEXT_OUTPUT_POOR_STUDENTS}{self.comma_join(sorted(poor_students))}')
        print(f'{self.TEXT_OUTPUT_BEST_QUESTIONS} {self.comma_join(best_questions)}')
        ratio = all_passed_students / self.all_student if self.all_student else 0
        result_text = "удался" if ratio >= 0.85 else "не удался"
        print(f"{self.TEXT_OUTPUT_FINAL} {result_text}")


if __name__ == "__main__":
    exam = Exam()
    exam.start()
    sys.stdout.write("\033[H")
    exam.print_double_tables()
    sys.stdout.flush()
    while not all(s.exam_is_successful is not None for s in exam.dict_of_students.values()):
        exam.print_double_tables()
        sys.stdout.flush()
        time.sleep(0.1)

    exam.stop()
    exam.print_double_tables(finish=True)
    exam.print_statistics()
