import os
import re
import asyncio
from urllib.parse import urlparse
import aiohttp
import aiofiles


class AsyncDownloader:
    HEADER_BROWSER = 'Mozilla/5.0'
    PATH_INPUT_TEXT = "Введите название папки для сохранения файлов, если папки не существует, то она будет создана: "
    URL_INPUT_TEXT = "Для скачивания файла, введите ссылку: "
    INCORRECT_PATH_ERROR_TEXT = "Некорректный путь!"
    INCORRECT_URL_FORMAT_TEXT = "Некорректный формат ссылки!"
    PERMISSION_DENIED_TEXT = "Данная папка недоступна для записи!"
    FILENAME_TO_SAVE_DEFAULT = 'image.jpg'
    TIMEOUT = 3  # в секундах
    ATTEMPTS = 1  # количество попыток для скачивания
    TIME_DELAY = 0  # время между попытками в секундах без блокировки процесса

    def __init__(self):
        self.path = ''
        self.tasks = set()
        self.headers = {'User-Agent': self.HEADER_BROWSER}
        self.log = []
        self.max_len_of_url = 0

    def add_path_to_save(self):
        text_input = input(self.PATH_INPUT_TEXT)
        if len(text_input) > 0:
            self.path = self.clean_path(text_input)
            os.makedirs(self.path, exist_ok=True)
            if not os.access(self.path, os.W_OK):
                print(f"{self.PERMISSION_DENIED_TEXT}")
                return self.add_path_to_save()
        return None

    @staticmethod
    def clean_path(dirty_path):
        return re.sub(r'[^A-Za-z0-9_\-/. ]+', '_', dirty_path)

    async def add_url(self, session, url: str) -> bool:
        url = url.strip()
        parsed = urlparse(url)
        if not url:
            return False
        if parsed.scheme not in ("http", "https"):
            print(self.INCORRECT_URL_FORMAT_TEXT)
            return False

        self.max_len_of_url = max(self.max_len_of_url, len(url))
        task = asyncio.create_task(self.download(session, url))
        self.tasks.add(task)
        task.add_done_callback(lambda t: self.tasks.discard(t))
        return True

    async def download(self, session, url):
        filename = self.filename_from_url(url)
        save_path = os.path.join(self.path, filename)
        success = False

        for attempt in range(self.ATTEMPTS):
            try:
                async with session.get(url, headers=self.headers, timeout=self.TIMEOUT) as response:
                    response.raise_for_status()
                    content = await response.read()
                    async with aiofiles.open(save_path, 'wb') as f:
                        await f.write(content)
            except Exception:
                await asyncio.sleep(self.TIME_DELAY)
                continue
            else:
                success = True
                break

        self.log.append((url, success))


    def filename_from_url(self, url: str) -> str:
        path = urlparse(url).path
        filename = os.path.basename(path)
        if not filename:
            filename = self.FILENAME_TO_SAVE_DEFAULT
        return filename

    def print_result(self):
        horizontal_border = "-" * (self.max_len_of_url + 2)
        bottom = f'+{horizontal_border}+{"-" * 8}+'
        print(bottom)
        print(f'| Ссылка{" " * (self.max_len_of_url - 5)}| Статус |')
        print(bottom)
        for i in self.log:
            current_len = len(i[0])
            print(f'| {i[0]}{" " * (self.max_len_of_url - current_len + 1)}{"| Успех  |" if i[1] else "| Ошибка |"}')
        print(bottom)

    async def start(self):
        try:
            self.add_path_to_save()
        except ValueError:
            print(self.INCORRECT_PATH_ERROR_TEXT)
            self.add_path_to_save()

        timeout = aiohttp.ClientTimeout(total=self.TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout, headers=self.headers) as session:
            while True:
                url = await asyncio.to_thread(input, self.URL_INPUT_TEXT)
                if not url:
                    break
                await self.add_url(session, url)

            if self.tasks:
                await asyncio.gather(*self.tasks)

        self.print_result()

async def main():
    img_downloader = AsyncDownloader()
    await img_downloader.start()


if __name__ == "__main__":
    asyncio.run(main())
