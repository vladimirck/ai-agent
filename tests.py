# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


class TestGetFilesInfo(unittest.TestCase):

    def test_calculator_dot(self):
        result = get_files_info("calculator", ".")
        print(result)
        self.assertIn("- main.py:", result)
        self.assertIn("- tests.py:", result)
        self.assertIn("- tests.py:", result)
        self.assertIn("- pkg:", result)

    def test_calculator_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(result)
        self.assertIn("- calculator.py:", result)
        self.assertIn("- render.py:", result)
        self.assertIn("- __pycache__:", result)

    def test_error_bin(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertEqual('Error: Cannot list "/bin" as it is outside the permitted working directory', result)

    def test_error_dotdot(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertEqual('Error: Cannot list "../" as it is outside the permitted working directory', result)

    def test_truncated(self):
        result = get_file_content("calculator", "lorem.txt")
        print(result)
        self.assertIn('[...File "lorem.txt" truncated at 10000 characters]', result)
    
    def test_error_outside(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertEqual('Error: Cannot read "/bin/cat" as it is outside the permitted working directory', result)

    def test_error_not_file(self):
        result = get_file_content("calculator", "pkg")
        print(result)
        self.assertEqual('Error: File not found or is not a regular file: "pkg"', result)

    def test_does_not_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)
        self.assertEqual('Error: File not found or is not a regular file: "pkg/does_not_exist.py"', result)

    def test_file_exists(self):
        result_main = get_file_content("calculator", "main.py")
        result_pkg_calc = get_file_content("calculator", "pkg/calculator.py")
        print(result_main)
        self.assertIn('def main():', result_main)
        print(result_pkg_calc)
        self.assertIn('def _apply_operator(self, operators, values):', result_pkg_calc)

    

if __name__ == "__main__":
    unittest.main()