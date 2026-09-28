"""2022-C题教学 notebook 使用的测试套件基类。"""

from pathlib import Path
from itertools import combinations
import inspect
import re

import nbformat
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

try:
    from termcolor import colored
except ImportError:  # 不强制学生额外安装仅用于着色的依赖
    def colored(text, *_args, **_kwargs):
        return text


class BaseTestSuite:
    """收集 notebook 中的评分函数、运行测试并计算成绩。"""

    required_tests_for_100_points = None
    maximum_grade = 100

    def __init__(self):
        self.test_results = {}
        self.test_targets = {}
        self.function_source_codes = {}

    def collect_all_tests(self, ipynb_filename):
        """收集标记为 ``# GRADED FUNCTION: name`` 的函数。"""
        self.test_targets.clear()
        self.function_source_codes.clear()

        notebook_path = Path(ipynb_filename)
        with notebook_path.open("r", encoding="utf-8") as stream:
            notebook = nbformat.read(stream, as_version=4)

        graded_cells = [
            cell.source
            for cell in notebook.cells
            if cell.cell_type == "code" and "# GRADED FUNCTION:" in cell.source
        ]
        combined_code = "\n\n".join(graded_cells)
        exec_globals = {
            "pd": pd,
            "np": np,
            "Path": Path,
            "re": re,
            "stats": stats,
            "combinations": combinations,
            "train_test_split": train_test_split,
            "StratifiedKFold": StratifiedKFold,
            "cross_val_score": cross_val_score,
            "StandardScaler": StandardScaler,
            "Pipeline": Pipeline,
            "LogisticRegression": LogisticRegression,
            "KNeighborsClassifier": KNeighborsClassifier,
            "DecisionTreeClassifier": DecisionTreeClassifier,
            "RandomForestClassifier": RandomForestClassifier,
            "KMeans": KMeans,
            "PCA": PCA,
            "confusion_matrix": confusion_matrix,
            "accuracy_score": accuracy_score,
            "balanced_accuracy_score": balanced_accuracy_score,
            "precision_score": precision_score,
            "recall_score": recall_score,
            "f1_score": f1_score,
            "__builtins__": __builtins__,
        }

        try:
            exec(combined_code, exec_globals)
        except Exception as error:
            print(colored(f"执行评分函数时出错：{error}", "red"))
            return self.test_targets

        pattern = re.compile(r"# GRADED FUNCTION:\s*([a-zA-Z_][a-zA-Z0-9_]*)")
        for code_cell in graded_cells:
            match = pattern.search(code_cell)
            if not match:
                continue
            function_name = match.group(1)
            target = exec_globals.get(function_name)
            if callable(target):
                self.test_targets[f"test_{function_name}"] = target
                self.function_source_codes[function_name] = self._extract_function_source(
                    code_cell, function_name
                )

        return self.test_targets

    @staticmethod
    def _extract_function_source(code_cell, function_name):
        """从一个评分单元中提取函数定义，供需要时检查。"""
        lines = code_cell.splitlines()
        function_lines = []
        in_function = False
        indentation = 0

        for line in lines:
            if re.match(rf"def\s+{re.escape(function_name)}\s*\(", line.strip()):
                in_function = True
                indentation = len(line) - len(line.lstrip())
                function_lines.append(line)
            elif in_function:
                if not line.strip():
                    function_lines.append(line)
                elif len(line) - len(line.lstrip()) > indentation:
                    function_lines.append(line)
                else:
                    break

        return "\n".join(function_lines)

    def get_function_source(self, function_name):
        source = self.function_source_codes.get(function_name, "")
        if source:
            return source

        for target in self.test_targets.values():
            if getattr(target, "__name__", None) == function_name:
                try:
                    source = inspect.getsource(target)
                except (OSError, TypeError):
                    source = ""
                self.function_source_codes[function_name] = source
                return source
        return ""

    def run_all_tests(self):
        if not self.test_targets:
            print("没有找到需要测试的函数，请先运行 collect_all_tests()。")
            return

        for test_name, target in self.test_targets.items():
            test_method = getattr(self, test_name, None)
            if callable(test_method):
                test_method(target)
            else:
                print(colored(f"警告：找不到测试方法 {test_name}", "yellow"))

    def calculate_grade(self, passed_tests, total_tests):
        required = self.required_tests_for_100_points or total_tests
        if required <= 0:
            return 0
        return min(round(passed_tests / required * 100), self.maximum_grade)

    def print_summary(self):
        """汇总当前内核中逐题运行的结果。"""
        if not self.test_results:
            print("尚未运行练习测试。")
            return 0

        passed = sum(self.test_results.values())
        total = len(self.test_results)
        grade = self.calculate_grade(passed, total)
        print("\n" + "=" * 50)
        print(colored(f"通过 {passed} / {total} 道练习测试", "green"))
        print(colored(f"自动评分成绩：{grade}", "green"))
        return grade

    def grade_all_tests(self, notebook_path):
        """从已保存的 notebook 重新收集函数并完成统一评分。"""
        print(f"正在从 notebook 收集评分函数：{notebook_path}")
        collected = self.collect_all_tests(notebook_path)
        if not collected:
            print("没有找到需要测试的函数。")
            return 0

        self.test_results = {}
        self.run_all_tests()
        return self.print_summary()

    def _run_exercise(self, test_name, target, checks):
        """运行一道练习的全部断言，并以0/1记录结果。"""
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target
        try:
            checks()
            self.test_results[test_name] = 1
            passed = sum(self.test_results.values())
            total = len(self.test_results)
            print(colored(f"恭喜你通过了 {test_name}。当前进度 {passed}/{total}", "green"))
        except NotImplementedError as error:
            print(colored(f"{test_name} 尚未完成：{error}", "yellow"))
        except Exception as error:
            print(colored(f"测试失败 {test_name}：{error}", "red"))
