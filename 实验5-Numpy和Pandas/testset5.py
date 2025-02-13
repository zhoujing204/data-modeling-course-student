# 实验5的测试集， 进行实验的同学请不要修改测试文件的内容。
from termcolor import colored
import numpy as np
import pandas as pd
import pytest
import math
import ast
import inspect

test_ids ={
    "test_create_and_add_arrays": 0,
    "test_multiply_max_min": 0,
    "test_get_stocks_price": 0,
    "test_reshape_and_reverse": 0,
    "test_matrix_product_and_inverse": 0,
    "test_compute_scores": 0,
    "test_big_countries": 0,
}

def reset_test_ids_values():
    for key in test_ids.keys():
        test_ids[key] = 0

def test_create_and_add_arrays(target):
    """测试习题一"""
    test_name="习题一: test_create_and_add_arrays"
    test_ids["test_create_and_add_arrays"] = 0

    # Call the function
    A, B, C, D = target()

    # Assertions for arrays A, B, C
    np.testing.assert_array_equal(A, np.array([1, 2, 3, 4]))
    np.testing.assert_array_equal(B, np.array([5, 6, 7, 8]))
    np.testing.assert_array_equal(C, np.zeros(4))

    # Assert for the sum array D
    expected_D = A + B + C  # Should be [6, 8, 10, 12]
    np.testing.assert_array_equal(D, expected_D)

    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    test_ids["test_create_and_add_arrays"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))


