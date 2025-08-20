
# base_test_suite.py
import nbformat
import re
import copy
import pandas as pd
import pulp
import numpy as np
from io import StringIO
from termcolor import colored
import matplotlib.pyplot as plt
from pathlib import Path
import random
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import power
import inspect

class BaseTestSuite:
    """测试套件基类，提供通用的测试功能"""

    def __init__(self):
        self.test_results = {}
        self.test_targets = {}
        self.function_source_codes = {}

    def collect_all_tests(self, ipynb_filename):
        """
        从 Jupyter notebook 文件中收集所有标记为 '# GRADED FUNCTION: funcname' 的函数
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
            'stats': stats, 'sm': sm, 'smf': smf, 'power': power, 'random': random,
            'copy': copy, 'pulp' : pulp,
            '__builtins__': __builtins__,
        }

        try:
            exec(combined_code, exec_globals)
        except Exception as e:
            print(f"Error executing code: {e}")
            return self.test_targets

        # 修改正则表达式模式，使其更准确
        pattern = re.compile(r'# GRADED FUNCTION:\s*([a-zA-Z_][a-zA-Z0-9_]*)')

        # 为每个代码单元格单独处理
        for code_cell in all_code:
            match = pattern.search(code_cell)
            if match:
                func_name = match.group(1)
                if func_name in exec_globals:
                    self.test_targets[f"test_{func_name}"] = exec_globals[func_name]
                    # 提取函数定义部分
                    func_source = self._extract_function_source(code_cell, func_name)
                    self.function_source_codes[func_name] = func_source
                    # print(f"收集到函数: {func_name}")

        return self.test_targets

    def _extract_function_source(self, code_cell, func_name):
        """从代码单元格中提取特定函数的源代码"""
        lines = code_cell.split('\n')
        func_lines = []
        in_function = False
        indent_level = 0

        for i, line in enumerate(lines):
            # 查找函数定义行
            if re.match(rf'def\s+{func_name}\s*\(', line.strip()):
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                func_lines.append(line)
            elif in_function:
                # 如果是空行，继续添加
                if not line.strip():
                    func_lines.append(line)
                # 如果缩进级别表明还在函数内部，继续添加
                elif len(line) - len(line.lstrip()) > indent_level or line.lstrip().startswith(('#', '"""', "'''")):
                    func_lines.append(line)
                # 如果遇到同级别或更低级别的代码，函数结束
                else:
                    break

        return '\n'.join(func_lines)

    def get_function_source(self, func_name):
        """获取函数源代码"""
        source = self.function_source_codes.get(func_name, "")
        if not source:
            # 如果存储的源代码为空，尝试使用inspect获取
            if func_name in [target.__name__ for target in self.test_targets.values()]:
                for target in self.test_targets.values():
                    if target.__name__ == func_name:
                        try:
                            source = inspect.getsource(target)
                            self.function_source_codes[func_name] = source
                            break
                        except:
                            pass
        return source

    def _test_no_loops(self, target):
        """检查函数是否包含循环"""
        src = self.get_function_source(target.__name__)
        if not src:
            print(colored(f"警告: 无法获取函数 {target.__name__} 的源代码", "yellow"))
            return
        assert "for" not in src, "函数中不应该包含 `for` 循环"
        assert "while" not in src, "函数中不应该包含 `while` 循环"

    def run_all_tests(self):
        """运行所有收集到的测试"""
        if not self.test_targets:
            print("没有找到需要测试的函数，请先运行 collect_all_tests()")
            return

        for test_name, func in self.test_targets.items():
            test_method = getattr(self, test_name, None)
            if test_method and callable(test_method):
                # print(f"\n正在运行测试: {test_name}")
                test_method(func)
            else:
                print(colored(f"警告: 找不到测试方法 {test_name}", "yellow"))

    def grade_all_tests(self, notebook_path):
        """
        从指定的 notebook 路径收集所有函数并进行测试评分
        """
        print(f"正在从 notebook 文件收集测试函数: {notebook_path}")
        collected_tests = self.collect_all_tests(notebook_path)

        if not collected_tests:
            print("没有找到需要测试的函数！")
            return 0

        # 初始化测试结果
        for key in self.test_results:
            self.test_results[key] = 0

        self.run_all_tests()

        if self.test_results:
            print("\n" + "="*50)
            print("最终测试结果:")
            passed_tests = sum(self.test_results.values())
            total_tests = len(self.test_results)
            print(colored(f"通过 {passed_tests} / {total_tests} 个测试", "green"))

            stu_grade = round(passed_tests / total_tests * 100) if total_tests > 0 else 0
            print(colored(f"自动评分成绩(百分制): {stu_grade}", "green"))
            return stu_grade
        else:
            print("没有可用的测试结果")
            return 0

    def _print_test_success(self, test_name):
        """打印测试成功信息的辅助方法"""
        passed = sum(self.test_results.values())
        total = len(self.test_results)
        print(colored(f"{test_name} 通过测试。{passed}/{total}", "green"))

    def _print_test_failure(self, test_name, error):
        """打印测试失败信息的辅助方法"""
        print(colored(f"测试失败 {test_name}: {str(error)}", "red"))

    def debug_function_collection(self, ipynb_filename):
        """调试函数收集过程"""
        print("=== 调试函数收集过程 ===")

        with open(ipynb_filename, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        print(f"总共找到 {len(nb.cells)} 个单元格")

        graded_cells = [cell for cell in nb.cells
                       if cell.cell_type == 'code' and '# GRADED FUNCTION:' in cell.source]

        print(f"包含 '# GRADED FUNCTION:' 的单元格数量: {len(graded_cells)}")

        pattern = re.compile(r'# GRADED FUNCTION:\s*([a-zA-Z_][a-zA-Z0-9_]*)')

        for i, cell in enumerate(graded_cells):
            print(f"\n--- 单元格 {i+1} ---")
            match = pattern.search(cell.source)
            if match:
                func_name = match.group(1)
                print(f"函数名: {func_name}")
                func_source = self._extract_function_source(cell.source, func_name)
                print(f"提取的源代码长度: {len(func_source)} 字符")
                if func_source:
                    print("源代码预览:")
                    print(func_source[:200] + "..." if len(func_source) > 200 else func_source)
            else:
                print("未找到函数名")
