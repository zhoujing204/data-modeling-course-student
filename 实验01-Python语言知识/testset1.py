# 实验一的测试集， 进行实验的同学请不要修改测试文件的内容。
from termcolor import colored
import pytest
import math

test_ids ={
    "test_name_and_student_id": 0,
    "test_quiz2": 0,
    "test_subtract_abc": 0,
    "test_greet": 0,
    "test_get_hypotenuse": 0,
    "test_get_third_side": 0,
    "test_nearest_sq": 0
}

def reset_test_ids_values():
    for key in test_ids.keys():
        test_ids[key] = 0

def test_name_and_student_id(student_name, student_id):
    """测试习题一：学生的名字和学号是否填好"""
    test_name = "习题一：test_name_and_student_id"
    test_ids["test_name_and_student_id"] = 0
    assert student_name is not None, '请在name变量中填入你的名字'
    assert student_id is not None, '请在student_id变量中填入你的学号'
    print('你的名字是：', student_name)
    print('你的学号是：', student_id)
    test_ids["test_name_and_student_id"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_quiz2(answer2):
    """测试习题二的答案是否正确"""
    test_name = "习题二：test_quiz2"
    test_ids["test_quiz2"] = 0
    assert answer2.strip().upper() == "B", "第二题答案不正确，请检查你的答案"
    test_ids["test_quiz2"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_subtract_abc(target):
    """测试习题三"""
    test_name="习题三：test_subtract_abc"
    test_ids["test_subtract_abc"] = 0
    assert target(100, 2, 1) == 97, "第三题答案不正确，请检查你的答案"
    test_ids["test_subtract_abc"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_greet(target):
    """测试习题四"""
    test_name="习题四：test_greet"
    test_ids["test_greet"] = 0
    assert target('ada', 'lovelace') == 'Hello, Ada Lovelace!', "第四题答案不正确，请检查你的答案"
    test_ids["test_greet"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))


def test_get_hypotenuse(target):
    """测试习题五"""
    test_name="习题五：test_get_hypotenuse"
    test_ids["test_get_hypotenuse"] = 0
    assert target(3, 4) == pytest.approx(5.0) , "第五题答案不正确，请检查你的答案"
    assert target(6, 8) == pytest.approx(10.0)
    assert target(5, 12) == pytest.approx(13.0)
    res = target(2.5, 3.5)
    expected = (2.5**2 + 3.5**2) ** 0.5
    assert res == pytest.approx(expected) , "第五题答案不正确，请检查你的答案"
    test_ids["test_get_hypotenuse"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_get_third_side(target):
    """测试习题六"""
    test_name="习题六：test_get_third_side"
    test_ids["test_get_third_side"] = 0
    msg6 = "第6题答案不正确，请检查你的答案"
    test_get_third_side_right_angle(target, msg6)
    test_get_third_side_zero_angle(target, msg6)
    test_get_third_side_180_degrees(target, msg6)
    test_get_third_side_60_degrees(target, msg6)
    test_get_third_side_arbitrary(target, msg6)
    test_ids["test_get_third_side"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))


def test_get_third_side_right_angle(target, msg6):
    # 当夹角为90度(π/2弧度)时,应该符合勾股定理
    assert target(3, 4, math.pi/2) == pytest.approx(5.0), msg6
    assert target(5, 12, math.pi/2) == pytest.approx(13.0), msg6

def test_get_third_side_zero_angle(target, msg6):
    # 当夹角为0时,第三边长度应该是两边之差的绝对值
    assert target(5, 3, 0) == pytest.approx(2.0), msg6
    assert target(10, 7, 0) == pytest.approx(3.0), msg6

def test_get_third_side_180_degrees(target, msg6):
    # 当夹角为180度(π弧度)时,第三边长度应该是两边之和
    assert target(3, 4, math.pi) == pytest.approx(7.0), msg6
    assert target(5, 7, math.pi) == pytest.approx(12.0), msg6

def test_get_third_side_60_degrees(target, msg6):
    # 当夹角为60度(π/3弧度)时的特殊情况
    # 等边三角形的情况
    result = target(2, 2, math.pi/3)
    assert result == pytest.approx(2.0), msg6

def test_get_third_side_arbitrary(target, msg6):
    # 测试任意角度的情况
    result = target(4, 5, math.pi/4)  # 45度
    expected = math.sqrt(4**2 + 5**2 - 2*4*5*math.cos(math.pi/4))
    assert result == pytest.approx(expected), msg6

def test_nearest_sq(target):
    """测试习题七"""
    test_name="习题七：test_nearest_sq"
    test_ids["test_nearest_sq"] = 0
    msg7 = "第7题答案不正确，请检查你的答案"
    assert target(1) == 1, msg7
    assert target(2) == 1, msg7
    assert target(10) == 9, msg7
    assert target(111) == 121, msg7
    assert target(9999) == 10000, msg7
    test_ids["test_nearest_sq"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{round(sum(test_ids.values())/len(test_ids))} ", "green"))

def grade_all_tests(test_args):
    """对所有的测试进行评分"""
    reset_test_ids_values()
    all_tests = [
        (test_name_and_student_id, test_args[0]),
        (test_quiz2, test_args[1]),
        (test_subtract_abc, test_args[2]),
        (test_greet, test_args[3]),
        (test_get_hypotenuse, test_args[4]),
        (test_get_third_side, test_args[5]),
        (test_nearest_sq, test_args[6])
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
    print(colored(f"恭喜你通过了 {sum(test_ids.values())}/{len(test_ids)} 个测试", "green"))
    # print(colored(f"你的代码自动评分成绩是：{sum(test_ids.values()) * 10}", "green"))
    student_grade = round(sum(test_ids.values()) / len(test_ids) * 100)
    print(colored(f"你的代码自动评分成绩(百分制)是:{student_grade}",
                  "green"))
    return student_grade