"""2022-C题机器学习教学 notebook 的自动测试。

测试共享基础、五种建模任务、两类敏感性分析和最终分类指标。
每个练习只承担一个明确知识点，避免重复实现相同流程。
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from base_test_suite import BaseTestSuite


class TestSuite2022CMachineLearning(BaseTestSuite):
    """测试十一道相互独立、逐步衔接的练习。"""

    required_tests_for_100_points = 11
    case_dir = Path(__file__).resolve().parents[1]
    known_file = case_dir / "data" / "processed" / "2022c-文物采样面.csv"
    unknown_file = case_dir / "data" / "processed" / "2022c-待鉴别文物.csv"
    feature_columns = [
        "二氧化硅(SiO2)", "氧化钾(K2O)", "氧化钙(CaO)",
        "氧化铝(Al2O3)", "氧化铅(PbO)", "氧化钡(BaO)",
    ]

    @classmethod
    def _raw(cls):
        known = pd.read_csv(cls.known_file, dtype={"文物编号": "string"})
        unknown = pd.read_csv(cls.unknown_file, dtype={"文物编号": "string"})
        return known, unknown

    @classmethod
    def _model_data(cls):
        known, unknown = cls._raw()
        X = known[cls.feature_columns].astype(float).reset_index(drop=True)
        y = known["类型"].map({"高钾": 0, "铅钡": 1}).astype(int).reset_index(drop=True)
        X_unknown = unknown[cls.feature_columns].astype(float).reset_index(drop=True)
        ids = unknown["文物编号"].astype("string").reset_index(drop=True)
        return known, unknown, X, y, X_unknown, ids

    @staticmethod
    def _check_prediction_table(table, ids, predictions):
        assert table.columns.tolist() == ["文物编号", "预测类型"]
        pd.testing.assert_series_equal(table["文物编号"], ids, check_names=False)
        expected = pd.Series(predictions).map({0: "高钾", 1: "铅钡"})
        pd.testing.assert_series_equal(table["预测类型"], expected, check_names=False)

    def test_build_glass_datasets(self, target):
        name = "test_build_glass_datasets"

        def checks():
            known, unknown = self._raw()
            result = target(known, unknown, self.feature_columns)
            required = {"X", "y", "known_ids", "X_unknown", "unknown_ids"}
            assert required.issubset(result)
            _, _, X, y, X_unknown, ids = self._model_data()
            pd.testing.assert_frame_equal(result["X"], X)
            pd.testing.assert_series_equal(result["y"], y)
            pd.testing.assert_frame_equal(result["X_unknown"], X_unknown)
            pd.testing.assert_series_equal(result["unknown_ids"], ids)
            assert result["X"].shape == (61, 6)
            assert result["X_unknown"].shape == (8, 6)

        self._run_exercise(name, target, checks)

    def test_scale_train_and_new(self, target):
        name = "test_scale_train_and_new"

        def checks():
            _, _, X, _, X_unknown, _ = self._model_data()
            result = target(X, X_unknown)
            scaler = StandardScaler().fit(X)
            expected_train = pd.DataFrame(
                scaler.transform(X), index=X.index, columns=X.columns
            )
            expected_new = pd.DataFrame(
                scaler.transform(X_unknown), index=X_unknown.index, columns=X_unknown.columns
            )
            pd.testing.assert_frame_equal(result["X_train_scaled"], expected_train)
            pd.testing.assert_frame_equal(result["X_new_scaled"], expected_new)
            np.testing.assert_allclose(result["scaler"].mean_, scaler.mean_)

        self._run_exercise(name, target, checks)

    def test_fit_pca_analysis(self, target):
        name = "test_fit_pca_analysis"

        def checks():
            _, _, X, _, _, _ = self._model_data()
            result = target(X, n_components=3)
            scaler = StandardScaler().fit(X)
            scaled = scaler.transform(X)
            pca = PCA(n_components=3, svd_solver="full").fit(scaled)
            expected_scores = pd.DataFrame(
                pca.transform(scaled), index=X.index,
                columns=["PC1", "PC2", "PC3"],
            )
            expected_ratio = pd.Series(
                pca.explained_variance_ratio_,
                index=expected_scores.columns,
                name="explained_variance_ratio",
            )
            expected_loadings = pd.DataFrame(
                pca.components_.T, index=X.columns,
                columns=expected_scores.columns,
            )
            pd.testing.assert_frame_equal(result["scores"], expected_scores)
            pd.testing.assert_series_equal(result["explained_variance_ratio"], expected_ratio)
            pd.testing.assert_frame_equal(result["loadings"], expected_loadings)

        self._run_exercise(name, target, checks)

    def test_predict_unknown_pca_logistic(self, target):
        name = "test_predict_unknown_pca_logistic"

        def checks():
            _, _, X, y, X_unknown, ids = self._model_data()
            result = target(X, y, X_unknown, ids, n_components=3, C=0.8)
            reference = Pipeline([
                ("scaler", StandardScaler()),
                ("pca", PCA(n_components=3, svd_solver="full")),
                ("classifier", LogisticRegression(
                    C=0.8, max_iter=2000, solver="liblinear", random_state=42
                )),
            ]).fit(X, y)
            pred = reference.predict(X_unknown)
            prob = reference.predict_proba(X_unknown)[:, 1]
            scores = reference.named_steps["pca"].transform(
                reference.named_steps["scaler"].transform(X_unknown)
            )
            np.testing.assert_array_equal(result["predictions"], pred)
            np.testing.assert_allclose(result["probabilities"], prob)
            np.testing.assert_allclose(result["unknown_pca_scores"], scores)
            self._check_prediction_table(result["prediction_table"], ids, pred)

        self._run_exercise(name, target, checks)

    def test_predict_unknown_knn(self, target):
        name = "test_predict_unknown_knn"

        def checks():
            _, _, X, y, X_unknown, ids = self._model_data()
            result = target(X, y, X_unknown, ids, n_neighbors=5)
            reference = Pipeline([
                ("scaler", StandardScaler()),
                ("classifier", KNeighborsClassifier(n_neighbors=5)),
            ]).fit(X, y)
            pred = reference.predict(X_unknown)
            np.testing.assert_array_equal(result["predictions"], pred)
            self._check_prediction_table(result["prediction_table"], ids, pred)

        self._run_exercise(name, target, checks)

    def test_predict_unknown_tree(self, target):
        name = "test_predict_unknown_tree"

        def checks():
            _, _, X, y, X_unknown, ids = self._model_data()
            result = target(X, y, X_unknown, ids, 3, 2, 42)
            reference = DecisionTreeClassifier(
                criterion="gini", max_depth=3,
                min_samples_leaf=2, random_state=42,
            ).fit(X, y)
            pred = reference.predict(X_unknown)
            np.testing.assert_array_equal(result["predictions"], pred)
            self._check_prediction_table(result["prediction_table"], ids, pred)

        self._run_exercise(name, target, checks)

    def test_predict_unknown_forest(self, target):
        name = "test_predict_unknown_forest"

        def checks():
            _, _, X, y, X_unknown, ids = self._model_data()
            result = target(X, y, X_unknown, ids, 120, 4, 42)
            reference = RandomForestClassifier(
                n_estimators=120, max_depth=4, min_samples_leaf=1,
                max_features="sqrt", random_state=42, n_jobs=1,
            ).fit(X, y)
            pred = reference.predict(X_unknown)
            prob = reference.predict_proba(X_unknown)[:, 1]
            np.testing.assert_array_equal(result["predictions"], pred)
            np.testing.assert_allclose(result["probabilities"], prob)
            expected_importance = pd.Series(
                reference.feature_importances_, index=X.columns, name="importance"
            ).sort_values(ascending=False)
            pd.testing.assert_series_equal(result["feature_importance"], expected_importance)
            self._check_prediction_table(result["prediction_table"], ids, pred)

        self._run_exercise(name, target, checks)

    def test_cluster_glass_subtypes(self, target):
        name = "test_cluster_glass_subtypes"

        def checks():
            known, _ = self._raw()
            features = [
                "二氧化硅(SiO2)", "氧化铅(PbO)",
                "氧化钡(BaO)", "五氧化二磷(P2O5)",
            ]
            result = target(known, "铅钡", features, 2, 42)
            subset = known.loc[
                known["类型"] == "铅钡",
                ["文物编号", "采样面状态", *features],
            ].dropna(subset=features).reset_index(drop=True)
            scaler = StandardScaler().fit(subset[features])
            scaled = scaler.transform(subset[features])
            model = KMeans(n_clusters=2, n_init=20, random_state=42).fit(scaled)
            expected = subset[["文物编号", "采样面状态"]].copy()
            expected["亚类"] = model.labels_ + 1
            centers = pd.DataFrame(
                scaler.inverse_transform(model.cluster_centers_),
                columns=features, index=pd.Index([1, 2], name="亚类"),
            )
            pd.testing.assert_frame_equal(result["assignments"], expected)
            pd.testing.assert_frame_equal(result["centers"], centers)

        self._run_exercise(name, target, checks)

    def test_analyze_kmeans_seed_sensitivity(self, target):
        name = "test_analyze_kmeans_seed_sensitivity"

        def checks():
            known, _ = self._raw()
            features = ["二氧化硅(SiO2)", "氧化钾(K2O)", "氧化钙(CaO)"]
            X = known.loc[known["类型"] == "高钾", features].reset_index(drop=True)
            scaled = StandardScaler().fit_transform(X)
            seeds = [1, 7, 42]
            result = target(scaled, seeds, n_clusters=2)
            base = KMeans(n_clusters=2, n_init=20, random_state=1).fit(scaled)
            base_same = base.labels_[:, None] == base.labels_[None, :]
            upper = np.triu_indices(len(X), k=1)
            expected_rows = []
            for seed in seeds:
                model = KMeans(n_clusters=2, n_init=20, random_state=seed).fit(scaled)
                same = model.labels_[:, None] == model.labels_[None, :]
                expected_rows.append({
                    "random_state": seed,
                    "inertia": model.inertia_,
                    "pair_agreement": np.mean(same[upper] == base_same[upper]),
                })
            expected = pd.DataFrame(expected_rows)
            pd.testing.assert_frame_equal(result, expected)

        self._run_exercise(name, target, checks)

    def test_analyze_prediction_sensitivity(self, target):
        name = "test_analyze_prediction_sensitivity"

        def checks():
            _, _, X, y, X_unknown, ids = self._model_data()
            model = Pipeline([
                ("scaler", StandardScaler()),
                ("pca", PCA(n_components=3, svd_solver="full")),
                ("classifier", LogisticRegression(
                    C=0.8, max_iter=2000, solver="liblinear", random_state=42
                )),
            ]).fit(X, y)
            result = target(model, X_unknown, ids, 0.02, 12, 7)
            rng = np.random.default_rng(7)
            baseline = model.predict(X_unknown)
            all_pred, all_prob = [], []
            for _ in range(12):
                changed = pd.DataFrame(
                    np.clip(
                        X_unknown.to_numpy() * rng.normal(1.0, 0.02, X_unknown.shape),
                        0, None,
                    ),
                    index=X_unknown.index,
                    columns=X_unknown.columns,
                )
                all_pred.append(model.predict(changed))
                all_prob.append(model.predict_proba(changed)[:, 1])
            all_pred, all_prob = np.asarray(all_pred), np.asarray(all_prob)
            expected = pd.DataFrame({
                "文物编号": ids,
                "基准预测": pd.Series(baseline).map({0: "高钾", 1: "铅钡"}),
                "保持基准类别比例": (all_pred == baseline).mean(axis=0),
                "铅钡预测比例": (all_pred == 1).mean(axis=0),
                "平均铅钡概率": all_prob.mean(axis=0),
                "概率标准差": all_prob.std(axis=0),
            })
            pd.testing.assert_frame_equal(result, expected)

        self._run_exercise(name, target, checks)

    def test_compute_binary_metrics(self, target):
        name = "test_compute_binary_metrics"

        def checks():
            y_true = np.array([0, 0, 0, 1, 1, 1, 1, 1])
            y_pred = np.array([0, 0, 1, 1, 1, 0, 1, 1])
            result = target(y_true, y_pred)
            matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
            tn, fp, fn, tp = matrix.ravel()
            expected = {
                "accuracy": (tn + tp) / matrix.sum(),
                "precision": tp / (tp + fp),
                "recall": tp / (tp + fn),
                "specificity": tn / (tn + fp),
                "f1": 2 * tp / (2 * tp + fp + fn),
                "balanced_accuracy": ((tp / (tp + fn)) + (tn / (tn + fp))) / 2,
            }
            np.testing.assert_array_equal(result["confusion_matrix"], matrix)
            for key, value in expected.items():
                np.testing.assert_allclose(result[key], value)

        self._run_exercise(name, target, checks)
