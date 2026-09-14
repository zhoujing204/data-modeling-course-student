import ast
import textwrap

import pandas as pd

from base_test_suite import BaseTestSuite
from termcolor import colored


class TestSuite3(BaseTestSuite):
    """实验3：pandas 数据处理测试套件。"""

    def _assert_no_explicit_loops(self, target):
        """要求习题使用 pandas 向量化操作，不使用显式 for/while 循环。"""
        source = self.get_function_source(target.__name__)
        if not source:
            return
        tree = ast.parse(textwrap.dedent(source))
        loop_nodes = (ast.For, ast.AsyncFor, ast.While)
        assert not any(isinstance(node, loop_nodes) for node in ast.walk(tree)), \
            "请使用 pandas 向量化操作，不要使用 for 或 while 循环"

    def _run_test(self, test_name, target, assertions):
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target
        try:
            assertions()
            self._assert_no_explicit_loops(target)
            self.test_results[test_name] = 1
            passed = sum(self.test_results.values())
            total = len(self.test_results)
            print(colored(f"恭喜你通过了 {test_name} 测试。{passed}/{total}", "green"))
        except Exception as exc:
            print(colored(f"测试失败 {test_name}: {exc}", "red"))

    def test_select_large_discount_orders(self, target):
        """测试习题1：订单筛选、索引和复合排序。"""
        test_name = "test_select_large_discount_orders"

        def assertions():
            orders = pd.DataFrame({
                "order_id": ["O4", "O2", "O3", "O1", "O5"],
                "order_date": ["2026-03-02", "2026-03-01", "2026-03-03", "2026-03-04", "2026-03-05"],
                "customer_id": ["C2", "C1", "C3", "C1", "C4"],
                "product_id": ["P2", "P1", "P3", "P4", "P5"],
                "quantity": [5, 5, 3, 2, 4],
                "discount": [0.15, 0.15, 0.20, 0.25, None],
            })
            original = orders.copy(deep=True)
            result = target(orders, min_quantity=3, min_discount=0.15)
            expected = pd.DataFrame(
                {
                    "order_date": ["2026-03-01", "2026-03-02", "2026-03-03"],
                    "customer_id": ["C1", "C2", "C3"],
                    "product_id": ["P1", "P2", "P3"],
                    "quantity": [5, 5, 3],
                    "discount": [0.15, 0.15, 0.20],
                },
                index=pd.Index(["O2", "O4", "O3"], name="order_id"),
            )
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(orders, original)

        self._run_test(test_name, target, assertions)

    def test_clean_customer_records(self, target):
        """测试习题2：客户缺失值、重复值和字符串类型。"""
        test_name = "test_clean_customer_records"

        def assertions():
            customers = pd.DataFrame({
                "customer_id": ["C2", "C1", "C2", "C3"],
                "customer_name": ["Bob Li", "Alice Zhang", "Bob Revised", "Chen Wu"],
                "city": ["Beijing", "Shanghai", "Shenzhen", None],
                "segment": ["teacher", "student", "corporate", "student"],
                "email": ["old@example.com", None, "new@example.com", None],
            })
            original = customers.copy(deep=True)
            result = target(customers)
            expected = pd.DataFrame({
                "customer_id": ["C3", "C2", "C1"],
                "customer_name": ["Chen Wu", "Bob Li", "Alice Zhang"],
                "city": [None, "Beijing", "Shanghai"],
                "segment": pd.Series(["student", "teacher", "student"], dtype="string"),
                "email": ["unknown", "old@example.com", "unknown"],
            })
            pd.testing.assert_frame_equal(result, expected, check_dtype=True)
            pd.testing.assert_frame_equal(customers, original)

        self._run_test(test_name, target, assertions)

    def test_standardize_product_text(self, target):
        """测试习题3：商品文本字段标准化。"""
        test_name = "test_standardize_product_text"

        def assertions():
            products = pd.DataFrame({
                "product_id": ["P2", "P1", "P2", "P3"],
                "product_name": [" desk lamp ", "wireless MOUSE", "old lamp", " USB-C hub "],
                "category": [" Home ", "ELECTRONICS", "home", " Electronics "],
                "unit_price": [80.0, 120.0, 75.0, 60.0],
                "status": [" active ", "INACTIVE", "inactive", " Active "],
            })
            original = products.copy(deep=True)
            result = target(products)
            expected = pd.DataFrame({
                "product_id": ["P2", "P3", "P1"],
                "product_name": ["Desk Lamp", "Usb-C Hub", "Wireless Mouse"],
                "category": ["home", "electronics", "electronics"],
                "unit_price": [80.0, 60.0, 120.0],
                "status": ["ACTIVE", "ACTIVE", "INACTIVE"],
            })
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(products, original)

        self._run_test(test_name, target, assertions)

    def test_add_order_size_band(self, target):
        """测试习题4：订单数量分箱和分类类型。"""
        test_name = "test_add_order_size_band"

        def assertions():
            orders = pd.DataFrame({
                "order_id": ["O1", "O2", "O3", "O4", "O5"],
                "quantity": [0.5, 1.0, 1.01, 3.0, 3.01],
            })
            original = orders.copy(deep=True)
            result = target(orders)
            expected_values = ["单件", "单件", "小批", "小批", "大批"]
            assert result.columns.tolist() == ["order_id", "quantity", "order_size"]
            assert result["order_size"].astype("string").tolist() == expected_values
            assert isinstance(result["order_size"].dtype, pd.CategoricalDtype)
            assert result["order_size"].cat.ordered
            assert result["order_size"].cat.categories.tolist() == ["单件", "小批", "大批"]
            pd.testing.assert_frame_equal(orders, original)

        self._run_test(test_name, target, assertions)

    def test_build_stock_sales_detail(self, target):
        """测试习题5：库存销售连接、基数校验和派生列。"""
        test_name = "test_build_stock_sales_detail"

        def assertions():
            inventory = pd.DataFrame({
                "product_id": ["P1", "P2", "P3"],
                "warehouse": ["Shanghai", "Shanghai", "Shanghai"],
                "stock": [10, 8, 5],
            })
            monthly_sales = pd.DataFrame({
                "product_id": ["P1", "P3", "P4"],
                "2026-02": [90, 70, 30],
                "2026-03": [100, 75, 40],
            })
            originals = [inventory.copy(deep=True), monthly_sales.copy(deep=True)]
            result = target(inventory, monthly_sales)
            expected = pd.DataFrame({
                "product_id": ["P3", "P1"],
                "warehouse": ["Shanghai", "Shanghai"],
                "stock": [5, 10],
                "2026-03": [75, 100],
                "sales_per_stock": [15.0, 10.0],
            })
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(inventory, originals[0])
            pd.testing.assert_frame_equal(monthly_sales, originals[1])

            duplicated_sales = pd.concat(
                [monthly_sales, monthly_sales.iloc[[0]]], ignore_index=True
            )
            try:
                target(inventory, duplicated_sales)
            except pd.errors.MergeError:
                pass
            else:
                raise AssertionError("连接必须使用 validate='one_to_one' 检查重复键")

        self._run_test(test_name, target, assertions)

    def test_summarize_customer_orders(self, target):
        """测试习题6：按客户分组和命名聚合。"""
        test_name = "test_summarize_customer_orders"

        def assertions():
            orders = pd.DataFrame({
                "order_id": ["O1", "O1", "O2", "O3", "O4"],
                "customer_id": ["C1", "C1", "C1", "C2", "C3"],
                "product_id": ["P1", "P2", "P2", "P1", "P3"],
                "quantity": [2, 1, 3, 4, 1],
                "discount": [0.0, 0.1, 0.2, 0.15, 0.05],
            })
            original = orders.copy(deep=True)
            result = target(orders)
            expected = pd.DataFrame({
                "customer_id": ["C1", "C2", "C3"],
                "order_count": [2, 1, 1],
                "product_count": [2, 1, 1],
                "total_quantity": [6, 4, 1],
                "average_discount": [0.1, 0.15, 0.05],
            })
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(orders, original)

        self._run_test(test_name, target, assertions)

    def test_summarize_order_batches(self, target):
        """测试习题7：纵向拼接订单批次并汇总。"""
        test_name = "test_summarize_order_batches"

        def assertions():
            first_batch = pd.DataFrame({
                "order_id": ["O1", "O2"],
                "customer_id": ["C1", "C2"],
                "quantity": [2, 5],
            })
            second_batch = pd.DataFrame({
                "order_id": ["O3", "O4"],
                "customer_id": ["C1", "C3"],
                "quantity": [2, 2],
            })
            originals = [first_batch.copy(deep=True), second_batch.copy(deep=True)]
            result = target(first_batch, second_batch)
            expected = pd.DataFrame({
                "customer_id": ["C2", "C1", "C3"],
                "order_count": [1, 2, 1],
                "total_quantity": [5, 4, 2],
            })
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(first_batch, originals[0])
            pd.testing.assert_frame_equal(second_batch, originals[1])

        self._run_test(test_name, target, assertions)

    def test_reshape_product_attributes(self, target):
        """测试习题8：商品属性宽表转长表。"""
        test_name = "test_reshape_product_attributes"

        def assertions():
            products = pd.DataFrame({
                "product_id": ["P1", "P2"],
                "product_name": ["Mouse", "Lamp"],
                "category": ["Electronics", "Home"],
                "unit_price": [10.0, 20.0],
                "status": ["active", "inactive"],
            })
            original = products.copy(deep=True)
            result = target(products)
            expected = pd.DataFrame({
                "product_id": ["P1", "P1", "P1", "P2", "P2", "P2"],
                "unit_price": [10.0, 10.0, 10.0, 20.0, 20.0, 20.0],
                "attribute": ["category", "product_name", "status"] * 2,
                "value": ["Electronics", "Mouse", "active", "Home", "Lamp", "inactive"],
            })
            pd.testing.assert_frame_equal(result, expected)
            pd.testing.assert_frame_equal(products, original)

        self._run_test(test_name, target, assertions)
