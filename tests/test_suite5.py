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

    def test_analyze_ab_conversion_ztest(self, target):
        """测试习题6：两总体比例z检验"""
        test_name = inspect.currentframe().f_code.co_name
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            data_path = Path().resolve() / "data" / "ab_conversion_ztest.csv"
            result = target(data_path)
            expected = (
                0.082,
                0.09807692307692308,
                0.016076923076923072,
                2.8334907021995037,
                0.004604264737460241,
                True,
            )

            assert isinstance(result, tuple), "函数应返回tuple"
            assert len(result) == 6, "应该返回6项数据"
            for index in range(5):
                assert result[index] == pytest.approx(expected[index], rel=1e-6), \
                    f"返回结果第{index + 1}项计算错误"
            assert isinstance(result[5], (bool, np.bool_)), "是否显著应为布尔值"
            assert bool(result[5]) is expected[5], "显著性判断错误"

            # 使用行顺序相反的模拟数据，确保学生根据variant列选择数据。
            mock_csv = StringIO(
                "variant,visitors,conversions\n"
                "Personalized page,500,50\n"
                "Original page,500,40\n"
            )
            mock_result = target(mock_csv)
            mock_expected = (
                0.08,
                0.10,
                0.02,
                1.10498924021966,
                0.2691642514676925,
                False,
            )

            for index in range(5):
                assert mock_result[index] == pytest.approx(mock_expected[index], rel=1e-6), \
                    f"模拟数据第{index + 1}项计算错误"
            assert bool(mock_result[5]) is mock_expected[5], "模拟数据显著性判断错误"

            # 验证alpha参数参与显著性判断。
            mock_csv.seek(0)
            relaxed_alpha_result = target(mock_csv, alpha=0.30)
            assert bool(relaxed_alpha_result[5]) is True, "应使用传入的alpha判断显著性"

            self._test_no_loops(target)
            self.test_results[test_name] = 1
            print(colored(
                f"习题6通过 {test_name} 测试。"
                f"{sum(self.test_results.values())}/{len(self.test_results)}",
                "green",
            ))

        except Exception as e:
            self._print_test_failure(test_name, e)
