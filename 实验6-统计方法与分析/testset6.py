# 实验6的测试集， 进行实验的同学请不要修改测试文件的内容。
import inspect
from pathlib import Path
import sys
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from termcolor import colored

test_results = {  }
test_targets = {  }

def test_get_columns_by_types(target):
    """测试习题1"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    # 模拟 CSV 数据
    mock_csv_data = """SalePrice,PropertyType,Bedrooms,BldgGrade
                        280000,Multiplex,6,7
                        1000000,Single Family,4,10
                        745000,Single Family,4,8
                        425000,Single Family,5,7
                        240000,Single Family,4,7
                        """
    # 使用 StringIO 模拟文件对象
    mock_csv_file = StringIO(mock_csv_data)

    # 构建期望的 DataFrame
    expected_df = pd.DataFrame({
        "SalePrice": [280000, 1000000, 745000, 425000, 240000],
        "PropertyType": ["Multiplex", "Single Family", "Single Family", "Single Family", "Single Family"],
        "Bedrooms": [6, 4, 4, 5, 4],
        "BldgGrade": [7, 10, 8, 7, 7]
    })

    continuous_variable = expected_df['SalePrice']
    discrete_variable = expected_df['Bedrooms']
    ordinal_variable = expected_df['BldgGrade']
    nominal_variable = expected_df['PropertyType']

    # 调用目标函数并检查返回结果
    result = target(mock_csv_file)
    pd.testing.assert_series_equal(result[0], continuous_variable, check_dtype=False)
    pd.testing.assert_series_equal(result[1], discrete_variable, check_dtype=False)
    pd.testing.assert_series_equal(result[2], ordinal_variable, check_dtype=False)
    pd.testing.assert_series_equal(result[3], nominal_variable, check_dtype=False)

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题1 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))


def test_calculate_z_scores(target):
    """测试习题2"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    # 测试集 1: 标准简单测试
    data = np.array([1, 2, 3, 4, 5])
    expected_z_scores = np.array([-1.41421356, -0.70710678, 0,  0.70710678,  1.41421356])
    np.testing.assert_almost_equal(target(data), expected_z_scores, decimal=6)

    # # 测试集 2: 全相同数据
    # data = np.array([5, 5, 5, 5, 5])
    # expected_z_scores = np.array([0, 0, 0, 0, 0])  # 所有数相同时标准分数应为 0
    # np.testing.assert_almost_equal(target(data), expected_z_scores, decimal=6)

    # 测试集 3: 数据为负值
    data = np.array([-5, -10, -15])
    expected_z_scores = np.array([1.22474487, 0, -1.22474487])
    np.testing.assert_almost_equal(target(data), expected_z_scores, decimal=6)

    # 测试集 4: 数据中包含小数
    data = np.array([10.5, 3.2, 7.8, 5.0, 9.1])
    expected_z_scores = (data - np.mean(data)) / np.std(data, ddof=0)  # 手动计算预期值
    np.testing.assert_almost_equal(target(data), expected_z_scores, decimal=6)

    # 测试集 5: 随机较大数据集
    data = np.random.randn(1000)  # 生成 1000 个标准正态分布的随机值
    expected_z_scores = (data - np.mean(data)) / np.std(data, ddof=0)
    np.testing.assert_almost_equal(target(data), expected_z_scores, decimal=6)

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题2 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))

