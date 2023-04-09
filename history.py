#!/bin/bash
from pathlib import Path
from collections import deque
import shutil
import audio


class History:
    def __init__(self, name):
        self.dir = Path(Path.cwd(), "AudioCache", "History_" + name)
        if self.dir.is_dir():
            shutil.rmtree(self.dir)
        Path.mkdir(self.dir)
        self.queue = deque()

    def add(self, name):
        self.queue.append(Path(name))
        if len(self.queue) > 5:
            trash = self.queue.popleft()
            trash.unlink()

    def goBack(self, audio):
        if len(self.queue) == 0:
            print('Невозможно откатиться дальше по истории изменений')
            return
        trash = self.queue.pop()
        audio.current = self.queue.pop()
        audio.count -= 1
        self.add(str(audio.current))
        trash.unlink()

    def save(self):
        if len(self.queue) == 0:
            print('Не было изменений')
            return
        print("Сохранить в ...")
        print("P.s. Если хотите продолжить без сохранения, нажмите enter")
        while True:
            path = input()
            if path == "":
                self.exit()
            file_path = Path(path)
            if not file_path.is_dir():
                print("Директория не найдена, попробуйте еще раз")
                continue
            a = self.queue.pop()
            self.add(str(a))
            while True:
                print("Напишите имя аудиофайла")
                name = input()
                b = str(file_path) + "\\" + name + a.suffix
                if Path(b).is_file():
                    print("Фаил с таким названием уже существует,"
                          " попробуйте еще раз")
                    continue
                break
            shutil.copy(str(a), str(b))
            break

    def exit(self):
        while self.queue:
            trash = self.queue.popleft()
            trash.unlink()
        self.dir.rmdir()
        audio.AudioEditor()

    def exit_for_test(self):
        while self.queue:
            trash = self.queue.popleft()
            trash.unlink()
        self.dir.rmdir()
