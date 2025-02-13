# 实验4的测试集， 进行实验的同学请不要修改测试文件的内容。
import sys
from termcolor import colored
import inspect
from pulp import constants
from random import randint, seed

test_results = {  }
test_targets = {  }

def test_solve_worker_assignment_lp(target):
    """测试习题1"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    # 调用目标函数并检查返回结果
    result = target()

    # 检查返回的结果是否包含所有必需的键
    expected_keys = {"status", "total_time"}
    assert expected_keys.issubset(result.keys()), f"返回结果应包含键：{expected_keys}"

    # 检查最优解状态：状态应为 Optimal
    assert result["status"] == "Optimal", "期望的状态应为 Optimal"

    # 检查最优生产数量和总利润（允许细微浮点误差）
    assert abs(result["total_time"] - 70) < 1e-6, "最小消耗时间计算错误"

    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题1 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))

def test_plan_invite_list(target):
    """测试派对邀请名单规划问题"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

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
        test_results[test_name] = 1
        print(colored(f"恭喜你通过了{test_name}测试。{sum(test_results.values())}/{len(test_results)}", "green"))
    except AssertionError as e:
        print(colored(f"测试失败：{str(e)}", "red"))
    except Exception as e:
        print(colored(f"测试出现错误：{str(e)}", "red"))

def test_encode_and_solve_three_coloring(target):
    """测试习题3"""
    test_name= inspect.currentframe().f_code.co_name
    test_results[test_name] = 0
    test_targets[test_name] = target

    def check_three_color_assign(n, edge_list, color_assign):
        assert len(color_assign) == n, f'Error: 你的颜色分配列表的长度为{len(color_assign)}, 应该等于节点数{n}'
        assert (all( col == 'r' or col == 'b' or col == 'g' for col in color_assign),
                f'错误: 颜色分配列表中的值应该为r, g, 或者b. 你的代码返回的是{color_assign}')
        for (i, j) in edge_list:
            ci = color_assign[i]
            cj = color_assign[j]
            assert ci != cj, f' 错误: 边 ({i,j}) 有相同的颜色 ({ci, cj})'

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


    test_results[test_name] = 1
    print(colored(f"恭喜你通过了习题3 {test_name} 测试。{sum(test_results.values())}/{len(test_results)}", "green"))


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
