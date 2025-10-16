import requests
import os

"""
добавить:
 цикл для ввода ссылок на файлы
 асинхронность
 несколько попыток на скачивание файла


"""


class Downloader:
    def __init__(self, browser='Mozilla/5.0'):
        self.path = ''
        self.files_stack = []
        self.headers = {'User-Agent': browser}

    def add_path(self):
        text_input = input(
            "Введите название папки для сохранения файлов, если папки не существует, то она будет создана: ")
        if len(text_input) > 0:
            self.path = text_input
            os.makedirs(self.path, exist_ok=True)

    def add_task(self):
        self.files_stack.append(input("Для скачивания файла, введите ссылку: "))

    def download(self, url: str, filename='image.jpg'):
        response = requests.get(url, headers=self.headers)
        save_path = os.path.join(self.path, filename)
        with open(save_path, "wb") as file:
            file.write(response.content)

    def start(self):
        try:
            self.add_path()
            self.add_task()
        except ValueError:
            print('Ошибка ввода')
        for task in self.files_stack:
            self.download(url=task)


if __name__ == "__main__":
    img_downloader = Downloader()
    img_downloader.start()
