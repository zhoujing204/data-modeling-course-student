import numpy as np
import pandas as pd
import re
import pytest
from base_test_suite import BaseTestSuite
from termcolor import colored

class TestSuite2(BaseTestSuite):
    """实验2的测试套件"""

    def test_create_and_add_arrays(self, target):
        """测试习题一"""
        test_name = "test_create_and_add_arrays"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：n=4 的基本测试
            A, B, C, D = target(4)

            expected_A = np.array([0, 1, 2, 3])  # np.arange(4)
            expected_B = np.array([4, 4, 4, 4])  # np.ones(4) * 4
            expected_C = np.array([0, 0, 0, 0])  # np.zeros(4)
            expected_D = expected_A + expected_B + expected_C  # [4, 5, 6, 7]

            np.testing.assert_array_equal(A, expected_A, "数组A不符合预期")
            np.testing.assert_array_equal(B, expected_B, "数组B不符合预期")
            np.testing.assert_array_equal(C, expected_C, "数组C不符合预期")
            np.testing.assert_array_equal(D, expected_D, "数组D不符合预期")

            # 测试用例2：n=1 的边界情况
            A, B, C, D = target(1)
            expected_A = np.array([0])
            expected_B = np.array([1])
            expected_C = np.array([0])
            expected_D = np.array([1])

            np.testing.assert_array_equal(A, expected_A, "n=1时数组A不符合预期")
            np.testing.assert_array_equal(B, expected_B, "n=1时数组B不符合预期")
            np.testing.assert_array_equal(C, expected_C, "n=1时数组C不符合预期")
            np.testing.assert_array_equal(D, expected_D, "n=1时数组D不符合预期")

            # 测试用例3：n=6 的较大值测试
            A, B, C, D = target(6)
            expected_A = np.array([0, 1, 2, 3, 4, 5])
            expected_B = np.array([6, 6, 6, 6, 6, 6])
            expected_C = np.array([0, 0, 0, 0, 0, 0])
            expected_D = np.array([6, 7, 8, 9, 10, 11])

            np.testing.assert_array_equal(A, expected_A, "n=6时数组A不符合预期")
            np.testing.assert_array_equal(B, expected_B, "n=6时数组B不符合预期")
            np.testing.assert_array_equal(C, expected_C, "n=6时数组C不符合预期")
            np.testing.assert_array_equal(D, expected_D, "n=6时数组D不符合预期")

            # 测试数组类型和形状
            A, B, C, D = target(5)
            assert A.shape == (5,), f"数组A的形状应为(5,)，但得到{A.shape}"
            assert B.shape == (5,), f"数组B的形状应为(5,)，但得到{B.shape}"
            assert C.shape == (5,), f"数组C的形状应为(5,)，但得到{C.shape}"
            assert D.shape == (5,), f"数组D的形状应为(5,)，但得到{D.shape}"

            # 检查数组数据类型
            assert A.dtype in [np.int32, np.int64], f"数组A应为整型，但得到{A.dtype}"
            assert D.dtype in [np.int32, np.int64, np.float64], f"数组D类型错误：{D.dtype}"

            # 检查源代码
            # source_code = inspect.getsource(target)
            source_code = self.get_function_source(target.__name__)

            # 使用正则表达式更精确地匹配必须的函数
            assert re.search(r'np\.arange\s*\(', source_code), "函数中必须使用 np.arange"

            # 检查是否使用了 ones 或 ones_like
            ones_pattern = re.search(r'np\.(ones|ones_like)\s*\(', source_code)
            assert ones_pattern, "函数中必须使用 np.ones 或 np.ones_like"

            # 检查是否使用了 zeros 或 zeros_like
            zeros_pattern = re.search(r'np\.(zeros|zeros_like)\s*\(', source_code)
            assert zeros_pattern, "函数中必须使用 np.zeros 或 np.zeros_like"

            # 检查不允许的结构
            assert "for" not in source_code, "函数中不应该包含`for`循环"
            assert "while" not in source_code, "函数中不应该包含`while`循环"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题一 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))



    def test_multiply_max_min(self, target):
        """测试习题二"""
        test_name = "test_multiply_max_min"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题二 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_get_stocks_price(self, target):
        """测试习题三"""
        test_name = "test_get_stocks_price"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            expected_output = np.array([[1, 2, 3],[29, 43, 45],[22, 33, 41]])
            np.testing.assert_array_equal(target(stocks), expected_output)

            # Test case 6: Empty matrix
            stocks = np.array([[]])
            expected_output = np.array([[]])
            np.testing.assert_array_equal(target(stocks), expected_output)

            # Additional Test: Check that the function contains no loops
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题三 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_reshape_and_reverse(self, target):
        """测试习题四"""
        test_name = "test_reshape_and_reverse"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题四 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_matrix_product_and_inverse(self, target):
        """测试习题五"""
        test_name = "test_matrix_product_and_inverse"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题五 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_compute_scores(self, target):
        """测试习题六"""
        test_name = "test_compute_scores"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            self._test_no_loops(target)

            # Mark the test as passed
            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题六 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))



    def test_process_exam_results(self, target):
        """测试习题7 - numpy.where函数应用"""
        test_name = "test_process_exam_results"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：基本功能测试
            scores = np.array([95, 85, 75, 65, 55, 45, 90, 100, 0, 60])
            pass_status, grades, bonus_scores = target(scores)

            expected_pass_status = np.array([True, True, True, True, False, False, True, True, False, True])
            expected_grades = np.array(['A', 'B', 'C', 'D', 'F', 'F', 'A', 'A', 'F', 'D'])
            expected_bonus_scores = np.array([100, 85, 75, 65, 55, 45, 95, 105, 0, 60])  # 90+分加5分

            np.testing.assert_array_equal(pass_status, expected_pass_status, "通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "奖励分数计算错误")

            # 测试用例2：边界值测试
            scores = np.array([90, 89, 80, 79, 70, 69, 60, 59])
            pass_status, grades, bonus_scores = target(scores, pass_threshold=60)

            expected_pass_status = np.array([True, True, True, True, True, True, True, False])
            expected_grades = np.array(['A', 'B', 'B', 'C', 'C', 'D', 'D', 'F'])
            expected_bonus_scores = np.array([95, 89, 80, 79, 70, 69, 60, 59])  # 只有90分加奖励

            np.testing.assert_array_equal(pass_status, expected_pass_status, "边界值通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "边界值等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "边界值奖励分数计算错误")

            # 测试用例3：自定义及格线测试
            scores = np.array([85, 75, 65, 55])
            pass_status, grades, bonus_scores = target(scores, pass_threshold=70)

            expected_pass_status = np.array([True, True, False, False])
            expected_grades = np.array(['B', 'C', 'D', 'F'])  # 注意：这里D是>=60但<70，F是<60
            expected_bonus_scores = np.array([85, 75, 65, 55])  # 没有90+的分数

            np.testing.assert_array_equal(pass_status, expected_pass_status, "自定义及格线通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "自定义及格线等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "自定义及格线奖励分数计算错误")

            # 测试用例4：极端值测试
            scores = np.array([100, 0])
            pass_status, grades, bonus_scores = target(scores)

            expected_pass_status = np.array([True, False])
            expected_grades = np.array(['A', 'F'])
            expected_bonus_scores = np.array([105, 0])

            np.testing.assert_array_equal(pass_status, expected_pass_status, "极端值通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "极端值等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "极端值奖励分数计算错误")

            # 测试用例5：单个元素数组
            scores = np.array([92])
            pass_status, grades, bonus_scores = target(scores)

            expected_pass_status = np.array([True])
            expected_grades = np.array(['A'])
            expected_bonus_scores = np.array([97])

            np.testing.assert_array_equal(pass_status, expected_pass_status, "单元素数组通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "单元素数组等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "单元素数组奖励分数计算错误")

            # 测试用例6：所有学生都不及格
            scores = np.array([50, 45, 30, 25])
            pass_status, grades, bonus_scores = target(scores)

            expected_pass_status = np.array([False, False, False, False])
            expected_grades = np.array(['F', 'F', 'F', 'F'])
            expected_bonus_scores = np.array([50, 45, 30, 25])  # 没有奖励

            np.testing.assert_array_equal(pass_status, expected_pass_status, "全部不及格通过状态判断错误")
            np.testing.assert_array_equal(grades, expected_grades, "全部不及格等级分配错误")
            np.testing.assert_array_equal(bonus_scores, expected_bonus_scores, "全部不及格奖励分数计算错误")

            # 测试数组类型和形状
            scores = np.array([85, 75, 95])
            pass_status, grades, bonus_scores = target(scores)

            assert pass_status.shape == scores.shape, f"pass_status形状应为{scores.shape}，但得到{pass_status.shape}"
            assert grades.shape == scores.shape, f"grades形状应为{scores.shape}，但得到{grades.shape}"
            assert bonus_scores.shape == scores.shape, f"bonus_scores形状应为{scores.shape}，但得到{bonus_scores.shape}"

            # 检查数据类型
            assert pass_status.dtype == bool, f"pass_status应为bool类型，但得到{pass_status.dtype}"
            assert grades.dtype.kind in ['U', 'S'], f"grades应为字符串类型，但得到{grades.dtype}"
            assert bonus_scores.dtype in [np.int32, np.int64, np.float64], f"bonus_scores数据类型错误：{bonus_scores.dtype}"

            # 检查源代码 - 必须使用np.where
            source_code = self.get_function_source(target.__name__)

            # 检查必须使用np.where函数
            where_matches = re.findall(r'np\.where\s*\(', source_code)
            assert len(where_matches) >= 2, f"函数中必须使用至少2次 np.where, 但只找到{len(where_matches)}次"

            # 检查不允许的结构
            self._test_no_loops(target)
            assert "if" not in source_code or "elif" not in source_code, "应该使用np.where而不是if/elif语句进行条件判断"

            # 检查不应该使用的函数（应该用np.where代替）
            discouraged_patterns = [r'\.append\s*\(', r'\.extend\s*\(', r'list\s*\(']
            for pattern in discouraged_patterns:
                assert not re.search(pattern, source_code), f"不应该使用循环或列表操作：{pattern}，请使用np.where"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题7 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_big_countries(self, target):
        """测试习题8"""
        test_name = "test_big_countries"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
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
            self._test_no_loops(target)

            # Test passed
            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题8 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))