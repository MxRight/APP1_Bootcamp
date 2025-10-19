import multiprocessing
import random
import os

#from prettytable import PrettyTable


class Man:
    def __init__(self, name: str, gender: str):
        self.name = name
        self.gender = gender

    def __repr__(self):
        return f'<Имя:{self.name}, Пол:{self.gender}>'


class Examiner(Man):
    pass


class Student(Man):
    pass


class Question:
    def __init__(self, question):
        self.question = question

    def __repr__(self):
        return f'<Вопрос: {self.question}>'


class Exam:
    DICT_OF_FILES = {Examiner: "examiners.txt", Question: "questions.txt", Student: "students.txt"}
    __DICT_OF_SELF = {Examiner: "list_of_examiners", Question: "list_of_questions", Student: "list_of_students"}

    def __init__(self):
        self.list_of_examiners = []
        self.list_of_students = []
        self.list_of_questions = []

    def scan_file(self, class_name, split_text=True):
        with open(self.DICT_OF_FILES[class_name], "r", encoding="utf-8") as f_in:
            if split_text:
                objects = [class_name(*line.strip().split()) for line in f_in]
            else:
                objects = [class_name(line.strip()) for line in f_in]
        setattr(self, self.__DICT_OF_SELF[class_name], objects)

    def load_data(self):
        for class_name in self.DICT_OF_FILES:
            split_text = class_name is not Question
            self.scan_file(class_name, split_text)

    def start(self):
        self.load_data()


    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":


    exam = Exam()
    exam.start()

    print(exam.list_of_examiners)
    print(exam.list_of_students)
    print(exam.list_of_questions)
    #exam.clear_screen()

    """ 
    table = PrettyTable()
    table.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
    table.add_row(["Adelaide", 1295, 1158259, 600.5])
    print(table)
    """