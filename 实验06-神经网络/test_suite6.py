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

    def test_calculate_pefr_confidence_interval(self, target):
        """测试习题4"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            DATA = Path().resolve() / 'data'


            self._test_no_loops(target)
            self.test_results[test_name] = 1
            print(colored(f"习题4通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

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
                print(colored(f"警告: 找不到测试方法 {test_name}", "red"))

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
# suite = TestSuite6()
# suite.grade_all_tests("你的notebook路径.ipynb")