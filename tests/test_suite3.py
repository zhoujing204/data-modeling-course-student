import inspect
from base_test_suite import BaseTestSuite
from termcolor import colored

class TestSuite3(BaseTestSuite):
    """实验3的测试套件"""

    def test_solve_machine_production_lp(self, target):
        """测试习题1"""
        test_name = "test_solve_machine_production_lp"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 调用目标函数并检查返回结果
            result = target()

            # 检查返回的结果是否包含所有必需的键
            expected_keys = {"status", "甲机床生产数量", "乙机床生产数量", "总利润"}
            assert expected_keys.issubset(result.keys()), f"返回结果应包含键：{expected_keys}"

            # 检查最优解状态：状态应为 Optimal
            assert result["status"] == "Optimal", "期望的状态应为 Optimal"

            # 检查最优生产数量和总利润（允许细微浮点误差）
            assert abs(result["甲机床生产数量"] - 2) < 1e-6, "甲机床生产数量计算错误"
            assert abs(result["乙机床生产数量"] - 6) < 1e-6, "乙机床生产数量计算错误"
            assert abs(result["总利润"] - 26000) < 1e-6, "总利润计算错误"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题1 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_formulate_lp_problem(self, target):
        """测试习题2"""
        test_name = "test_formulate_lp_problem"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            m = 4
            n = 3
            list_c = [1, 1, 1]
            list_a = [ [2, 1, 2], [1, 0, 0], [0, 1, 0], [0, 0, -1]]
            list_b = [5, 7, 9, 4]
            (is_feas, is_bnded, sols) = target(m, n, list_c, list_a, list_b)

            assert is_feas, '这个线性规划问题是有解的 -- 你的代码返回结果是无解'
            assert is_bnded, '这个线性规划问题是有界的 -- 你的代码返回结果是无界的'
            # print("测试用例的解：",sols)
            assert abs(sols[0] - 2.0) <= 1E-04 , 'x0 must be 2.0'
            assert abs(sols[1] - 9.0) <= 1E-04 , 'x1 must be 9.0'
            assert abs(sols[2] + 4.0) <= 1E-04 , 'x2 must be -4.0'

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题2 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_solve_investment_problem(self, target):
        """测试习题3"""
        test_name = "test_solve_investment_problem"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            result = target()
            assert result["status"] == "Optimal", "期望的状态应为 Optimal"
            assert abs(result["profit"] - 1098.59) <= 0.1, "目标函数计算错误"
            assert abs(result["x1"] - 33.83) <= 0.1, "x1 计算错误"
            assert abs(result["x2"] - 0.0) <= 0.1, "x2 计算错误"
            assert abs(result["x3"] - 0.0) <= 0.1, "x3 计算错误"
            assert abs(result["x4"] - 104.45) <= 0.1, "x4 计算错误"
            assert abs(result["x5"] - 32.05) <= 0.1, "x5 计算错误"
            assert abs(result["x6"] - 0.0) <= 0.1, "x6 计算错误"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题3 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))