def test_multiply_max_min(target):
    """测试习题二"""
    test_name="习题二: test_multiply_max_min"
    test_ids["test_multiply_max_min"] = 0

    # Test case 1: Regular arrays
    A = np.array([1, 2, 3, 4, 5])
    B = np.array([5, 4, 3, 2, 1])
    assert target(A, B) == 5

    # Test case 2: Negative values in arrays
    A = np.array([-10, -20, 30, 40])
    B = np.array([-5, -10, -15, 0])
    assert target(A, B) == -600

    # Test case 3: Single element in arrays
    A = np.array([42])
    B = np.array([-7])
    assert target(A, B) == -294

    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    test_ids["test_multiply_max_min"] = 1
    print(colored(f"恭喜你通过了{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_get_stocks_price(target):
    """测试习题三"""
    test_name= inspect.currentframe().f_code.co_name
    test_ids[test_name] = 0
    # Test case 1: Example input (normal case)
    stocks = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                       [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                       [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]])
    expected_output = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                 [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Test case 2: Single row matrix
    stocks = np.array([[1, 2, 3, 4, 5]])
    expected_output = np.array([[1, 2, 3, 4, 5]])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Test case 3: Single column matrix
    stocks = np.array([[1],
                       [11],
                       [21],
                       [31]])
    expected_output = np.array([[1],
                                 [31]])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Test case 4: Matrix with fewer than three rows
    stocks = np.array([[1, 2, 3],
                       [4, 5, 6]])
    expected_output = np.array([[1, 2, 3]])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Test case 5: Matrix with more than 7 rows
    stocks = np.array([[1, 2, 3],
                       [2, 3, 4],
                       [2, 3, 4],
                       [29, 43, 45],
                       [2, 3, 4],
                       [2, 3, 4],
                       [22, 33, 41],
                       [4, 5, 6]])
    expected_output = np.array([[1, 2, 3],[29, 43, 45],[22, 33, 41],])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Test case 6: Empty matrix
    stocks = np.array([[]])
    expected_output = np.array([[]])
    np.testing.assert_array_equal(target(stocks), expected_output)

    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    test_ids[test_name] = 1
    print(colored(f"恭喜你通过了习题三{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_reshape_and_reverse(target):
    """测试习题四"""
    test_name= inspect.currentframe().f_code.co_name
    test_ids[test_name] = 0

    # Test Case 1: A simple 2x2 matrix
    A = np.array([[1, 2], [3, 4]])
    shape, B = target(A)
    assert shape == (2, 2)
    assert np.array_equal(B, np.array([4, 3, 2, 1]))

    # Test Case 2: A 3x3 matrix
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    shape, B = target(A)
    assert shape == (3, 3)
    assert np.array_equal(B, np.array([9, 8, 7, 6, 5, 4, 3, 2, 1]))

    # Test Case 3: A 1x4 matrix
    A = np.array([[10, 20, 30, 40]])
    shape, B = target(A)
    assert shape == (1, 4)
    assert np.array_equal(B, np.array([40, 30, 20, 10]))

    # Test Case 4: A 4x1 matrix
    A = np.array([[1], [2], [3], [4]])
    shape, B = target(A)
    assert shape == (4, 1)
    assert np.array_equal(B, np.array([4, 3, 2, 1]))

    # Test Case 5: A single element matrix
    A = np.array([[42]])
    shape, B = target(A)
    assert shape == (1, 1)
    assert np.array_equal(B, np.array([42]))

    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    test_ids[test_name] = 1
    print(colored(f"恭喜你通过了习题四{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

def test_matrix_product_and_inverse(target):
    """测试习题五"""
    test_name= inspect.currentframe().f_code.co_name
    test_ids[test_name] = 0

    # Test Case 1: Random invertible matrix
    A = np.array([
        [2, 1],
        [4, 3],
    ])
    B = np.array([
        [1, 2],
        [3, 4],
    ])
    result = target(A, B)
    expected = np.linalg.inv(np.dot(A, B))
    assert np.allclose(result, expected)

    # Test Case 2: Singular Matrix (should raise an exception)
    A = np.array([
        [1, 2],
        [2, 4],
    ])
    B = np.array([
        [1, 0],
        [0, 1],
    ])
    with pytest.raises(np.linalg.LinAlgError):
        target(A, B)

    # Test Case 3: Another identity matrix case
    A = np.identity(3)
    B = np.identity(3)
    result = target(A, B)
    expected = np.identity(3)
    assert np.allclose(result, expected)

    # Test Case 4: 5x5 random invertible matrices
    A = np.array([
        [2, 5, 1, 3, 1],
        [4, 1, 3, 2, 7],
        [3, 4, 5, 6, 1],
        [7, 2, 8, 4, 3],
        [1, 2, 3, 4, 5],
    ])
    B = np.array([
        [1, 0, 3, 1, 2],
        [3, 2, 1, 5, 1],
        [4, 4, 2, 3, 6],
        [2, 1, 3, 2, 4],
        [1, 3, 2, 1, 3],
    ])
    result = target(A, B)
    expected = np.linalg.inv(np.dot(A, B))
    assert np.allclose(result, expected)


    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    test_ids[test_name] = 1
    print(colored(f"恭喜你通过了习题6{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))


def test_compute_scores(target):
    """测试习题6"""
    test_name = inspect.currentframe().f_code.co_name
    test_ids[test_name] = 0

    # Test Case 1: Example case
    scores = np.array([
        [80, 90, 85],
        [70, 60, 65],
        [90, 80, 85],
        [85, 75, 80],
        [60, 70, 75],
    ])
    mean, total = target(scores)
    expected_mean = np.array([77., 75., 78.])
    expected_total = np.array([255., 195., 255., 240., 205.])
    assert np.allclose(mean, expected_mean), f"期望平均分为 {expected_mean}，但得到了 {mean}"
    assert np.allclose(total, expected_total), f"期望总分为 {expected_total}，但得到了 {total}"

    # Test Case 2: Edge case with one student and one course
    scores = np.array([[100]])
    mean, total = target(scores)
    expected_mean = np.array([100.])
    expected_total = np.array([100.])
    assert np.allclose(mean, expected_mean), f"期望平均分为 {expected_mean}，但得到了 {mean}"
    assert np.allclose(total, expected_total), f"期望总分为 {expected_total}，但得到了 {total}"

    # Test Case 3: Edge case with all zeros
    scores = np.zeros((3, 4))
    mean, total = target(scores)
    expected_mean = np.zeros(4)
    expected_total = np.zeros(3)
    assert np.allclose(mean, expected_mean), f"期望平均分为 {expected_mean}，但得到了 {mean}"
    assert np.allclose(total, expected_total), f"期望总分为 {expected_total}，但得到了 {total}"

    # Test Case 4: Random scores
    scores = np.array([
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ])
    mean, total = target(scores)
    expected_mean = np.array([40., 50., 60.])
    expected_total = np.array([60., 150., 240.])
    assert np.allclose(mean, expected_mean), f"期望平均分为 {expected_mean}，但得到了 {mean}"
    assert np.allclose(total, expected_total), f"期望总分为 {expected_total}，但得到了 {total}"

    # Test Case 5: Random larger matrix
    scores = np.array([
        [15, 25, 35, 45],
        [20, 30, 40, 50],
        [25, 35, 45, 55],
        [30, 40, 50, 60],
    ])
    mean, total = target(scores)
    expected_mean = np.array([22.5, 32.5, 42.5, 52.5])
    expected_total = np.array([120., 140., 160., 180.])
    assert np.allclose(mean, expected_mean), f"期望平均分为 {expected_mean}，但得到了 {mean}"
    assert np.allclose(total, expected_total), f"期望总分为 {expected_total}，但得到了 {total}"

    # Additional Test: Check that the function contains no loops
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含`for`循环"
    assert "while" not in source_code, "函数中不应该包含`while`循环"

    # Mark the test as passed
    test_ids[test_name] = 1
    print(colored(f"恭喜你通过了习题6 {test_name} 测试。{sum(test_ids.values())}/{len(test_ids)}", "green"))



def test_big_countries(target):
    """测试习题7"""
    test_name = inspect.currentframe().f_code.co_name
    test_ids["test_big_countries"] = 0

    # Input DataFrame
    data = {
        "name": ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola"],
        "continent": ["Asia", "Europe", "Africa", "Europe", "Africa"],
        "area": [652230, 28748, 2381741, 468, 1246700],
        "population": [25500100, 2831741, 37100000, 78115, 20609294],
        "gdp": [20343000000, 12960000000, 188681000000, 3712000000, 100990000000]
    }
    df = pd.DataFrame(data)

    # Expected output DataFrame
    expected_data = {
        "name": ["Afghanistan", "Algeria"],
        "population": [25500100, 37100000],
        "area": [652230, 2381741]
    }
    expected_df = pd.DataFrame(expected_data)

    # Call the target function
    result_df = target(df)

    # Assertions
    # Check if result and expected tables are identical
    pd.testing.assert_frame_equal(
        result_df.sort_values(by=['name']).reset_index(drop=True),
        expected_df.sort_values(by=['name']).reset_index(drop=True),
    )

    # Additional Test 1: No big countries in the input
    data = {
        "name": ["Country1", "Country2", "Country3"],
        "continent": ["Asia", "Europe", "Africa"],
        "area": [2000000, 50000, 450000],
        "population": [10000000, 2000000, 1500000],
        "gdp": [50000000000, 1000000000, 2000000000]
    }
    df = pd.DataFrame(data)

    # Additional Test 2: All countries qualify as big
    data = {
        "name": ["CountryA", "CountryB", "CountryC"],
        "continent": ["Asia", "Europe", "Africa"],
        "area": [5000000, 4000000, 6000000],
        "population": [30000000, 50000000, 80000000],
        "gdp": [70000000000, 800000000000, 1500000000000]
    }
    df = pd.DataFrame(data)

    # Expected output: All countries should appear
    expected_df = pd.DataFrame({
        "name": ["CountryA", "CountryB", "CountryC"],
        "population": [30000000, 50000000, 80000000],
        "area": [5000000, 4000000, 6000000]
    })

    result_df = target(df)

    pd.testing.assert_frame_equal(
        result_df.sort_values(by=["name"]).reset_index(drop=True),
        expected_df.sort_values(by=["name"]).reset_index(drop=True),
    )


    # Additional Test 3: Mixed qualification with different criteria
    data = {
        "name": ["CountryX", "CountryY", "CountryZ"],
        "continent": ["Asia", "Europe", "Africa"],
        "area": [2500000, 4000000, 500000],
        "population": [13000000, 20000000, 30000000],  # CountryZ qualifies based on population
        "gdp": [5000000000, 4000000000, 8000000000]
    }
    df = pd.DataFrame(data)

    # Expected output: Only CountryY and CountryZ should qualify
    expected_df = pd.DataFrame({
        "name": ["CountryY", "CountryZ"],
        "population": [20000000, 30000000],
        "area": [4000000, 500000]
    })

    result_df = target(df)

    pd.testing.assert_frame_equal(
        result_df.sort_values(by=["name"]).reset_index(drop=True),
        expected_df.sort_values(by=["name"]).reset_index(drop=True),
    )

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    # Test passed
    test_ids["test_big_countries"] = 1
    print(colored(f"恭喜你通过了习题7{test_name}测试。{sum(test_ids.values())}/{len(test_ids)} ", "green"))

test_ids ={
    "test_create_and_add_arrays": 0,
    "test_multiply_max_min": 0,
    "test_get_stocks_price": 0,
    "test_reshape_and_reverse": 0,
    "test_matrix_product_and_inverse": 0,
    "test_compute_scores": 0,
    "test_big_countries": 0,
}

def grade_all_tests(test_args):
    reset_test_ids_values()
    all_tests = [
        (test_create_and_add_arrays, test_args[0]),
        (test_multiply_max_min, test_args[1]),
        (test_get_stocks_price, test_args[2]),
        (test_reshape_and_reverse, test_args[3]),
        (test_matrix_product_and_inverse, test_args[4]),
        (test_compute_scores, test_args[5]),
        (test_big_countries, test_args[6])
    ]
    # all_tests = [(globals()[test_name], test_args[i]) for i, test_name in enumerate(test_ids.keys())]

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
    print(colored(f"你的代码自动评分成绩(百分制)是:{sum(test_ids.values()) / len(test_ids) * 100}",
                  "green"))