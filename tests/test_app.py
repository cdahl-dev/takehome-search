import unittest
from app.settings import Settings
from app.utils import get_log_events

class AppTest(unittest.TestCase):
    FILENAME = "test.log"
    FILE_LINES = [
        "Line 1: First line. This is line one.",
        "Line 2: Second line. This is line two.",
        "Line 3: Third line. This is line three."
    ]

    def setUp(self):
        Settings.LOG_FOLDER = "tests/files"

    def test_app_chunk_size(self):
        for chunk_size in [10, int(1024 * 4000)]:
            with self.subTest(chunk_size=chunk_size):
                Settings.CHUNK_SIZE = chunk_size
                result = get_log_events(AppTest.FILENAME)

                assert len(result) == len(AppTest.FILE_LINES), "Incorrect number of results"

                for i in range(len(result)):
                    assert result[i] == AppTest.FILE_LINES[len(result) - i - 1], "Unexpected line content"

    def test_app_top_n(self):
        for n in [1, 2, 3]:
            with self.subTest(n=n):
                result = get_log_events(AppTest.FILENAME, n=n)

                assert len(result) == n, "Incorrect number of results"

                for i in range(n):
                    assert result[i] == AppTest.FILE_LINES[len(AppTest.FILE_LINES) - i - 1], "Unexpected line content"

    def test_app_(self):
        result_index = 0
        for keyword in ['one', 'two', 'three']:
            with self.subTest(keywords=keyword):
                result = get_log_events(AppTest.FILENAME, keywords=keyword)

                assert len(result) == 1, "Incorrect number of results"

                assert result[0] == AppTest.FILE_LINES[result_index], "Unexpected line content"
                result_index += 1

    def test_app_keyword_chunk_size(self):
        Settings.CHUNK_SIZE = 2 # ensure that match gets broken up across chunks
        result = get_log_events(AppTest.FILENAME, keywords="This")

        assert len(result) == len(AppTest.FILE_LINES), "Incorrect number of results"

        for i in range(len(result)):
            assert result[i] == AppTest.FILE_LINES[len(result) - i - 1], "Unexpected line content"

    def test_app_keyword_case_sensitive(self):
        result = get_log_events(AppTest.FILENAME, keywords="TWO")
        assert len(result) == 1, "Incorrect number of results"
        assert result[0] == AppTest.FILE_LINES[1], "Unexpected line content"

    def test_app_keyword_multi(self):
        result = get_log_events(AppTest.FILENAME, keywords="one line")
        assert len(result) == 1, "Incorrect number of results"
        assert result[0] == AppTest.FILE_LINES[0], "Unexpected line content"

        result = get_log_events(AppTest.FILENAME, keywords="second two")
        assert len(result) == 1, "Incorrect number of results"
        assert result[0] == AppTest.FILE_LINES[1], "Unexpected line content"

        result = get_log_events(AppTest.FILENAME, keywords="testing line")
        assert len(result) == 0, "Incorrect number of results"

 