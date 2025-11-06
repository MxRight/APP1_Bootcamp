import os
import re
import asyncio
from pathlib import Path
from urllib.parse import urlparse
import requests


class AsyncDownloader:
    HEADER_BROWSER = 'Mozilla/5.0'
    MODULE_NAME = 'Async Downloader by Renatann'
    VERSION = '0.8'
    PATH_INPUT_TEXT = "Введите название папки для сохранения файлов, если папки не существует, то она будет создана (по умолчанию используется папка img): "
    URL_INPUT_TEXT = "Для скачивания файлов, вводите ссылки поддерживаются массивы ссылок через пробел, запятую, перенос строки (Enter для выхода): "
    INCORRECT_PATH_ERROR_TEXT = "Некорректный путь!"
    INCORRECT_URL_FORMAT_TEXT = "Некорректный формат ссылки!"
    PERMISSION_DENIED_TEXT = "Данная папка недоступна для записи!"
    FILENAME_TO_SAVE_DEFAULT = 'image.jpg'
    TIMEOUT = 3
    ATTEMPTS = 1
    TIME_DELAY = 0

    def __init__(self):
        self.path = 'img/'
        self.tasks = set()
        self.headers = {'User-Agent': self.HEADER_BROWSER}
        self.log = set()
        self.max_len_of_url = 0
        self.all_loaded_files = 0
        self.not_loaded_files = 0
        self.first_output = True
        self.title = f'{self.MODULE_NAME} Ver.:{self.VERSION}'

    def add_path_to_save(self) -> bool:
        text_input = input(self.PATH_INPUT_TEXT).strip()
        if not text_input:
            text_input = self.path
        path_obj = Path(text_input)

        try:
            path_obj.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Имя папки недопустимо: {e}")
            return False

        if not os.access(path_obj, os.W_OK):
            print(self.PERMISSION_DENIED_TEXT)
            return False

        self.path = str(path_obj.resolve())
        return True

    async def add_url(self, url: str) -> bool:
        url = url.strip()
        parsed = urlparse(url)
        if not url:
            return False
        if parsed.scheme not in ("http", "https"):
            print(f"{self.INCORRECT_URL_FORMAT_TEXT}: {url}")
            return False

        self.max_len_of_url = max(self.max_len_of_url, len(url))
        task = asyncio.create_task(self.download(url))
        self.tasks.add(task)
        task.add_done_callback(lambda t: self.tasks.discard(t))
        return True

    async def download(self, url) -> None:
        filename = self.filename_from_url(url)
        save_path = os.path.join(self.path, filename)
        success = False

        for attempt in range(self.ATTEMPTS):
            try:
                response = await asyncio.to_thread(
                    requests.get, url, headers=self.headers, timeout=self.TIMEOUT
                )
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    f.write(response.content)
            except Exception as e:
                # print(f"Ошибка при скачивании {url}: {e}")
                await asyncio.sleep(self.TIME_DELAY)
                continue
            else:
                success = True
                break

        if self.first_output:
            print()
            self.first_output = False

        if success:
            self.all_loaded_files += 1
            print(f"✅ Файл сохранён: {os.path.basename(save_path)}")
        else:
            print(f"❌ Ошибка: файл по указанной ссылке недоступен {url}")
            self.not_loaded_files += 1

        self.log.add((url, success, self.not_loaded_files + self.all_loaded_files))

    def filename_from_url(self, url: str) -> str:
        path = urlparse(url).path
        filename = os.path.basename(path)
        if not filename:
            filename = self.FILENAME_TO_SAVE_DEFAULT
        return filename

    def print_result(self) -> None:
        if len(self.log) == 0:
            self.log.add(("empty", ""))
            self.max_len_of_url = 5
        horizontal_border = "-" * (self.max_len_of_url + 2)
        bottom = f'+{horizontal_border}+{"-" * 8}+'
        print(bottom)
        print(f'| Ссылка{" " * (self.max_len_of_url - 5)}| Статус |')
        print(bottom)
        for i in self.log:
            current_len = len(i[0])
            print(f'| {i[0]}{" " * (self.max_len_of_url - current_len + 1)}{"| Успех  |" if i[1] else "| Ошибка |"}')
        print(bottom)

    async def start(self) -> None:
        print(self.title)
        while not self.add_path_to_save():
            pass
        print(self.URL_INPUT_TEXT)

        while True:
            line = await asyncio.to_thread(input)
            if not line.strip():
                break

            parts = re.split(r'[\s,]+', line.strip())
            for url in parts:
                await self.add_url(url)
            self.first_output = True

        if self.tasks:
            await asyncio.gather(*self.tasks)

        self.print_result()


async def main():
    img_downloader = AsyncDownloader()
    await img_downloader.start()


if __name__ == "__main__":
    asyncio.run(main())
