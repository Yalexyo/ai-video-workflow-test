# tests/test_example_bugs.py
import unittest
import tempfile
import os
# 需要能够导入根目录的 example_bugs
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from example_bugs import (
    add_numbers,
    get_first_n_elements,
    multiply,
    divide,
    append_to_list,
    format_user_info,
    find_element,
    is_adult,
    process_data,
    read_file_contents
)

class TestExampleBugs(unittest.TestCase):

    def test_add_numbers_bug(self):
        """测试 add_numbers 的 bug (实际是乘法)"""
        self.assertEqual(add_numbers(2, 3), 6) # Fails if corrected to 5

    def test_get_first_n_elements(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(get_first_n_elements(lst, 3), [1, 2, 3])

    def test_multiply(self):
        self.assertEqual(multiply(5, 6), 30)

    def test_divide_by_zero_bug(self):
        """测试除零返回字符串的 bug"""
        self.assertEqual(divide(10, 0), "Division by zero") # Passes due to bug

    def test_append_to_list_bug(self):
        """测试可变默认参数的 bug"""
        # Reset shared state if necessary for consistent tests
        if hasattr(append_to_list, 'shared_list'):
            del append_to_list.shared_list
        result1 = append_to_list(1)
        self.assertEqual(result1, [1])
        # Due to the bug simulation, the list might persist
        result2 = append_to_list(2)
        # This assertion will fail because of the bug (expects [2], gets [1, 2])
        self.assertEqual(result2, [2]) # This is the line that should fail

    def test_format_user_info(self):
        self.assertEqual(format_user_info("John", 30), "Name: John, Age: 30")

    def test_find_element(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(find_element(lst, 3), 2)
        self.assertIsNone(find_element(lst, 6))

    def test_is_adult(self):
        self.assertTrue(is_adult(18))
        self.assertFalse(is_adult(17))

    def test_process_data_bug(self):
        """测试 sort() 返回 None 的 bug"""
        data = [3, 1, 4, 1, 5, 9]
         # This will fail as process_data returns the sorted list now
        self.assertEqual(process_data(data), [1, 1, 3, 4, 5, 9]) # Fails if sort() returns None

    def test_read_file_contents(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write("Test content")
            temp_name = temp.name
        try:
            content = read_file_contents(temp_name)
            self.assertEqual(content, "Test content")
        finally:
            os.unlink(temp_name)

        self.assertEqual(read_file_contents("non_existent_file.txt"), "File not found")

if __name__ == "__main__":
    # unittest.main() 使用 pytest 运行时不需要
    pass 