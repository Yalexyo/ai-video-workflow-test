#!/usr/bin/env python3
"""
包含一些故意引入的 bug 用于测试工作流。
"""
import os # read_file_contents 需要

def add_numbers(a, b):
    """本意是加法，但错误地写成了乘法"""
    return a * b # Bug: 应该是 a + b

def get_first_n_elements(lst, n):
    """获取列表前n个元素"""
    return lst[:n]

def multiply(a, b):
    """正确的乘法"""
    return a * b

def divide(a, b):
    """除法，未处理除零错误"""
    if b == 0:
         # Bug: 应该抛出异常或返回特定值，而不是字符串
        return "Division by zero"
    return a / b

def append_to_list(item, target_list=None):
    """
    添加到列表。
    Bug: 使用了可变的默认参数，导致后续调用受影响。
    """
    if target_list is None:
         # 正确做法应该是 target_list = []
         # 但这里故意留空以匹配之前的测试用例
         pass # 保持与原始测试用例的潜在问题一致
    # 为了复现原始测试的 bug，我们假设 target_list 是共享的
    if not hasattr(append_to_list, 'shared_list'):
         append_to_list.shared_list = []
    append_to_list.shared_list.append(item)
    return append_to_list.shared_list


def format_user_info(name, age):
    """格式化用户信息"""
    # Bug: age 应该是数字，但格式化时可能期待字符串
    try:
        return f"Name: {name}, Age: {str(age)}" # 假设 age 总是能转字符串
    except Exception:
        return "Invalid input"

def find_element(lst, element):
    """查找元素索引，未处理找不到的情况"""
    try:
        # Bug: index 会在找不到时抛出 ValueError
        return lst.index(element)
    except ValueError:
        return None # 正确处理

def is_adult(age):
    """判断是否成年"""
    return age >= 18 # 假设 age 是数字

def process_data(data):
    """处理数据（排序）"""
    # Bug: sort() 直接修改列表，返回 None
    data.sort()
    return data # 应该返回排序后的 data

def read_file_contents(filepath):
    """读取文件内容，未处理文件不存在等异常"""
    try:
        # Bug: 未指定 'r' 模式，未处理 FileNotFoundError
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"
    except Exception:
        return "Error reading file" 