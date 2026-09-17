"""2022-C题统计分析教学 notebook 的自动测试。

范围限于《Practical Statistics for Data Scientists》第二版出现的方法：
t检验、QQ图、置换检验、卡方检验、Fisher精确检验、
Pearson/Spearman相关和Bonferroni校正。
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from base_test_suite import BaseTestSuite


class TestSuite2022CHypothesisTesting(BaseTestSuite):
    """测试八个单项练习和三个赛题综合练习。"""

    processed_dir = Path(__file__).resolve().parents[1] / "data" / "processed"

    @classmethod
    def _prepare_data(cls):
        basic = pd.read_csv(
            cls.processed_dir / "2022c-文物信息.csv",
            dtype={"文物编号": "string"},
        )
        valid = pd.read_csv(
            cls.processed_dir / "2022c-有效采样点.csv",
            dtype={"文物编号": "string", "文物采样点": "string"},
        )
        artifact_surface = pd.read_csv(
            cls.processed_dir / "2022c-文物采样面.csv",
            dtype={"文物编号": "string"},
        )
        components = list(artifact_surface.columns[3:])
        return basic, valid, artifact_surface, components

    def test_simple_independent_t_test(self, target):
        test_name = "test_simple_independent_t_test"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            data = artifact_surface.loc[artifact_surface["采样面状态"] == "无风化"]
            result = target(
                data, "二氧化硅(SiO2)", "类型", "高钾", "铅钡", alpha=0.05
            )
            required = {
                "n_a", "n_b", "mean_a", "mean_b", "mean_difference",
                "sd_difference", "dof", "t_statistic", "p_value",
                "is_significant",
            }
            assert isinstance(result, dict) and required.issubset(result)
            group_a = data.loc[data["类型"] == "高钾", "二氧化硅(SiO2)"].dropna()
            group_b = data.loc[data["类型"] == "铅钡", "二氧化硅(SiO2)"].dropna()
            reference = stats.ttest_ind(group_a, group_b, equal_var=True)
            assert result["n_a"] == len(group_a) == 10
            assert result["n_b"] == len(group_b) == 21
            np.testing.assert_allclose(result["mean_a"], group_a.mean())
            np.testing.assert_allclose(result["mean_b"], group_b.mean())
            np.testing.assert_allclose(result["mean_difference"], group_a.mean() - group_b.mean())
            np.testing.assert_allclose(result["sd_difference"], group_a.std() - group_b.std())
            assert result["dof"] == len(group_a) + len(group_b) - 2
            np.testing.assert_allclose(result["t_statistic"], reference.statistic)
            np.testing.assert_allclose(result["p_value"], reference.pvalue)
            assert result["is_significant"] == (reference.pvalue < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_chi_square_independence(self, target):
        test_name = "test_chi_square_independence"

        def checks():
            basic, _, _, _ = self._prepare_data()
            result = target(basic, "类型", "表面风化", alpha=0.05)
            required = {
                "table", "expected", "statistic", "p_value", "dof",
                "min_expected", "is_significant",
            }
            assert isinstance(result, dict) and required.issubset(result)
            observed = pd.crosstab(basic["类型"], basic["表面风化"])
            reference = stats.chi2_contingency(observed)
            pd.testing.assert_frame_equal(result["table"], observed)
            assert isinstance(result["expected"], pd.DataFrame)
            np.testing.assert_allclose(result["expected"], reference.expected_freq)
            np.testing.assert_allclose(result["statistic"], reference.statistic)
            np.testing.assert_allclose(result["p_value"], reference.pvalue)
            assert result["dof"] == reference.dof
            np.testing.assert_allclose(result["min_expected"], reference.expected_freq.min())
            assert result["is_significant"] == (reference.pvalue < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_fisher_exact_independence(self, target):
        test_name = "test_fisher_exact_independence"

        def checks():
            basic, _, _, _ = self._prepare_data()
            data = basic.assign(
                是否浅蓝=np.where(basic["颜色"].eq("浅蓝"), "浅蓝", "非浅蓝")
            )
            rows = ["浅蓝", "非浅蓝"]
            columns = ["无风化", "风化"]
            result = target(
                data, "是否浅蓝", "表面风化", rows, columns,
                alternative="two-sided", alpha=0.05,
            )
            observed = pd.crosstab(data["是否浅蓝"], data["表面风化"]).reindex(
                index=rows, columns=columns, fill_value=0
            )
            reference = stats.fisher_exact(observed.to_numpy(), alternative="two-sided")
            pd.testing.assert_frame_equal(result["table"], observed)
            np.testing.assert_allclose(result["odds_ratio"], reference.statistic)
            np.testing.assert_allclose(result["p_value"], reference.pvalue)
            assert result["is_significant"] == (reference.pvalue < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_prepare_qq_plot_data(self, target):
        test_name = "test_prepare_qq_plot_data"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            data = artifact_surface.loc[
                (artifact_surface["类型"] == "铅钡")
                & artifact_surface["采样面状态"].isin(["无风化", "风化"])
            ]
            result = target(data, "氧化铅(PbO)", "采样面状态", "无风化", "风化")
            required = {
                "n_a", "n_b", "qq_a", "qq_b", "slope_a", "intercept_a",
                "r_a", "slope_b", "intercept_b", "r_b",
            }
            assert isinstance(result, dict) and required.issubset(result)
            group_a = data.loc[data["采样面状态"] == "无风化", "氧化铅(PbO)"].dropna()
            group_b = data.loc[data["采样面状态"] == "风化", "氧化铅(PbO)"].dropna()
            reference_a = stats.probplot(group_a, dist="norm")
            reference_b = stats.probplot(group_b, dist="norm")
            assert result["n_a"] == len(group_a) == 21
            assert result["n_b"] == len(group_b) == 21
            for key in ["qq_a", "qq_b"]:
                assert isinstance(result[key], pd.DataFrame)
                assert list(result[key].columns) == ["theoretical_quantiles", "ordered_values"]
            np.testing.assert_allclose(result["qq_a"], np.column_stack(reference_a[0]))
            np.testing.assert_allclose(result["qq_b"], np.column_stack(reference_b[0]))
            np.testing.assert_allclose(
                [result["slope_a"], result["intercept_a"], result["r_a"]], reference_a[1]
            )
            np.testing.assert_allclose(
                [result["slope_b"], result["intercept_b"], result["r_b"]], reference_b[1]
            )

        self._run_exercise(test_name, target, checks)

    def test_welch_t_test(self, target):
        test_name = "test_welch_t_test"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            data = artifact_surface.loc[
                (artifact_surface["类型"] == "高钾")
                & artifact_surface["采样面状态"].isin(["无风化", "风化"])
            ]
            result = target(data, "氧化钾(K2O)", "采样面状态", "无风化", "风化", alpha=0.05)
            group_a = data.loc[data["采样面状态"] == "无风化", "氧化钾(K2O)"].dropna()
            group_b = data.loc[data["采样面状态"] == "风化", "氧化钾(K2O)"].dropna()
            reference = stats.ttest_ind(group_a, group_b, equal_var=False)
            assert result["n_a"] == len(group_a) == 10
            assert result["n_b"] == len(group_b) == 6
            np.testing.assert_allclose(result["mean_a"], group_a.mean())
            np.testing.assert_allclose(result["mean_b"], group_b.mean())
            np.testing.assert_allclose(result["mean_difference"], group_a.mean() - group_b.mean())
            np.testing.assert_allclose(result["statistic"], reference.statistic)
            np.testing.assert_allclose(result["p_value"], reference.pvalue)
            np.testing.assert_allclose(result["dof"], reference.df)
            assert result["is_significant"] == (reference.pvalue < 0.05)

        self._run_exercise(test_name, target, checks)

    @staticmethod
    def _permutation_reference(group_a, group_b, iterations, random_state):
        observed = group_a.mean() - group_b.mean()
        combined = np.concatenate([group_a, group_b])
        rng = np.random.default_rng(random_state)
        extreme_count = 0
        for _ in range(iterations):
            shuffled = rng.permutation(combined)
            difference = shuffled[: len(group_a)].mean() - shuffled[len(group_a):].mean()
            extreme_count += abs(difference) >= abs(observed)
        return observed, (extreme_count + 1) / (iterations + 1)

    def test_permutation_mean_test(self, target):
        test_name = "test_permutation_mean_test"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            data = artifact_surface.loc[
                (artifact_surface["类型"] == "高钾")
                & artifact_surface["采样面状态"].isin(["无风化", "风化"])
            ]
            result = target(
                data, "二氧化硅(SiO2)", "采样面状态", "无风化", "风化",
                iterations=999, random_state=123, alpha=0.05,
            )
            group_a = data.loc[data["采样面状态"] == "无风化", "二氧化硅(SiO2)"].dropna().to_numpy()
            group_b = data.loc[data["采样面状态"] == "风化", "二氧化硅(SiO2)"].dropna().to_numpy()
            observed, p_value = self._permutation_reference(group_a, group_b, 999, 123)
            assert result["n_a"] == len(group_a) == 10
            assert result["n_b"] == len(group_b) == 6
            assert result["iterations"] == 999
            np.testing.assert_allclose(result["observed_difference"], observed)
            np.testing.assert_allclose(result["p_value"], p_value)
            assert result["is_significant"] == (p_value < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_correlation_significance_test(self, target):
        test_name = "test_correlation_significance_test"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            data = artifact_surface.loc[artifact_surface["类型"] == "铅钡"]
            columns = ["氧化铅(PbO)", "氧化钡(BaO)"]
            complete = data[columns].dropna()
            for method, reference_function in [
                ("spearman", stats.spearmanr), ("pearson", stats.pearsonr)
            ]:
                result = target(data, columns[0], columns[1], method=method)
                reference = reference_function(complete[columns[0]], complete[columns[1]])
                assert result["n"] == len(complete) == 45
                np.testing.assert_allclose(result["coefficient"], reference.statistic)
                np.testing.assert_allclose(result["p_value"], reference.pvalue)
                assert result["method"] == method

        self._run_exercise(test_name, target, checks)

    def test_bonferroni_adjustment(self, target):
        test_name = "test_bonferroni_adjustment"

        def checks():
            basic, _, _, _ = self._prepare_data()
            raw = {}
            for feature in ["类型", "纹饰", "颜色"]:
                complete = basic[[feature, "表面风化"]].dropna()
                raw[feature] = stats.chi2_contingency(
                    pd.crosstab(complete[feature], complete["表面风化"])
                ).pvalue
            raw = pd.Series(raw, name="raw_p_value")
            result = target(raw, alpha=0.05)
            expected = np.minimum(raw.to_numpy() * len(raw), 1.0)
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == ["raw_p_value", "adjusted_p_value", "reject"]
            assert result.index.equals(raw.index)
            np.testing.assert_allclose(result["raw_p_value"], raw)
            np.testing.assert_allclose(result["adjusted_p_value"], expected)
            np.testing.assert_array_equal(result["reject"], expected < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_analyze_weathering_factors(self, target):
        test_name = "test_analyze_weathering_factors"

        def checks():
            basic, _, _, _ = self._prepare_data()
            features = ["类型", "纹饰", "颜色"]
            result = target(basic, features, alpha=0.05)
            columns = ["n", "levels", "chi2", "dof", "p_value", "min_expected", "is_significant"]
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == columns
            assert result.index.tolist() == features
            for feature in features:
                complete = basic[[feature, "表面风化"]].dropna()
                table = pd.crosstab(complete[feature], complete["表面风化"])
                reference = stats.chi2_contingency(table)
                assert result.loc[feature, "n"] == table.to_numpy().sum()
                assert result.loc[feature, "levels"] == table.shape[0]
                np.testing.assert_allclose(result.loc[feature, "chi2"], reference.statistic)
                assert result.loc[feature, "dof"] == reference.dof
                np.testing.assert_allclose(result.loc[feature, "p_value"], reference.pvalue)
                np.testing.assert_allclose(result.loc[feature, "min_expected"], reference.expected_freq.min())
                assert bool(result.loc[feature, "is_significant"]) == (reference.pvalue < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_compare_weathering_components(self, target):
        test_name = "test_compare_weathering_components"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            components = ["二氧化硅(SiO2)", "氧化钠(Na2O)", "氧化铅(PbO)", "氧化钡(BaO)"]
            result = target(artifact_surface, "铅钡", components, alpha=0.05)
            columns = [
                "n_no_weathering", "n_weathered", "mean_no_weathering",
                "mean_weathered", "mean_difference", "statistic", "dof",
                "raw_p_value", "adjusted_p_value", "is_significant",
            ]
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == columns
            assert result.index.tolist() == components
            subset = artifact_surface.loc[
                (artifact_surface["类型"] == "铅钡")
                & artifact_surface["采样面状态"].isin(["无风化", "风化"])
            ]
            raw = []
            for component in components:
                group_a = subset.loc[subset["采样面状态"] == "无风化", component].dropna()
                group_b = subset.loc[subset["采样面状态"] == "风化", component].dropna()
                reference = stats.ttest_ind(group_a, group_b, equal_var=False)
                raw.append(reference.pvalue)
                assert result.loc[component, "n_no_weathering"] == len(group_a)
                assert result.loc[component, "n_weathered"] == len(group_b)
                np.testing.assert_allclose(result.loc[component, "mean_no_weathering"], group_a.mean())
                np.testing.assert_allclose(result.loc[component, "mean_weathered"], group_b.mean())
                np.testing.assert_allclose(result.loc[component, "mean_difference"], group_a.mean() - group_b.mean())
                np.testing.assert_allclose(result.loc[component, "statistic"], reference.statistic)
                np.testing.assert_allclose(result.loc[component, "dof"], reference.df)
                np.testing.assert_allclose(result.loc[component, "raw_p_value"], reference.pvalue)
            adjusted = np.minimum(np.asarray(raw) * len(raw), 1.0)
            np.testing.assert_allclose(result["adjusted_p_value"], adjusted)
            np.testing.assert_array_equal(result["is_significant"], adjusted < 0.05)

        self._run_exercise(test_name, target, checks)

    def test_analyze_component_correlations(self, target):
        test_name = "test_analyze_component_correlations"

        def checks():
            _, _, artifact_surface, _ = self._prepare_data()
            components = ["二氧化硅(SiO2)", "氧化钠(Na2O)", "氧化铅(PbO)", "氧化钡(BaO)"]
            result = target(artifact_surface, "铅钡", components, method="spearman", alpha=0.05)
            columns = [
                "component_x", "component_y", "n", "coefficient",
                "raw_p_value", "adjusted_p_value", "is_significant",
            ]
            pairs = list(combinations(components, 2))
            assert isinstance(result, pd.DataFrame)
            assert list(result.columns) == columns
            assert list(zip(result["component_x"], result["component_y"])) == pairs
            subset = artifact_surface.loc[artifact_surface["类型"] == "铅钡"]
            raw = []
            for row_number, (component_x, component_y) in enumerate(pairs):
                complete = subset[[component_x, component_y]].dropna()
                reference = stats.spearmanr(complete[component_x], complete[component_y])
                raw.append(reference.pvalue)
                assert result.loc[row_number, "n"] == len(complete)
                np.testing.assert_allclose(result.loc[row_number, "coefficient"], reference.statistic)
                np.testing.assert_allclose(result.loc[row_number, "raw_p_value"], reference.pvalue)
            adjusted = np.minimum(np.asarray(raw) * len(raw), 1.0)
            np.testing.assert_allclose(result["adjusted_p_value"], adjusted)
            np.testing.assert_array_equal(result["is_significant"], adjusted < 0.05)

        self._run_exercise(test_name, target, checks)
