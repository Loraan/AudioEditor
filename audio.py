#!/bin/bash
import ffmpeg
import subprocess
import multiprocessing
from playsound import playsound
from pathlib import Path
from history import History

extensions_dict = {".mp3": ".wav",
                   ".wav": ".mp3"}  # нужно для удобной смены расширения в convert


def is_file(file):
    return file.is_file()


def is_audio(file):
    return file.suffix in ('.mp3', ".wav")


def length(name):
    return float(ffmpeg.probe(name)['format']['duration'])


class AudioEditor:
    def __init__(self, check=True, path=""):
        self.count = 0
        if check:
            self.path = self._check()
        else:
            self.path = Path(path)
        self.name = self.path.name
        self.current = self.path
        self.history = History(self.name)
        self.dictionary = {
            "exit": self.history.exit,
            "cut": self.cut_input,
            "join": self.concat_input,
            "speed": self.change_speed_input,
            "convert": self.convert,
            "reverse": self.reverse,
            "play": self.play,
            "save": self.history.save,
            "back": lambda: self.history.goBack(self),
        }
        if check:
            self.menu()

    def _check(self):
        print('Введите имя и расширение аудиофайла (доступные расширения: .mp3, .wav)')
        while True:
            name = input()
            if name == "":
                if self.count == 0:
                    exit()
                return Path("")
            file_path = Path(name)
            if not is_file(file_path):
                print("Фаил " + name + " не найден")
                print("Попробуйте еще раз")
                continue
            if not is_audio(file_path):
                print('Не поддерживается данное расширение,'
                      ' проверьте правильность названия файла ' + name)
                print("Попробуйте еще раз")
                continue
            return file_path

    def cut_input(self):
        self.count += 1
        stream = ffmpeg.input(str(self.current))
        duration = length(str(self.current))
        print('Укажите начало аудиофрагмента (в секундах) или нажмите enter,'
              ' чтобы выйти из данной функции')
        while True:
            try:
                st = input()
                if st == "":
                    return
                st = int(st)
            except:
                print("Неправильный ввод попробуйте еще раз")
            else:
                if 0 <= st <= duration:
                    break
                print("Начало вне аудиофрагмента, попробуйте еще раз")
        print('Укажите конец аудиофрагмента (в секундах) или нажмите enter,'
              ' чтобы обрезалось до конца')
        while True:
            try:
                en = input()
                if en == "":
                    en = duration
                    break
                en = int(en)
            except:
                print("Неправильный ввод попробуйте еще раз")
            else:
                if 0 <= en <= duration:
                    break
                print("Конец вне аудиофрагмента, попробуйте еще раз")
        self.cut(st, en, stream)

    def cut(self, st, en, stream):
        path = str(self.history.dir) + "\\" + str(self.count) \
               + self.name
        stream = stream.filter_('atrim', start=st, end=en) \
            .filter_('asetpts', 'PTS-STARTPTS')
        stream = ffmpeg.output(stream, path, loglevel="quiet")
        ffmpeg.run(stream)
        self.current = Path(path)
        self.history.add(path)

    def concat_input(self):
        self.count += 1
        print('Напишите названия аудиофайлов'
              ', которыe надо объединить с текущим файлом')
        parts = [ffmpeg.input(str(self.current))]
        while True:
            name = self._check()
            if name.name == "":
                break
            parts.append(ffmpeg.input(str(name)))
        self.concat(parts)

    def concat(self, parts):
        stream = ffmpeg.concat(*parts, v=0, a=1)
        path = str(self.history.dir) + "\\" + str(self.count) + self.name
        stream = ffmpeg.output(stream, path, loglevel="quiet")
        ffmpeg.run(stream)
        self.current = Path(path)
        self.history.add(path)

    def change_speed_input(self):
        self.count += 1
        print('Укажите во сколько раз надо ускорить'
              ' аудиодорожку (диапазон от 0.5 до 10) или нажмите enter,'
              ' чтобы выйти из данной функции')
        while True:
            speed = input()
            try:
                if speed == "":
                    return
                number = float(speed)
                if not (0.5 <= number <= 10.0):
                    print("Неправильный диапозон")
                    continue
            except:
                print("Неправильный формат ввода, попробуйте еще раз")
            else:
                break
        self.change_speed(speed)

    def change_speed(self, speed):
        path = str(self.history.dir) + "\\" + str(self.count) + self.name
        process = subprocess.Popen([
            'ffmpeg', "-loglevel", "-8",
            "-i", str(self.current), "-af",
            "atempo=" + speed, path])
        process.wait()
        self.current = Path(path)
        self.history.add(path)

    def convert(self):
        self.count += 1
        path = str(self.history.dir) + "\\" + \
               str(self.count) + str(self.current.stem) + \
               extensions_dict[str(self.current.suffix)]
        process = subprocess.Popen([
            'ffmpeg', "-loglevel", "-8", '-i', str(self.current), path
        ])
        process.wait()
        self.current = Path(path)
        self.history.add(path)

    def reverse(self):
        self.count += 1
        path = str(self.history.dir) + "\\" + str(self.count) + self.name
        process = subprocess.Popen([
            'ffmpeg', "-loglevel", "-8", '-i', str(self.current), "-af", "areverse", path
        ])
        process.wait()
        self.current = Path(path)
        self.history.add(path)

    def play(self):
        p = multiprocessing.Process(target=playsound, args=(str(self.current),))
        p.start()
        input("Нажмите ENTER чтобы остановить воспроизведение")
        p.terminate()

    def menu(self):
        while True:
            print('Выберите функцию:',
                  'exit - перестать работать с аудиозаписью',
                  'cut - обрезать аудио',
                  'join - объединить несколько аудио с текущим',
                  'speed - изменить скорость воспроизведения аудио',
                  'convert - изменить расширение файла',
                  'reverse - перевернуть аудиофайл',
                  'play - воспроизвести последнюю версию аудиофайла',
                  'save - сохранить',
                  'back - назад'
                  , sep='\n')
            command = input()
            if command in self.dictionary.keys():
                self.dictionary[command]()
                print("Дело сделано\n")
                self.menu()
                break
            else:
                print("Неправильный ответ, попробуй еще раз")
