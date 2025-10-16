import requests
import os
import re

"""
добавить:
 цикл для ввода ссылок на файлы
 асинхронность
 несколько попыток на скачивание файла
 
 заменить регулярки и добавление пути на:
import os
from urllib.parse import urlparse

path = urlparse(url).path
filename = os.path.basename(path)
print(filename)  

"""


class Downloader:
    PATH_INPUT_TEXT = "Введите название папки для сохранения файлов, если папки не существует, то она будет создана: "
    URL_INPUT_TEXT = "Для скачивания файла, введите ссылку: "
    INCORRECT_PATH_ERROR_TEXT = "Некорректный путь или у программы нет доступа для сохранения по этому пути\n"
    TIMEOUT = 3

    def __init__(self, browser='Mozilla/5.0'):
        self.path = ''
        self.files_stack = []
        self.headers = {'User-Agent': browser}
        self.log = []

    def add_path_to_save(self):
        text_input = input(self.PATH_INPUT_TEXT)
        if len(text_input) > 0:
            self.path = self.clean_path(text_input)
            os.makedirs(self.path, exist_ok=True)

    @staticmethod
    def clean_path(dirty_path):
        return re.sub(r'[^A-Za-z0-9_\-/. ]+', '_', dirty_path)

    def add_file_url_to_load(self):
        self.files_stack.append(input(self.URL_INPUT_TEXT))

    def download(self, url: str, filename):
        response = requests.get(url, headers=self.headers, timeout=self.TIMEOUT)
        save_path = os.path.join(self.path, filename)
        with open(save_path, "wb") as file:
            file.write(response.content)

    def download_all(self, attempts=3):
        for _ in range(attempts):
            try:
                for url_task in self.files_stack:
                    filename = self.filename_from_url(url_task)
                    self.download(url=url_task, filename=filename)
            except Exception as e:
                print(f'{e}: {filename}')





    @staticmethod
    def filename_from_url(url:str) -> str:
        match = re.search(r'([^/]+)$', url)
        if match:
            filename = match.group(1)
        else:
            filename = 'image.jpg'
        return filename

    def logging(self):
        pass

    def print_result(self):
        pass

    def start(self):
        try:
            self.add_path_to_save()
        except ValueError:
            print(self.INCORRECT_PATH_ERROR_TEXT)
            self.add_path_to_save()

        self.add_file_url_to_load() # пока только один url
        self.download_all()




if __name__ == "__main__":
    img_downloader = Downloader()
    img_downloader.start()
