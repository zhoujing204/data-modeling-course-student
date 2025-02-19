# 实验二的测试集， 进行实验的同学请不要修改测试文件的内容。
from termcolor import colored
import pytest
import math
import ast
import inspect

test_ids ={
    "test_get_first_last": 0,
    "test_pop_and_append": 0,
    "test_cubic_numbers": 0,
    "test_get_titled_names": 0,
    "test_sort_capitalized_names": 0,
    "test_get_ticket_price": 0,
    "test_calculate_total": 0,
}

def reset_test_ids_values():
    for key in test_ids.keys():
        test_ids[key] = 0

def test_calculate_total(target):
    """测试习题七"""
    test_name="习题七：test_calculate_total"
    test_ids["test_calculate_total"] = 0
    # Test case 1: Normal scenario with multiple items
    prices = {'apple': 2, 'banana': 1, 'orange': 3}
    quantities = {'apple': 3, 'banana': 5, 'orange': 2}
    total, count = target(prices, quantities)
    assert total == (2*3 + 1*5 + 3*2)  # 6 + 5 + 6 = 17
    assert count == 3  # 3 types of items

    # Test case 2: No items in quantities dictionary
    prices = {'apple': 2, 'banana': 1, 'orange': 3}
    quantities = {}
    total, count = target(prices, quantities)
    assert total == 0  # No items, so total should be 0
    assert count == 0  # No types of items

    # Test case 3: Single item in quantities dictionary
    prices = {'apple': 2, 'banana': 1, 'orange': 3}
    quantities = {'apple': 4}
    total, count = target(prices, quantities)
    assert total == (2*4)  # 8
    assert count == 1  # 1 type of item

    test_ids["test_calculate_total"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_get_ticket_price(target):
    """测试习题六"""
    test_name="习题六：test_get_ticket_price"
    test_ids["test_get_ticket_price"] = 0
    assert target(100, 5) ==  (0, 0), "第七题答案不正确，请检查你的答案"
    assert target(100, 6) ==  (15, .5),  "第七题答案不正确，请检查你的答案"
    assert target(100, 14) == (15, .5), "第七题答案不正确，请检查你的答案"
    assert target(100, 15) == (30, 1), "第七题答案不正确，请检查你的答案"
    assert target(100, 59) == (30, 1), "第七题答案不正确，请检查你的答案"
    assert target(100, 60) == (21, .7), "第七题答案不正确，请检查你的答案"
    test_ids["test_get_ticket_price"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_sort_capitalized_names(target):
    """测试习题五"""
    test_name="习题五：test_sort_capitalized_names"
    test_ids["test_sort_capitalized_names"] = 0
    assert target(['ada lovelace']) == ['Ada Lovelace'], "第五题答案不正确，请检查你的答案"
    assert target(['bbb', 'ccc', 'aaa']) == ['Aaa', 'Bbb', 'Ccc'], "第五题答案不正确，请检查你的答案"
    test_ids["test_sort_capitalized_names"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_get_titled_names(target):
    """测试习题四"""
    test_name="习题四：test_get_titled_names"
    test_ids["test_get_titled_names"] = 0
    tree = ast.parse(inspect.getsource(target))
    has_listcomp = any(isinstance(node, ast.ListComp) for node in ast.walk(tree))
    assert has_listcomp, f"函数 {target.__name__} 必须包含列表推导式：[ 变量表达式  for 变量  in 列表] "
    assert target(['ada lovelace', 'alan turing', 'grace hopper']) == ['Ada Lovelace', 'Alan Turing', 'Grace Hopper'], "第四题答案不正确，请检查你的答案"
    assert target(['ada lovelace']) == ['Ada Lovelace'], "第四题答案不正确，请检查你的答案"
    test_ids["test_get_titled_names"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))


def test_cubic_numbers(target):
    """测试习题三"""
    test_name="习题三：test_cubic_numbers"
    test_ids["test_cubic_numbers"] = 0
    tree = ast.parse(inspect.getsource(target))
    has_listcomp = any(isinstance(node, ast.ListComp) for node in ast.walk(tree))
    assert has_listcomp, f"函数 {target.__name__} 必须包含列表推导式：[ 变量表达式  for 变量  in 列表] "
    assert target(1) == [1], "第三题答案不正确，请检查你的答案"
    assert target(2) == [1, 8], "第三题答案不正确，请检查你的答案"
    assert target(3) == [1, 8, 27], "第三题答案不正确，请检查你的答案"
    assert target(4) == [1, 8, 27, 64], "第三题答案不正确，请检查你的答案"
    assert target(10) == [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000], "第三题答案不正确，请检查你的答案"
    test_ids["test_cubic_numbers"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_get_first_last(target):
    """测试习题一"""
    test_name="习题一：test_get_first_last"
    test_ids["test_get_first_last"] = 0
    assert target([1, 2, 3, 4, 5]) == [1, 5], "第一题答案不正确，请检查你的答案"
    assert target([1]) == [1, 1], "第一题答案不正确，请检查你的答案"
    assert target([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [1, 10], "第一题答案不正确，请检查你的答案"
    test_ids["test_get_first_last"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_pop_and_append(target):
    """测试习题二"""
    test_name="习题二：test_pop_and_append"
    test_ids["test_pop_and_append"] = 0
    lst = [1, 2, 3, 4, 5]
    target(lst)
    assert lst == [2, 3, 4, 5, 1], "第二题答案不正确，请检查你的答案"
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    target(lst)
    assert lst == [2, 3, 4, 5, 6, 7, 8, 9, 10, 1], "第二题答案不正确，请检查你的答案"
    test_ids["test_pop_and_append"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def grade_all_tests(test_args):
    reset_test_ids_values()
    all_tests = [
        (test_get_first_last, test_args[0]),
        (test_pop_and_append, test_args[1]),
        (test_cubic_numbers, test_args[2]),
        (test_get_titled_names, test_args[3]),
        (test_sort_capitalized_names, test_args[4]),
        (test_get_ticket_price, test_args[5]),
        (test_calculate_total, test_args[6])
    ]
    for test_func, arg in all_tests:
        try:
            if isinstance(arg, tuple):
                test_func(*arg)
            else:
                test_func(arg)
        except AssertionError as e:
            print("习题测试失败:", e)
        except Exception as e:
            print("测试过程中出现其它异常:", e)
    print(colored(f"恭喜你{sum(test_ids.values())}/{len(test_ids)} 个测试", "green"))
    # print(colored(f"你的代码自动评分成绩是：{sum(test_ids.values()) * 10}", "green"))
    student_grade = round(sum(test_ids.values()) / len(test_ids) * 100)
    print(colored(f"你的代码自动评分成绩(百分制)是:{student_grade}",
                  "green"))
    return round(sum(test_ids.values()) / len(test_ids) * 100)