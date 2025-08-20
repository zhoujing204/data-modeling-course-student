# test_suite6.py
from pathlib import Path
from base_test_suite import BaseTestSuite
import pandas as pd
import numpy as np
from io import StringIO
import pytest
from termcolor import colored
import inspect

class TestSuite6(BaseTestSuite):
    """实验6的测试套件"""

    def test_get_dataset_info(self, target):
        """测试数据集信息获取函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：标准情况
            train_set_x_orig = np.random.randint(0, 255, size=(100, 64, 64, 3), dtype=np.uint8)
            test_set_x_orig = np.random.randint(0, 255, size=(25, 64, 64, 3), dtype=np.uint8)

            result = target(train_set_x_orig, test_set_x_orig)

            # 检查返回值结构
            assert len(result) == 3, "应该返回3个值: m_train, m_test, num_px"
            m_train, m_test, num_px = result

            # 检查返回值的正确性
            assert m_train == 100, f"训练样本数量应为100, 实际为 {m_train}"
            assert m_test == 25, f"测试样本数量应为25, 实际为 {m_test}"
            assert num_px == 64, f"图像尺寸应为64, 实际为 {num_px}"

            # 测试用例2：不同尺寸的图像
            train_set_x_orig_2 = np.random.randint(0, 255, size=(200, 32, 32, 3), dtype=np.uint8)
            test_set_x_orig_2 = np.random.randint(0, 255, size=(50, 32, 32, 3), dtype=np.uint8)

            result_2 = target(train_set_x_orig_2, test_set_x_orig_2)
            m_train_2, m_test_2, num_px_2 = result_2

            assert m_train_2 == 200, f"训练样本数量应为200, 实际为 {m_train_2}"
            assert m_test_2 == 50, f"测试样本数量应为50, 实际为 {m_test_2}"
            assert num_px_2 == 32, f"图像尺寸应为32, 实际为 {num_px_2}"

            # 测试用例3：边界情况 - 最小数据集
            train_set_x_orig_3 = np.random.randint(0, 255, size=(1, 16, 16, 3), dtype=np.uint8)
            test_set_x_orig_3 = np.random.randint(0, 255, size=(1, 16, 16, 3), dtype=np.uint8)

            result_3 = target(train_set_x_orig_3, test_set_x_orig_3)
            m_train_3, m_test_3, num_px_3 = result_3

            assert m_train_3 == 1, f"训练样本数量应为1, 实际为 {m_train_3}"
            assert m_test_3 == 1, f"测试样本数量应为1, 实际为 {m_test_3}"
            assert num_px_3 == 16, f"图像尺寸应为16, 实际为 {num_px_3}"

            # 测试用例4：大数据集
            train_set_x_orig_4 = np.random.randint(0, 255, size=(1000, 128, 128, 3), dtype=np.uint8)
            test_set_x_orig_4 = np.random.randint(0, 255, size=(200, 128, 128, 3), dtype=np.uint8)

            result_4 = target(train_set_x_orig_4, test_set_x_orig_4)
            m_train_4, m_test_4, num_px_4 = result_4

            assert m_train_4 == 1000, f"训练样本数量应为1000, 实际为 {m_train_4}"
            assert m_test_4 == 200, f"测试样本数量应为200, 实际为 {m_test_4}"
            assert num_px_4 == 128, f"图像尺寸应为128, 实际为 {num_px_4}"

            # 检查返回值类型
            assert isinstance(m_train, (int, np.integer)), f"m_train应为整数类型, 实际为 {type(m_train)}"
            assert isinstance(m_test, (int, np.integer)), f"m_test应为整数类型, 实际为 {type(m_test)}"
            assert isinstance(num_px, (int, np.integer)), f"num_px应为整数类型, 实际为 {type(num_px)}"

            # 检查是否使用了循环
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题1通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_reshape_image_dataset(self, target):
        """测试图像数据集重塑函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：标准情况 - 64x64 图像
            train_set = np.random.randint(0, 255, size=(100, 64, 64, 3), dtype=np.uint8)
            test_set = np.random.randint(0, 255, size=(25, 64, 64, 3), dtype=np.uint8)

            result = target(train_set, test_set)

            # 检查返回值结构
            assert len(result) == 2, "应该返回2个值: train_set_flatten, test_set_flatten"
            train_set_flatten, test_set_flatten = result

            # 检查形状是否正确
            expected_train_shape = (64 * 64 * 3, 100)  # (num_px * num_px * 3, m_train)
            expected_test_shape = (64 * 64 * 3, 25)    # (num_px * num_px * 3, m_test)

            assert train_set_flatten.shape == expected_train_shape, \
                f"训练集重塑后形状应为 {expected_train_shape}, 实际为 {train_set_flatten.shape}"
            assert test_set_flatten.shape == expected_test_shape, \
                f"测试集重塑后形状应为 {expected_test_shape}, 实际为 {test_set_flatten.shape}"

            # 验证数据完整性 - 检查总像素数是否保持不变
            assert train_set_flatten.size == train_set.size, \
                f"训练集重塑后总元素数应保持不变，原始: {train_set.size}, 重塑后: {train_set_flatten.size}"
            assert test_set_flatten.size == test_set.size, \
                f"测试集重塑后总元素数应保持不变，原始: {test_set.size}, 重塑后: {test_set_flatten.size}"

            # 测试用例2：不同尺寸 - 32x32 图像
            train_set_2 = np.random.randint(0, 255, size=(200, 32, 32, 3), dtype=np.uint8)
            test_set_2 = np.random.randint(0, 255, size=(50, 32, 32, 3), dtype=np.uint8)

            result_2 = target(train_set_2, test_set_2)
            train_set_flatten_2, test_set_flatten_2 = result_2

            expected_train_shape_2 = (32 * 32 * 3, 200)
            expected_test_shape_2 = (32 * 32 * 3, 50)

            assert train_set_flatten_2.shape == expected_train_shape_2, \
                f"训练集重塑后形状应为 {expected_train_shape_2}, 实际为 {train_set_flatten_2.shape}"
            assert test_set_flatten_2.shape == expected_test_shape_2, \
                f"测试集重塑后形状应为 {expected_test_shape_2}, 实际为 {test_set_flatten_2.shape}"

            # 测试用例3：边界情况 - 小数据集
            train_set_3 = np.random.randint(0, 255, size=(1, 16, 16, 3), dtype=np.uint8)
            test_set_3 = np.random.randint(0, 255, size=(1, 16, 16, 3), dtype=np.uint8)

            result_3 = target(train_set_3, test_set_3)
            train_set_flatten_3, test_set_flatten_3 = result_3

            expected_train_shape_3 = (16 * 16 * 3, 1)
            expected_test_shape_3 = (16 * 16 * 3, 1)

            assert train_set_flatten_3.shape == expected_train_shape_3, \
                f"训练集重塑后形状应为 {expected_train_shape_3}, 实际为 {train_set_flatten_3.shape}"
            assert test_set_flatten_3.shape == expected_test_shape_3, \
                f"测试集重塑后形状应为 {expected_test_shape_3}, 实际为 {test_set_flatten_3.shape}"

            # 测试用例4：验证数据内容一致性（使用已知数据）
            # 创建一个简单的测试数据来验证重塑的正确性
            simple_train = np.arange(24).reshape(1, 2, 2, 6)  # 1个样本，2x2图像，6个通道
            simple_test = np.arange(24, 48).reshape(1, 2, 2, 6)

            simple_result = target(simple_train, simple_test)
            simple_train_flatten, simple_test_flatten = simple_result

            # 检查第一个训练样本的重塑是否正确
            expected_train_flatten_shape = (2 * 2 * 6, 1)  # (24, 1)
            assert simple_train_flatten.shape == expected_train_flatten_shape, \
                f"简单测试案例训练集形状错误: 期望 {expected_train_flatten_shape}, 实际 {simple_train_flatten.shape}"

            # 验证重塑后的数据顺序正确
            # 原始数据: shape (1, 2, 2, 6)，重塑后应为 (24, 1)
            original_flattened = simple_train.reshape(1, -1).T  # 应该是 (24, 1)
            np.testing.assert_array_equal(simple_train_flatten, original_flattened,
                                        "重塑后的数据内容与期望不符")

            # 测试用例5：大数据集
            train_set_5 = np.random.randint(0, 255, size=(500, 128, 128, 3), dtype=np.uint8)
            test_set_5 = np.random.randint(0, 255, size=(100, 128, 128, 3), dtype=np.uint8)

            result_5 = target(train_set_5, test_set_5)
            train_set_flatten_5, test_set_flatten_5 = result_5

            expected_train_shape_5 = (128 * 128 * 3, 500)
            expected_test_shape_5 = (128 * 128 * 3, 100)

            assert train_set_flatten_5.shape == expected_train_shape_5, \
                f"大数据集训练集重塑后形状应为 {expected_train_shape_5}, 实际为 {train_set_flatten_5.shape}"
            assert test_set_flatten_5.shape == expected_test_shape_5, \
                f"大数据集测试集重塑后形状应为 {expected_test_shape_5}, 实际为 {test_set_flatten_5.shape}"

            # 检查返回值类型
            assert isinstance(train_set_flatten, np.ndarray), \
                f"train_set_flatten应为numpy数组, 实际为 {type(train_set_flatten)}"
            assert isinstance(test_set_flatten, np.ndarray), \
                f"test_set_flatten应为numpy数组, 实际为 {type(test_set_flatten)}"

            # 检查数据类型保持不变
            assert train_set_flatten.dtype == train_set.dtype, \
                f"训练集数据类型应保持不变, 原始: {train_set.dtype}, 重塑后: {train_set_flatten.dtype}"
            assert test_set_flatten.dtype == test_set.dtype, \
                f"测试集数据类型应保持不变, 原始: {test_set.dtype}, 重塑后: {test_set_flatten.dtype}"

            # 检查是否使用了循环
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题2通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_sigmoid(self, target):
        """测试sigmoid激活函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：关键数值验证
            assert abs(target(0) - 0.5) < 1e-10, "sigmoid(0)应等于0.5"
            assert abs(target(2) - 0.8807970779778823) < 1e-10, "sigmoid(2)计算错误"
            assert abs(target(-2) - 0.11920292202211755) < 1e-10, "sigmoid(-2)计算错误"

            # 测试用例2：输出范围验证
            extreme_values = np.array([-100, -10, 0, 10, 100])
            result = target(extreme_values)
            # print("测试用例2: 输出范围验证", result)
            assert np.all(result >= 0) and np.all(result <= 1), "sigmoid输出应在[0,1]范围内"

            # 测试用例3：特定数组输入验证
            test_array = np.array([-2, 0, 2, 10, 3])
            expected_output = np.array([
                0.11920292202211755,  # sigmoid(-2)
                0.5,                  # sigmoid(0)
                0.8807970779778823,   # sigmoid(2)
                0.9999546021312976,   # sigmoid(10)
                0.9525741268224334    # sigmoid(3)
            ])

            result_array = target(test_array)
            np.testing.assert_array_almost_equal(result_array, expected_output, decimal=10,
                err_msg="sigmoid计算结果不符合预期")

            # 检查是否使用了循环
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题3通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_initialize_with_zeros(self, target):
        """测试参数初始化函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例：标准维度
            dim = 10
            w, b = target(dim)

            # 验证w的形状和值
            assert w.shape == (dim, 1), f"w的形状应为({dim}, 1), 实际为{w.shape}"
            assert np.all(w == 0), "w应为全零向量"

            # 验证b的类型和值
            assert isinstance(b, (int, float)), f"b应为数值类型, 实际为{type(b)}"
            assert b == 0, f"b应为0, 实际为{b}"

            # 检查是否使用了循环
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题4通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_propagate(self, target):
        """测试前向和反向传播函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 创建简单的测试数据
            w = np.array([[0.1], [0.2]])  # 2个特征
            b = 0.5
            X = np.array([[1, 2], [3, 4]])  # 2个特征，2个样本
            Y = np.array([[1, 0]])  # 2个样本的标签

            grads, cost = target(w, b, X, Y)

            # 验证返回值结构
            assert isinstance(grads, dict), "grads应为字典类型"
            assert "dw" in grads and "db" in grads, "grads应包含'dw'和'db'键"

            # 验证梯度形状
            assert grads["dw"].shape == w.shape, f"dw形状应为{w.shape}, 实际为{grads['dw'].shape}"
            assert isinstance(grads["db"], (int, float, np.float64)), f"db应为标量, 实际类型为{type(grads['db'])}"

            # 验证cost为0维numpy数组
            assert isinstance(cost, np.ndarray), f"cost应为numpy数组, 实际类型为{type(cost)}"
            assert cost.ndim == 0, f"cost应为0维数组, 实际维度为{cost.ndim}"
            assert cost.item() >= 0, "交叉熵损失应为非负数"

            # 验证具体的预期值
            expected_cost = 0.9823478726603917
            expected_dw = np.array([[0.70183687], [1.28793613]])
            expected_db = 0.2930496298463307

            # 数值验证
            np.testing.assert_almost_equal(cost, expected_cost, decimal=6,
                err_msg="cost计算结果不符合预期")
            np.testing.assert_array_almost_equal(grads["dw"], expected_dw, decimal=6,
                err_msg="dw计算结果不符合预期")
            np.testing.assert_almost_equal(grads["db"], expected_db, decimal=6,
                err_msg="db计算结果不符合预期")

            # 检查是否使用了循环
            self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题5通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_optimize(self, target):
        """测试梯度下降优化函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 使用参考测试用例的数据
            w = np.array([[1.], [2.]])
            b = 2.
            X = np.array([[1., 2., -1.], [3., 4., -3.2]])
            Y = np.array([[1, 0, 1]])

            # 预期结果
            expected_w = np.array([[-0.70916784], [-0.42390859]])
            expected_b = np.float64(2.26891346)

            expected_dw = np.array([[0.06188603], [-0.01407361]])
            expected_db = np.float64(-0.04709353)

            expected_cost = [5.80154532, 0.31057104]

            # 调用目标函数
            params, grads, costs = target(w, b, X, Y, num_iterations=101, learning_rate=0.1, print_cost=False)

            # 验证 costs
            assert isinstance(costs, list), "costs应为列表类型"
            assert len(costs) == 2, f"costs长度错误。{len(costs)} != 2"
            np.testing.assert_allclose(costs, expected_cost,
                err_msg=f"costs值不符合预期。{costs} != {expected_cost}")

            # 验证 grads
            assert isinstance(grads, dict), "grads应为字典类型"
            assert "dw" in grads and "db" in grads, "grads应包含'dw'和'db'键"

            assert isinstance(grads['dw'], np.ndarray), f"grads['dw']类型错误。{type(grads['dw'])} != np.ndarray"
            assert grads['dw'].shape == w.shape, f"grads['dw']形状错误。{grads['dw'].shape} != {w.shape}"
            assert np.allclose(grads['dw'], expected_dw), f"grads['dw']值不符合预期。{grads['dw']} != {expected_dw}"
            assert np.allclose(grads['db'], expected_db), f"grads['db']值不符合预期。{grads['db']} != {expected_db}"


            # 验证 params
            assert isinstance(params, dict), "params应为字典类型"
            assert "w" in params and "b" in params, "params应包含'w'和'b'键"

            assert isinstance(params['w'], np.ndarray), f"params['w']类型错误。{type(params['w'])} != np.ndarray"
            assert params['w'].shape == w.shape, f"params['w']形状错误。{params['w'].shape} != {w.shape}"
            assert np.allclose(params['w'], expected_w), f"params['w']值不符合预期。{params['w']} != {expected_w}"
            assert np.allclose(params['b'], expected_b), f"params['b']值不符合预期。{params['b']} != {expected_b}"

            self.test_results[test_name] = 1
            print(colored(f"习题6通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}",
                          "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_predict(self, target):
        """测试预测函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 创建简单的测试数据
            w = np.array([[0.3], [-0.2]])  # 2个特征
            b = 0.1
            X = np.array([[1, 2, -1], [0.5, -1.5, 2]])  # 2个特征，3个样本

            Y_prediction = target(w, b, X)

            # 验证返回值类型和形状
            assert isinstance(Y_prediction, np.ndarray), f"Y_prediction应为numpy数组, 实际类型为{type(Y_prediction)}"
            assert Y_prediction.shape == (1, X.shape[1]), f"Y_prediction形状应为(1, {X.shape[1]}), 实际为{Y_prediction.shape}"

            # 验证预测值只包含0和1
            unique_values = np.unique(Y_prediction)
            assert all(val in [0, 1] for val in unique_values), f"预测值应只包含0和1, 实际包含{unique_values}"

            # 验证预测结果的数据类型
            assert Y_prediction.dtype in [int, float, np.int64, np.float64], f"预测值数据类型错误: {Y_prediction.dtype}"

            # 手工计算预期结果进行验证
            # 对于给定的w, b, X:
            # 样本1: sigmoid(0.3*1 + (-0.2)*0.5 + 0.1) = sigmoid(0.3) ≈ 0.574 > 0.5 → 1
            # 样本2: sigmoid(0.3*2 + (-0.2)*(-1.5) + 0.1) = sigmoid(1.0) ≈ 0.731 > 0.5 → 1
            # 样本3: sigmoid(0.3*(-1) + (-0.2)*2 + 0.1) = sigmoid(-0.6) ≈ 0.354 < 0.5 → 0
            expected_prediction = np.array([[1, 1, 0]])

            np.testing.assert_array_equal(Y_prediction, expected_prediction,
                err_msg=f"预测结果不符合预期。预期: {expected_prediction}, 实际: {Y_prediction}")

            # 检查是否对预测部分使用了循环（这里predict函数本身包含必要的循环）
            # self._test_no_loops(target)

            self.test_results[test_name] = 1
            print(colored(f"习题7通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_model(self, target):
        """测试完整的逻辑回归模型"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 设置随机种子确保结果可重复
            np.random.seed(0)

            # 预期输出结果
            expected_output = {
                'costs': [np.array(0.69314718)],
                'Y_prediction_test': np.array([[1., 1., 0.]]),
                'Y_prediction_train': np.array([[1., 1., 0., 1., 0., 0., 1.]]),
                'w': np.array([[ 0.08639757],
                            [-0.08231268],
                            [-0.11798927],
                            [ 0.12866053]]),
                'b': -0.03983236094816321
            }

            # 训练数据：4个特征，7个样本
            b, Y, X = 1.5, np.array([[1, 0, 0, 1, 0, 0, 1]]), np.random.randn(4, 7)

            # 测试数据：4个特征，3个样本
            x_test = np.random.randn(4, 3)
            y_test = np.array([[0, 1, 0]])

            # 调用目标函数
            d = target(X, Y, x_test, y_test, num_iterations=50, learning_rate=0.01)

            # 验证 costs
            assert isinstance(d['costs'], list), f"d['costs']类型错误。{type(d['costs'])} != list"
            assert len(d['costs']) == 1, f"d['costs']长度错误。{len(d['costs'])} != 1"
            assert np.allclose(d['costs'], expected_output['costs']), f"d['costs']值不符合预期。{d['costs']} != {expected_output['costs']}"

            # 验证 w
            assert isinstance(d['w'], np.ndarray), f"d['w']类型错误。{type(d['w'])} != np.ndarray"
            assert d['w'].shape == (X.shape[0], 1), f"d['w']形状错误。{d['w'].shape} != {(X.shape[0], 1)}"
            assert np.allclose(d['w'], expected_output['w']), f"d['w']值不符合预期。{d['w']} != {expected_output['w']}"

            # 验证 b
            assert np.allclose(d['b'], expected_output['b']), f"d['b']值不符合预期。{d['b']} != {expected_output['b']}"

            # 验证 Y_prediction_test
            assert isinstance(d['Y_prediction_test'], np.ndarray), f"d['Y_prediction_test']类型错误。{type(d['Y_prediction_test'])} != np.ndarray"
            assert d['Y_prediction_test'].shape == (1, x_test.shape[1]), f"d['Y_prediction_test']形状错误。{d['Y_prediction_test'].shape} != {(1, x_test.shape[1])}"
            assert np.allclose(d['Y_prediction_test'], expected_output['Y_prediction_test']), f"d['Y_prediction_test']值不符合预期。{d['Y_prediction_test']} != {expected_output['Y_prediction_test']}"

            # 验证 Y_prediction_train
            assert isinstance(d['Y_prediction_train'], np.ndarray), f"d['Y_prediction_train']类型错误。{type(d['Y_prediction_train'])} != np.ndarray"
            assert d['Y_prediction_train'].shape == (1, X.shape[1]), f"d['Y_prediction_train']形状错误。{d['Y_prediction_train'].shape} != {(1, X.shape[1])}"
            assert np.allclose(d['Y_prediction_train'], expected_output['Y_prediction_train']), f"d['Y_prediction_train']值不符合预期。{d['Y_prediction_train']} != {expected_output['Y_prediction_train']}"

            self.test_results[test_name] = 1
            print(colored(f"习题8通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))