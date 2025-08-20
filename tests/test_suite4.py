import inspect
from base_test_suite import BaseTestSuite
from termcolor import colored

class TestSuite4(BaseTestSuite):
    """实验4的测试套件"""

    def test_plan_invite_list(self, target):
        """测试派对邀请名单规划问题"""
        test_name = "test_plan_invite_list"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        # 测试用例1
        def inner_test_case_1():
            n = 20
            m = 12
            T_lists = [[1, 5, 12, 18, 19], [2, 3, 4, 6, 7],
                       [1, 2, 4, 7, 8, 9, 10, 11, 12, 14, 16],
                       [1, 3, 4, 5, 6, 13, 15, 17, 18, 19],
                       [1, 5, 7, 8, 9, 19]]
            G_lists = [[1, 5], [5, 19], [4, 7], [4, 12], [4, 19],
                       [4, 18], [3, 4, 15, 19], [4, 7, 18, 2]]
            pp_scores = [1, 2, 2, 1, 4, 5, 1, 2, 3, 4, 5, 1, 2,
                        3.5, 1, 0.6, 0, 1, 8, 8]

            status, result, optimal_pp_score = target(n, m, T_lists, G_lists, pp_scores)
            expected_result = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0,
                              0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                              0.0, 0.0]
            expected_pp_score = 18.1

            assert status == 1, "测试用例1状态应为1"
            assert len(result) == n, f"结果长度应为{n}"
            assert all(abs(a-b) < 1e-6 for a, b in zip(result, expected_result)), "测试用例1结果不符合预期"
            assert abs(optimal_pp_score - expected_pp_score) < 1e-6, "目标函数结果错误"

        # 测试用例2
        def inner_test_case_2():
            from random import seed, randint
            seed(1)
            n = 16
            m = 8
            num_teams = 4
            num_grievances = 3
            T_lists = [list(set([randint(0, n-1) for k in range(randint(3,10))]))
                      for i in range(num_teams)]
            G_lists = [list(set([randint(0, n-1) for k in range(randint(2,4))]))
                      for i in range(num_grievances)]
            pp_scores = [randint(0, 8) for i in range(n)]

            status, result, optimal_pp_score = target(n, m, T_lists, G_lists, pp_scores)
            expected_result = [0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                              0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0]
            expected_pp_score = 29

            assert status == 1, "测试用例2状态应为1"
            assert len(result) == n, f"结果长度应为{n}"
            assert all(abs(a-b) < 1e-6 for a, b in zip(result, expected_result)), "测试用例2结果不符合预期"
            assert abs(optimal_pp_score - expected_pp_score) < 1e-6, "目标函数结果错误"

        # 执行测试用例
        try:
            inner_test_case_1()
            inner_test_case_2()
            self.test_results[test_name] = 1
            print(colored(f"习题2通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_encode_and_solve_three_coloring(self, target):
        """测试习题3 - 三色图着色问题"""
        test_name = "test_encode_and_solve_three_coloring"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        def check_three_color_assign(n, edge_list, color_assign):
            assert len(color_assign) == n, f'Error: 你的颜色分配列表的长度为{len(color_assign)}, 应该等于节点数{n}'
            assert (all( col == 'r' or col == 'b' or col == 'g' for col in color_assign)),\
                   f'错误: 颜色分配列表中的值应该为r, g, 或者b. 你的代码返回的是{color_assign}'
            for (i, j) in edge_list:
                ci = color_assign[i]
                cj = color_assign[j]
                assert ci != cj, f' 错误: 边 ({i,j}) 有相同的颜色 ({ci, cj})'

        try:
            # 测试用例1
            n = 5
            edge_list = [(1,2), (1, 3), (1,4), (2, 4), (3,4)]
            # 调用目标函数并检查返回结果
            (flag, color_assign) = target(n, edge_list)
            assert flag == True, "错误： 这个图可以用三种颜色覆盖, 应该返回True"
            check_three_color_assign(n, edge_list, color_assign)

            # 测试用例2
            n = 5
            edge_list = [(1,2), (1, 3), (1,4), (2,3), (2, 4), (3,4)]
            (flag, color_assign) = target(n, edge_list)
            assert flag == False, "错误： 这个图不能用三种颜色覆盖, 应该返回False"

            # 测试用例3
            n = 10
            edge_list = [ (1, 5), (1, 7), (1, 9), (2, 4), (2, 5), (2, 9), (3, 4), (3, 6), (3,7), (3,8), (4, 5), (4,6), (4,7), (4,9),(5,6), (5,7),(6,8),(7,9),(8,9)]
            (flag, color_assign) = target(n, edge_list)
            assert flag == True, "错误： 这个图可以用三种颜色覆盖, 应该返回True"
            check_three_color_assign(n, edge_list, color_assign)

            self.test_results[test_name] = 1
            print(colored(f"习题3通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))


        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))


    def test_solve_worker_assignment_lp(self, target):
        """测试习题1"""
        test_name= inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
        # 调用目标函数并检查返回结果
            result = target()

            # 检查返回的结果是否包含所有必需的键
            expected_keys = {"status", "total_time"}
            assert expected_keys.issubset(result.keys()), f"返回结果应包含键：{expected_keys}"

            # 检查最优解状态：状态应为 Optimal
            assert result["status"] == "Optimal", "期望的状态应为 Optimal"

            # 检查最优生产数量和总利润（允许细微浮点误差）
            assert abs(result["total_time"] - 70) < 1e-6, "最小消耗时间计算错误"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题1 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))
