"""2022-C题数据预处理练习测试。"""

from pathlib import Path

import numpy as np
import pandas as pd

from base_test_suite import BaseTestSuite


class TestSuite2022CPreprocessing(BaseTestSuite):
    """测试 notebook 中五个数据预处理练习。"""

    data_file = Path(__file__).resolve().parents[1] / "data" / "2022c-附件.xlsx"

    @classmethod
    def _load_source_tables(cls):
        return pd.read_excel(
            cls.data_file,
            sheet_name=None,
            dtype={"文物编号": "string", "文物采样点": "string"},
        )

    def test_load_case_workbook(self, target):
        test_name = "test_load_case_workbook"

        def checks():
            result = target(self.data_file)
            assert isinstance(result, dict), "应返回字典"
            assert set(result) == {"表单1", "表单2", "表单3"}, "工作表名称不正确"
            assert all(isinstance(frame, pd.DataFrame) for frame in result.values()), (
                "字典中的每个值都应为 DataFrame"
            )
            assert result["表单1"].shape == (58, 5), "表单1尺寸应为58×5"
            assert result["表单2"].shape == (69, 15), "表单2尺寸应为69×15"
            assert result["表单3"].shape == (8, 16), "表单3尺寸应为8×16"
            assert result["表单1"].loc[0, "文物编号"] == "01", "文物编号01的前导零丢失"
            assert result["表单2"].loc[0, "文物采样点"] == "01", "采样点01的前导零丢失"

        self._run_exercise(test_name, target, checks)

    def test_split_sampling_points(self, target):
        test_name = "test_split_sampling_points"

        def checks():
            source_tables = self._load_source_tables()
            source = source_tables["表单2"]

            # 使用附件中的另一组记录、不同列名和不同默认值测试函数的通用性。
            selected_labels = ["01", "03部位2", "08严重风化点", "42未风化点1"]
            exercise_data = (
                source.loc[source["文物采样点"].isin(selected_labels), ["文物采样点"]]
                .rename(columns={"文物采样点": "采样标签"})
                .reset_index(drop=True)
            )
            result = target(
                exercise_data,
                label_column="采样标签",
                default_sampling_point="常规部位",
            )

            assert isinstance(result, pd.DataFrame), "应返回 DataFrame"
            assert list(result.columns) == ["文物编号", "采样点"], (
                "输出应且仅应包含文物编号、采样点两列"
            )
            assert len(result) == len(exercise_data), "输出行数应与输入相同"

            expected = pd.DataFrame(
                {
                    "文物编号": pd.Series(["01", "03", "08", "42"], dtype="string"),
                    "采样点": pd.Series(
                        ["常规部位", "部位2", "严重风化点", "未风化点1"],
                        dtype="string",
                    ),
                }
            )
            pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

            # 再使用完整附件与本题默认值，检查所有原始采样点。
            full_result = target(
                source,
                label_column="文物采样点",
                default_sampling_point="部位1",
            )
            assert full_result.shape == (69, 2), "完整表单2应拆分为69行、2列"
            first_row = full_result.iloc[0]
            assert first_row["文物编号"] == "01"
            assert first_row["采样点"] == "部位1", "名称01应使用默认采样点部位1"
            assert full_result["文物编号"].notna().all(), "附件中的编号都应成功提取"

        self._run_exercise(test_name, target, checks)

    def test_fill_not_detected_zero(self, target):
        test_name = "test_fill_not_detected_zero"

        def checks():
            example = pd.DataFrame(
                {
                    "样品": ["x", "y"],
                    "颜色": [pd.NA, "蓝绿"],
                    "成分A": [1.0, np.nan],
                    "成分B": [np.nan, 2.0],
                }
            )
            result = target(example, ["成分A", "成分B"])
            assert isinstance(result, pd.DataFrame), "应返回 DataFrame"
            assert result[["成分A", "成分B"]].isna().sum().sum() == 0, "成分列仍有空白"
            assert pd.isna(result.loc[0, "颜色"]), "不应把颜色缺失改成0"

            source_tables = self._load_source_tables()
            source = source_tables["表单2"].copy(deep=True)
            before = source.copy(deep=True)
            components = list(source.columns[1:])
            case_result = target(source, components)
            pd.testing.assert_frame_equal(source, before)
            assert case_result[components].isna().sum().sum() == 0, "所有成分空白都应被处理"

        self._run_exercise(test_name, target, checks)

    def test_add_composition_quality(self, target):
        test_name = "test_add_composition_quality"

        def checks():
            source_tables = self._load_source_tables()
            source = source_tables["表单2"].copy(deep=True)
            components = list(source.columns[1:])
            result = target(source, components)
            assert {"成分总和", "是否有效"}.issubset(result.columns), "缺少质量控制列"
            assert int(result["是否有效"].sum()) == 67, "有效采样点应为67个"
            invalid = set(result.loc[~result["是否有效"], "文物采样点"])
            assert invalid == {"15", "17"}, "无效采样点应为15和17"
            assert "成分总和" not in source.columns, "不应修改输入 DataFrame"

            boundary_data = pd.DataFrame(
                {
                    "a": [85.00, 105.00, 84.99, 105.01, np.nan],
                    "b": [0, 0, 0, 0, 100],
                }
            )
            boundary_result = target(boundary_data, ["a", "b"])
            expected = [True, True, False, False, True]
            assert boundary_result["是否有效"].tolist() == expected, (
                "85和105应包含在有效区间内，并按0处理未检出值"
            )

            custom_result = target(boundary_data, ["a", "b"], lower=90, upper=100)
            assert custom_result["是否有效"].tolist() == [False, False, False, False, True], (
                "函数应使用调用者传入的上下界"
            )

        self._run_exercise(test_name, target, checks)

    def test_build_analysis_table(self, target):
        test_name = "test_build_analysis_table"

        def checks():
            source_tables = self._load_source_tables()
            basic_info = source_tables["表单1"]
            chemical_data = source_tables["表单2"]
            result = target(basic_info, chemical_data)
            required = {
                "文物采样点",
                "文物编号",
                "采样点",
                "类型",
                "纹饰",
                "颜色",
                "表面风化",
                "采样面状态",
                "成分总和",
                "是否有效",
            }
            assert isinstance(result, pd.DataFrame), "应返回 DataFrame"
            assert len(result) == 69, "连接后应保持69个采样点"
            assert required.issubset(result.columns), "输出缺少必要字段"
            assert result["类型"].notna().all(), "存在未匹配到类型的采样点"

            indexed = result.set_index("文物采样点")
            assert indexed.loc["08严重风化点", "采样面状态"] == "严重风化"
            assert indexed.loc["08严重风化点", "采样点"] == "严重风化点"
            assert indexed.loc["23未风化点", "采样面状态"] == "无风化"
            assert indexed.loc["23未风化点", "采样点"] == "未风化点"
            assert indexed.loc["02", "采样面状态"] == "风化", "普通采样点应继承文物状态"
            assert indexed.loc["02", "采样点"] == "部位1", "普通编号应采用默认采样点"
            assert indexed.loc["03部位1", "采样面状态"] == "无风化", (
                "部位采样点应继承文物状态"
            )

            duplicated_basic = pd.concat(
                [basic_info, basic_info.iloc[[0]]], ignore_index=True
            )
            try:
                duplicate_result = target(duplicated_basic, chemical_data)
            except (ValueError, pd.errors.MergeError):
                duplicate_result = None
            if duplicate_result is not None:
                assert len(duplicate_result) == len(chemical_data), (
                    "基本信息键重复时不能静默增加行数"
                )

        self._run_exercise(test_name, target, checks)
