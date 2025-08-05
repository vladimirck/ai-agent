# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


class TestGetFilesInfo(unittest.TestCase):

    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertEqual(f'Successfully wrote to "lorem.txt" ({len("wait, this isn\'t lorem ipsum")} characters written)', result)

    def test_write_file_outside(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertEqual('Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory', result)

    def test_write_file_morelorem(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertEqual(f'Successfully wrote to "pkg/morelorem.txt" ({len("lorem ipsum dolor sit amet")} characters written)', result)
    
    def test_run_python_file(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        self.assertTrue(result.startswith("STDOUT: ") or result.startswith("Process exited with code"))
        result = run_python_file("calculator", "tests.py")
        print(result)
        self.assertTrue(result.startswith("STDOUT: ") or result.startswith("Process exited with code"))

    def test_run_python_file_with_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)
        self.assertTrue(result.startswith("STDOUT: ") or result.startswith("Process exited with code"))

    def test_run_python_file_outside(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertEqual('Error: Cannot execute "../main.py" as it is outside the permitted working directory', result)

    def test_run_python_file_not_found(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertEqual(f'Error: File "nonexistent.py" not found.', result)

if __name__ == "__main__":
    unittest.main()