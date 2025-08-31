# tests/test_suite5.py
from pathlib import Path
from base_test_suite import BaseTestSuite
import pandas as pd
import numpy as np
from io import StringIO
import pytest
from termcolor import colored
import inspect

class TestSuite5(BaseTestSuite):
    """实验5的测试套件"""

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
            "Bedrooms": [6, 4, 4, 5, 4],
            "BldgGrade": [7, 10, 8, 7, 7]
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
            self._print_test_failure(test_name, e)

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
            self._print_test_failure(test_name, e)

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
            self._print_test_failure(test_name, e)

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
            self._print_test_failure(test_name, e)

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
            self._print_test_failure(test_name, e)

    def test_compute_metrics(self, target):
        """测试混淆矩阵指标计算函数"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1：给定的混淆矩阵
            cm1 = np.array([[828, 52], [33, 1027]])

            # 手工计算预期结果
            # TN=828, FP=52, FN=33, TP=1027
            # accuracy = (1027 + 828) / (1027 + 828 + 52 + 33) = 1855/1940 ≈ 0.9562
            # recall = 1027 / (1027 + 33) = 1027/1060 ≈ 0.9689
            # precision = 1027 / (1027 + 52) = 1027/1079 ≈ 0.9518
            # f1_score = 2 * (0.9518 * 0.9689) / (0.9518 + 0.9689) ≈ 0.9603

            expected_metrics1 = {
                "accuracy": 1855/1940,
                "recall": 1027/1060,
                "precision": 1027/1079,
                "f1_score": 2 * (1027/1079) * (1027/1060) / ((1027/1079) + (1027/1060))
            }

            metrics1 = target(cm1)

            # 验证返回值类型
            assert isinstance(metrics1, dict), f"返回值应为字典类型, 实际类型为{type(metrics1)}"

            # 验证字典包含所有必要的键
            required_keys = ["accuracy", "recall", "precision", "f1_score"]
            for key in required_keys:
                assert key in metrics1, f"返回字典缺少键: {key}"

            # 验证各个指标的数值
            for key in required_keys:
                assert isinstance(metrics1[key], (int, float, np.float64)), f"{key}应为数值类型, 实际类型为{type(metrics1[key])}"
                assert np.allclose(metrics1[key], expected_metrics1[key], rtol=1e-6), \
                    f"{key}计算错误。预期: {expected_metrics1[key]:.6f}, 实际: {metrics1[key]:.6f}"

            # 测试用例2：完美分类的情况
            cm2 = np.array([[500, 0], [0, 300]])
            expected_metrics2 = {
                "accuracy": 1.0,
                "recall": 1.0,
                "precision": 1.0,
                "f1_score": 1.0
            }

            metrics2 = target(cm2)
            for key in required_keys:
                assert np.allclose(metrics2[key], expected_metrics2[key], rtol=1e-6), \
                    f"完美分类测试失败。{key}: 预期 {expected_metrics2[key]}, 实际 {metrics2[key]}"

            # 测试用例3：边界情况
            cm3 = np.array([[100, 50], [25, 75]])
            expected_metrics3 = {
                "accuracy": (100 + 75) / (100 + 50 + 25 + 75),  # 175/250 = 0.7
                "recall": 75 / (75 + 25),                        # 75/100 = 0.75
                "precision": 75 / (75 + 50),                     # 75/125 = 0.6
                "f1_score": 2 * (0.6 * 0.75) / (0.6 + 0.75)     # 2*0.45/1.35 ≈ 0.6667
            }

            metrics3 = target(cm3)
            for key in required_keys:
                assert np.allclose(metrics3[key], expected_metrics3[key], rtol=1e-6), \
                    f"边界测试失败。{key}: 预期 {expected_metrics3[key]:.6f}, 实际 {metrics3[key]:.6f}"

            # 验证指标范围
            for metrics in [metrics1, metrics2, metrics3]:
                for key in required_keys:
                    assert 0 <= metrics[key] <= 1, f"{key}应在[0,1]范围内, 实际值为{metrics[key]}"

            self.test_results[test_name] = 1
            print(colored(f"习题6通过 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))