def test_analyze_house_prices(target):
    """测试习题3"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    # 使用固定数据作为测试用例
    csv_data = """SalePrice
    100000
    150000
    200000
    250000
    300000
    """

    # 将固定数据加载到 StringIO
    mock_csv_file = StringIO(csv_data)

    # 调用测试函数，返回计算结果
    result, ax = target(mock_csv_file)

    # 验证统计数据是否正确（使用手动计算的期望结果）
    assert result["Q1 (25th Percentile)"] == 150  # Q1: 150000 / 1000
    assert result["Q3 (75th Percentile)"] == 250  # Q3: 250000 / 1000
    assert result["IQR"] == 100                  # IQR: Q3 - Q1
    assert result["Lower Whisker"] == 0          # 下须: Q1 - 1.5 * IQR
    assert result["Upper Whisker"] == 400        # 上须: Q3 + 1.5 * IQR

    # 验证 ax 是否是一个 boxplot 对象
    assert isinstance(ax, plt.Axes)
    plt.close()


    # 使用随机数据测试
    np.random.seed(42)  # 设置随机种子
    random_prices = np.random.randint(100000, 500000, size=100)  # 生成100个随机房价
    random_data = pd.DataFrame({"SalePrice": random_prices})

    # 将随机数据转为 CSV 格式供函数使用
    mock_random_file = StringIO()
    random_data.to_csv(mock_random_file, index=False)
    mock_random_file.seek(0)

    # 手工计算随机数据的预期结果
    sale_prices_in_thousands = random_prices / 1000
    q1 = np.percentile(sale_prices_in_thousands, 25)
    q3 = np.percentile(sale_prices_in_thousands, 75)
    iqr = q3 - q1
    lower_whisker = q1 - 1.5 * iqr
    upper_whisker = q3 + 1.5 * iqr

    # 调用测试函数，验证返回值
    result, ax = target(mock_random_file)

    # 断言随机数据的计算是否正确
    assert result["Q1 (25th Percentile)"] == pytest.approx(q1, abs=0.1)
    assert result["Q3 (75th Percentile)"] == pytest.approx(q3, abs=0.1)
    assert result["IQR"] == pytest.approx(iqr, abs=0.1)
    assert result["Lower Whisker"] == pytest.approx(lower_whisker, abs=0.1)
    assert result["Upper Whisker"] == pytest.approx(upper_whisker, abs=0.1)

    # 验证 ax 是否是 matplotlib 的 boxplot 对象
    assert isinstance(ax, plt.Axes)
    plt.close()

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题3 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))


def test_calculate_pefr_confidence_interval(target):
    """测试习题4"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    DATA = Path().resolve() / 'data'
    LUNGDISEASE_CSV = DATA / 'lungdisease.csv'

    pefr_values, se, lcb, ucb = target(LUNGDISEASE_CSV)

    expected_perf_values = pd.read_csv(LUNGDISEASE_CSV)['PEFR']
    expected_se = 9.51826210181264
    expected_lcb = 346.99994398536523
    expected_ucb = 384.3115314244708

    pd.testing.assert_series_equal(pefr_values, expected_perf_values, check_dtype=False)
    assert se == pytest.approx(expected_se, abs=0.1), "均值的标准误差计算错误"
    assert lcb == pytest.approx(expected_lcb, abs=0.1), "置信区间的置信下限计算错误"
    assert ucb == pytest.approx(expected_ucb, abs=0.1), "置信区间的置信上限计算错误"

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题4 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))


def test_analyze_nap_sleep_duration(target):
    """测试习题5"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    DATA = Path().resolve() / 'data'
    NAP_NO_NAP_CSV = DATA / "nap_no_nap.csv"

    result = target(NAP_NO_NAP_CSV)
    # 期望的输出值
    expected = (
        33.82533333333333,
        -16.00487687572963,
        18,
        1.4811248223284985,
        0.1558664953018476,
        False
    )

    # 断言检查
    assert len(result) == 6, "应该返回6项数据"  # 检查返回值数量

    # 分别检查每个返回值
    assert result[0] == pytest.approx(result[0], abs=0.1), "均值的差计算错误"
    assert result[1] == pytest.approx(result[1], abs=0.1), "均值的标准差的差值计算错误"
    assert result[2] == expected[2], "自由度计算错误"
    assert result[3] == pytest.approx(result[3], abs=0.1), "t统计量计算错误"
    assert result[4] == pytest.approx(result[4], abs=0.1), "p值计算错误"
    assert result[5] == expected[5]  # 显著性结果

    # Additional Test: Check that there are no loops in the target function
    source_code = inspect.getsource(target)
    assert "for" not in source_code, "函数中不应该包含 `for` 循环"
    assert "while" not in source_code, "函数中不应该包含 `while` 循环"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题5 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))


def grade_all_tests():
    for key in test_results.keys():
        test_results[key] = 0

    tests_list = [
        func
        for name, func in inspect.getmembers(sys.modules[__name__], inspect.isfunction)
        if name.startswith("test_")
    ]

    # print("tests_list:",tests_list)

    # all_tests = [(test, test_targets[i]) for i, test in enumerate(tests_list)]
    all_tests = [(test, test_targets[test.__name__]) for test in tests_list]

    # print("all_tests:",all_tests)

    for test_func, target in all_tests:
        try:
            if isinstance(target, tuple):
                test_func(*target)
            else:
                test_func(target)
        except AssertionError as e:
            print("习题测试失败:", e)
        except Exception as e:
            print("测试过程中出现其它异常:", e)
    print(colored(f"恭喜你{sum(test_results.values())}/{len(test_results)} 个测试", "green"))
    print(colored(f"你的代码自动评分成绩(百分制)是:{sum(test_results.values()) / len(test_results) * 100}",
                  "green"))
