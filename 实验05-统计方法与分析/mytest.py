import sys
import nbformat
import re
import inspect
import pandas as pd
import numpy as np
from io import StringIO
from termcolor import colored
import matplotlib.pyplot as plt
from pathlib import Path
import pytest
import random
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import power

# Global variables (not ideal for production, but keeping for now)
test_results = {}
test_targets = {}
function_source_codes = {}

def collect_all_tests(ipynb_filename):
    """
    Collects all functions in a Jupyter notebook cell marked with '# GRADED FUNCTION: funcname'
    from notebook file and stores their objects in the test_targets dict.
    """
    test_targets.clear()
    function_source_codes.clear()
    with open(ipynb_filename, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    all_code = [cell.source for cell in nb.cells
                if cell.cell_type == 'code' and '# GRADED FUNCTION:' in cell.source]
    combined_code = '\n'.join(all_code)
    exec_globals = {
        'pd': pd, 'np': np, 'plt': plt, 'Path': Path, 'StringIO': StringIO,
        'stats': stats, 'sm': sm, 'smf': smf, 'power': power, 'random': random, '__builtins__': __builtins__,
    }
    try:
        exec(combined_code, exec_globals)
    except Exception as e:
        print(f"Error executing code: {e}")
        return test_targets
    pattern = re.compile(r'# GRADED FUNCTION: ([a-zA-Z_][a-zA-Z0-9_]*)')
    for code_cell in all_code:
        match = pattern.search(code_cell)
        if match:
            func_name = match.group(1)
            if func_name in exec_globals:
                test_targets[f"test_{func_name}"] = exec_globals[func_name]
                function_source_codes[func_name] = code_cell
    return test_targets

def get_function_source(func_name):
    return function_source_codes.get(func_name, "")

def _test_no_loops(target):
    src = get_function_source(target.__name__)
    assert "for" not in src, "函数中不应该包含 `for` 循环"
    assert "while" not in src, "函数中不应该包含 `while` 循环"

def test_get_columns_by_types(target):
    test_name = inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target
    mock_csv = StringIO("""SalePrice,PropertyType,Bedrooms,BldgGrade
280000,Multiplex,6,7
1000000,Single Family,4,10
745000,Single Family,4,8
425000,Single Family,5,7
240000,Single Family,4,7""")
    expected_df = pd.DataFrame({
        "SalePrice": [280000, 1000000, 745000, 425000, 240000],
        "PropertyType": ["Multiplex", "Single Family", "Single Family", "Single Family", "Single Family"],
        "Bedrooms": [6, 4, 4, 5, 4], "BldgGrade": [7, 10, 8, 7, 7]
    })
    try:
        result = target(mock_csv)
        pd.testing.assert_series_equal(result[0], expected_df['SalePrice'], check_dtype=False)
        pd.testing.assert_series_equal(result[1], expected_df['Bedrooms'], check_dtype=False)
        pd.testing.assert_series_equal(result[2], expected_df['BldgGrade'], check_dtype=False)
        pd.testing.assert_series_equal(result[3], expected_df['PropertyType'], check_dtype=False)
        _test_no_loops(target)
        test_results[test_name] = 1
        print(colored(f"习题1通过 {test_name}  {sum(test_results.values())}/{len(test_results)}", "green"))
    except Exception as e:
        print(colored(f"{test_name} 测试失败: {e}", "red"))

def test_calculate_z_scores(target):
    test_name = inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target
    try:
        arrs = [
            np.array([1,2,3,4,5]),
            np.array([-5, -10, -15]),
            np.array([10.5, 3.2, 7.8, 5.0, 9.1]),
            np.random.RandomState(42).randn(1000),
            np.array([5, 5, 5, 5, 5])
        ]
        for data in arrs[:-1]:
            expected = (data - np.mean(data)) / np.std(data, ddof=0)
            np.testing.assert_almost_equal(target(data), expected, decimal=6)
        np.testing.assert_almost_equal(target(arrs[-1]), np.zeros_like(arrs[-1]), decimal=6)
        _test_no_loops(target)
        test_results[test_name] = 1
        print(colored(f"习题2通过 {test_name}  {sum(test_results.values())}/{len(test_results)}", "green"))
    except Exception as e:
        print(colored(f"{test_name} 测试失败: {e}", "red"))


def test_analyze_house_prices(target):
    test_name = inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target
    try:
        mock_csv = StringIO("SalePrice\n100000\n150000\n200000\n250000\n300000\n")
        result, ax = target(mock_csv)
        assert result["Q1 (25th Percentile)"] == 150
        assert result["Q3 (75th Percentile)"] == 250
        assert result["IQR"] == 100
        assert result["Lower Whisker"] == 0
        assert result["Upper Whisker"] == 400
        assert isinstance(ax, plt.Axes)
        plt.close()
        # test with random data
        np.random.seed(42)
        rand_prices = np.random.randint(100000, 500000, 100)
        q1, q3 = np.percentile(rand_prices / 1000, [25, 75])
        iqr = q3 - q1
        mock_random = StringIO()
        pd.DataFrame({"SalePrice": rand_prices}).to_csv(mock_random, index=False)
        mock_random.seek(0)
        result, ax = target(mock_random)
        assert result["Q1 (25th Percentile)"] == pytest.approx(q1, abs=0.1)
        assert result["Q3 (75th Percentile)"] == pytest.approx(q3, abs=0.1)
        assert result["IQR"] == pytest.approx(iqr, abs=0.1)
        _test_no_loops(target)
        test_results[test_name] = 1
        print(colored(f"习题3通过 {test_name} {sum(test_results.values())}/{len(test_results)}", "green"))
    except Exception as e:
        print(colored(f"{test_name} 测试失败: {e}", "red"))


def run_all_tests():
    if not test_targets:
        print("没有找到需要测试的函数，请先运行 collect_all_tests()")
        return
    print(f"{len(test_targets)} 函数将被测试:")
    for test_name, func in test_targets.items():
        print(f"- {test_name}: {func.__name__}")
    for test_name, func in test_targets.items():
        if test_name == "test_get_columns_by_types":
            test_get_columns_by_types(func)
        elif test_name == "test_calculate_z_scores":
            test_calculate_z_scores(func)
        elif test_name == "test_analyze_house_prices":
            test_analyze_house_prices(func)
        # Add other test functions here as needed

def grade_all_tests():
    for key in test_results:
        test_results[key] = 0
    all_tests = [(getattr(sys.modules[__name__], name), test_targets[name])
                 for name in test_targets if name.startswith("test_")]
    for test_func, target in all_tests:
        try:
            test_func(target)
        except Exception as e:
            print(f"习题测试失败: {e}")
    print(colored(f"通过 {sum(test_results.values())} / {len(test_results)} 个测试", "green"))
    stu_grade = round(sum(test_results.values()) / len(test_results) * 100)
    print(colored(f"自动评分成绩:{stu_grade}", "green"))
    return stu_grade

if __name__ == "__main__":
    notebook_path = "实验6-统计方法与分析-with-answer.ipynb"  # update this as needed
    collect_all_tests(notebook_path)
    run_all_tests()
    print("="*50)
    print("最终测试结果:")
    final_grade = grade_all_tests()