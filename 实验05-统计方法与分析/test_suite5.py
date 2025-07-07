# 实验5的测试集， 进行实验的同学请不要修改测试文件的内容。

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

class TestSuite5:
    def __init__(self):
        self.test_results = {}
        self.test_targets = {}
        self.function_source_codes = {}

    def collect_all_tests(self, ipynb_filename):
        """
        Collects all functions in a Jupyter notebook cell marked with '# GRADED FUNCTION: funcname'
        from notebook file and stores their objects in the test_targets dict.
        """
        self.test_targets.clear()
        self.function_source_codes.clear()
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
            return self.test_targets
        pattern = re.compile(r'# GRADED FUNCTION: ([a-zA-Z_][a-zA-Z0-9_]*)')
        for code_cell in all_code:
            match = pattern.search(code_cell)
            if match:
                func_name = match.group(1)
                if func_name in exec_globals:
                    self.test_targets[f"test_{func_name}"] = exec_globals[func_name]
                    self.function_source_codes[func_name] = code_cell
        return self.test_targets

    def get_function_source(self, func_name):
        return self.function_source_codes.get(func_name, "")

    def _test_no_loops(self, target):
        src = self.get_function_source(target.__name__)
        assert "for" not in src, "函数中不应该包含 `for` 循环"
        assert "while" not in src, "函数中不应该包含 `while` 循环"

    def test_get_columns_by_types(self, target):
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target
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
            self._test_no_loops(target)
            self.test_results[test_name] = 1
            print(colored(f"习题1通过 {test_name}  {sum(self.test_results.values())}/{len(self.test_results)}", "green"))
        except Exception as e:
            print(colored(f"{test_name} 测试失败: {e}", "red"))

    def test_calculate_z_scores(self, target):
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target
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
            self._test_no_loops(target)
            self.test_results[test_name] = 1
            print(colored(f"习题2通过 {test_name}  {sum(self.test_results.values())}/{len(self.test_results)}", "green"))
        except Exception as e:
            print(colored(f"{test_name} 测试失败: {e}", "red"))

    def test_analyze_house_prices(self, target):
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target
        try:
            mock_csv = StringIO("SalePrice\n100000\n150000\n200000\n250000\n300000\n")
            result = target(mock_csv)
            assert result["Q1 (25th Percentile)"] == 150
            assert result["Q3 (75th Percentile)"] == 250
            assert result["IQR"] == 100
            assert result["Lower Whisker"] == 0
            assert result["Upper Whisker"] == 400

            # test with random data
            np.random.seed(42)
            rand_prices = np.random.randint(100000, 500000, 100)
            q1, q3 = np.percentile(rand_prices / 1000, [25, 75])
            iqr = q3 - q1
            mock_random = StringIO()
            pd.DataFrame({"SalePrice": rand_prices}).to_csv(mock_random, index=False)
            mock_random.seek(0)
            result = target(mock_random)
            assert result["Q1 (25th Percentile)"] == pytest.approx(q1, abs=0.1)
            assert result["Q3 (75th Percentile)"] == pytest.approx(q3, abs=0.1)
            assert result["IQR"] == pytest.approx(iqr, abs=0.1)
            self._test_no_loops(target)
            self.test_results[test_name] = 1
            print(colored(f"习题3通过 {test_name} {sum(self.test_results.values())}/{len(self.test_results)}", "green"))
        except Exception as e:
            print(colored(f"{test_name} 测试失败: {e}", "red"))

    def test_calculate_pefr_confidence_interval(self, target):
        """测试习题4"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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

            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题4通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_analyze_nap_sleep_duration(self, target):
        """测试习题5"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            DATA = Path().resolve() / 'data'
            NAP_NO_NAP_CSV = DATA / "nap_no_nap.csv"

            result = target(NAP_NO_NAP_CSV)
            expected = (
                33.82533333333333,
                -16.00487687572963,
                18,
                1.4811248223284985,
                0.1558664953018476,
                False
            )

            assert len(result) == 6, "应该返回6项数据"
            assert result[0] == pytest.approx(expected[0], abs=0.1), "均值的差计算错误"
            assert result[1] == pytest.approx(expected[1], abs=0.1), "均值的标准差的差值计算错误"
            assert result[2] == expected[2], "自由度计算错误"
            assert result[3] == pytest.approx(expected[3], abs=0.1), "t统计量计算错误"
            assert result[4] == pytest.approx(expected[4], abs=0.1), "p值计算错误"
            assert result[5] == expected[5]

            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题5通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def run_all_tests(self):
        """运行所有收集到的测试"""
        if not self.test_targets:
            print("没有找到需要测试的函数，请先运行 collect_all_tests()")
            return

        for test_name, func in self.test_targets.items():
            # 根据 test_name 获取对应的测试方法
            test_method = getattr(self, test_name, None)
            if test_method and callable(test_method):
                test_method(func)
            else:
                print(f"警告: 找不到测试方法 {test_name}")

    def grade_all_tests(self, notebook_path):
        """
        从指定的 notebook 路径收集所有函数并进行测试评分
        """
        print(f"正在从 notebook 文件收集测试函数: {notebook_path}")
        collected_tests = self.collect_all_tests(notebook_path)
        if not collected_tests:
            print("没有找到需要测试的函数！")
            return 0
        for key in self.test_results:
            self.test_results[key] = 0
        self.run_all_tests()
        if self.test_results:
            print("\n" + "="*50)
            print("最终测试结果:")
            print(colored(f"通过 {sum(self.test_results.values())} / {len(self.test_results)} 个测试", "green"))
            stu_grade = round(sum(self.test_results.values()) / len(self.test_results) * 100)
            print(colored(f"自动评分成绩(百分制):{stu_grade}", "green"))
            return stu_grade
        else:
            print("没有可用的测试结果")
            return 0

# 用法示例（非代码块）
# suite = TestSuite5()
# suite.grade_all_tests("你的notebook路径.ipynb")