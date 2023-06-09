# Приложение «Аудиоредактор»

---

## Авторы
Головачев Георгий, Щербакова Полина \
ФТ-203

---

## Описание
Это приложение работает с аудио, у него есть следующие функции:
- обрезание аудио
- объединение нескольких аудио с текущим
- изменение скорости аудио
- конвертация из `.mp3` в `.wav` и наоборот
- разворачивание аудиозаписи
- воспроизведение аудио
- сохранение аудио
- откат назад (до предыдущей версии)
- функция выхода из программы

Приложение работает со следующими расширениями файлов:
- `.mp3` 
- `.wav`

---

## Состав приложения
- `audioEditor.py` - запускающий модуль
- `audio.py` - модуль содержащий класс, который отвечающий за приложение и его функции
- `history.py` - модуль работы с историей версий и отката назад
- `systemFiles` - папка для хранения истории версий
- `README.py` - файл с описанием проекта
- `tests.py` - тестирующий модуль
- `test.mp3` - тестовое аудио для проверки функциональности
- `test.txt` - тестовый файл неправильного расширения, нужен для проведения тестов 

---

## Запуск утилиты
- На Windows 11: `py audioEditor.py`
- На других операционных системах: `python3 audioEditor.py`

После запуска на экране появляются подсказки, которым нужно следовать. Ничего дополнительно делать не нужно