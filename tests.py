from audio import AudioEditor, length, is_file, is_audio
from pathlib import Path
import ffmpeg
import filecmp
import pytest

audio = AudioEditor(check=False, path="test.mp3")


class TestAudioEditor:
    def test_use_exist_file(self):
        assert is_file(Path("test.mp3")), "Файл не существует"

    def test_use_non_exist_file(self):
        assert not is_file(Path("wrong.mp3"))

    def test_use_audio(self):
        assert is_audio(Path("test.mp3")), "Файл имеет не допустимое расширение"

    def test_use_not_audio(self):
        assert not is_audio(Path("test.txt"))

    def test_cut(self):
        audio.cut(0, 5, stream=ffmpeg.input(str(audio.current)))
        result = length(str(audio.current))

        assert 5 - 0.1 <= result <= 5 + 0.1

        audio.history.exit_for_test()

    def test_concat(self):
        parts = [ffmpeg.input(str(audio.current)), ffmpeg.input(str(audio.current))]
        audio.concat(parts)

        assert filecmp.cmp("test_concat.mp3", audio.current, shallow=False)
        assert not filecmp.cmp("test.mp3", audio.current, shallow=False)

        audio.history.exit_for_test()

    def test_speed_change(self):
        audio.change_speed("2")

        assert filecmp.cmp("test_speed.mp3", audio.current, shallow=False)
        assert not filecmp.cmp("test.mp3", audio.current, shallow=False)

        audio.history.exit_for_test()

    def test_convert_mp3_to_wav(self):
        audio.convert()

        assert str(audio.history.dir) + "\\" + str(audio.current.stem) + ".wav"

        audio.history.exit_for_test()

    def test_reverse_audio(self):
        audio.reverse()

        assert filecmp.cmp("test_reverse.mp3", audio.current, shallow=False)
        assert not filecmp.cmp("test.mp3", audio.current, shallow=False)

        audio.history.exit_for_test()
