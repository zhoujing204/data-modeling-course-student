import re
import pytest
from base_test_suite import BaseTestSuite
from termcolor import colored

class TestSuite1(BaseTestSuite):
    """实验1的测试套件"""

    def test_format_user_info(self, target):
        """测试习题一 - 用户信息格式化"""
        test_name = "test_format_user_info"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1:基本功能测试
            user_data = "john,doe,john.doe@gmail.com,25"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: John Doe, Age: 25, Email: john.doe@gmail.com"
            expected_email_domain = "gmail.com"
            expected_initials = "J.D."

            assert formatted_info == expected_formatted_info, f"格式化信息错误:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"邮箱域名错误:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"姓名缩写错误:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例2:包含空格和大小写混合的数据
            user_data = " ALICE , smith , Alice.Smith@YAHOO.COM , 30 "
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: Alice Smith, Age: 30, Email: alice.smith@yahoo.com"
            expected_email_domain = "yahoo.com"
            expected_initials = "A.S."

            assert formatted_info == expected_formatted_info, f"混合格式测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"域名大小写处理错误:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"首字母处理错误:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例3:复杂邮箱格式
            user_data = "bob,wilson,bob.wilson@hotmail.com,45"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: Bob Wilson, Age: 45, Email: bob.wilson@hotmail.com"
            expected_email_domain = "hotmail.com"
            expected_initials = "B.W."

            assert formatted_info == expected_formatted_info, f"复杂邮箱测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"hotmail域名测试失败:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"复杂姓名缩写测试失败:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例4:单字母姓名
            user_data = "a,b,a.b@test.org,18"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: A B, Age: 18, Email: a.b@test.org"
            expected_email_domain = "test.org"
            expected_initials = "A.B."

            assert formatted_info == expected_formatted_info, f"单字母姓名测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"org域名测试失败:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"单字母缩写测试失败:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例5:长名字测试
            user_data = "christopher,montgomery,chris.montgomery@university.edu,35"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: Christopher Montgomery, Age: 35, Email: chris.montgomery@university.edu"
            expected_email_domain = "university.edu"
            expected_initials = "C.M."

            assert formatted_info == expected_formatted_info, f"长名字测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"edu域名测试失败:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"长名字缩写测试失败:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例6:小写姓名测试
            user_data = "mary,jane,mary.jane@company.net,28"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: Mary Jane, Age: 28, Email: mary.jane@company.net"
            expected_email_domain = "company.net"
            expected_initials = "M.J."

            assert formatted_info == expected_formatted_info, f"小写姓名测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"net域名测试失败:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"小写姓名缩写测试失败:期望 '{expected_initials}', 得到 '{initials}'"

            # 测试用例7:混合大小写邮箱
            user_data = "david,brown,DAVID.Brown@Example.COM,40"
            formatted_info, email_domain, initials = target(user_data)

            expected_formatted_info = "Name: David Brown, Age: 40, Email: david.brown@example.com"
            expected_email_domain = "example.com"
            expected_initials = "D.B."

            assert formatted_info == expected_formatted_info, f"混合大小写邮箱测试失败:期望 '{expected_formatted_info}', 得到 '{formatted_info}'"
            assert email_domain == expected_email_domain, f"混合大小写域名测试失败:期望 '{expected_email_domain}', 得到 '{email_domain}'"
            assert initials == expected_initials, f"混合大小写缩写测试失败:期望 '{expected_initials}', 得到 '{initials}'"

            # 检查返回值类型
            assert isinstance(formatted_info, str), f"formatted_info应为字符串类型, 得到{type(formatted_info)}"
            assert isinstance(email_domain, str), f"email_domain应为字符串类型, 得到{type(email_domain)}"
            assert isinstance(initials, str), f"initials应为字符串类型, 得到{type(initials)}"

            # 检查返回值格式
            assert formatted_info.startswith("Name: "), f"formatted_info应以'Name: '开头"
            assert ", Age: " in formatted_info, f"formatted_info应包含', Age: '"
            assert ", Email: " in formatted_info, f"formatted_info应包含', Email: '"
            assert len(initials) == 4, f"initials长度应为4（如'J.D.'）, 得到长度{len(initials)}"
            assert initials[1] == '.' and initials[3] == '.', f"initials格式应为'F.L.', 得到'{initials}'"

            # 检查源代码 - 必须使用指定的字符串方法
            source_code = self.get_function_source(target.__name__)
            # print("source:", str(source_code))

            # 检查f-string的使用
            assert 'f"' in source_code or "f'" in source_code, "函数中必须使用f-string格式化字符串"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题一 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_nearest_sq(self, target):
        """测试习题二 - 最近完全平方数"""
        test_name = "test_nearest_sq"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 基本测试用例
            assert target(1) == 1, f"1的最近完全平方数应为1, 得到{target(1)}"
            assert target(2) == 1, f"2的最近完全平方数应为1, 得到{target(2)}"
            assert target(10) == 9, f"10的最近完全平方数应为9, 得到{target(10)}"
            assert target(111) == 121, f"111的最近完全平方数应为121, 得到{target(111)}"
            assert target(9999) == 10000, f"9999的最近完全平方数应为10000, 得到{target(9999)}"

            # 检查源代码
            source_code = self.get_function_source(target.__name__)


            # 检查代码长度
            code_lines = [line.strip() for line in source_code.split('\n')
                        if line.strip() and not line.strip().startswith('#')]
            # print(code_lines)
            function_body_lines = [line for line in code_lines if not line.startswith('def ') and not line.startswith('return ')]
            # print(function_body_lines)

            assert len(function_body_lines) <= 2, f"函数体应控制在2行以内, 实际{len(function_body_lines)}行"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题二 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_analyze_scores(self, target):
        """测试习题三 - 学生成绩分析器"""
        test_name = "test_analyze_scores"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1:基本功能测试
            scores = [85, 92, 78, 96, 88, 73, 90]
            result = target(scores)
            high_scores, top_half, last_three, pass_count = result

            expected_high_scores = [92, 96, 90]
            expected_top_half = [85, 92, 78]  # 7个元素的前一半是前3个
            expected_last_three = [90, 73, 88]
            expected_pass_count = 7

            assert high_scores == expected_high_scores, f"高分成绩错误:期望{expected_high_scores}, 得到{high_scores}"
            assert top_half == expected_top_half, f"前一半成绩错误:期望{expected_top_half}, 得到{top_half}"
            assert last_three == expected_last_three, f"最后3个倒序错误:期望{expected_last_three}, 得到{last_three}"
            assert pass_count == expected_pass_count, f"及格人数错误:期望{expected_pass_count}, 得到{pass_count}"

            # 测试用例2:偶数长度列表
            scores = [95, 87, 92, 78, 83, 91]
            result = target(scores)
            high_scores, top_half, last_three, pass_count = result

            expected_high_scores = [95, 92, 91]
            expected_top_half = [95, 87, 92]  # 6个元素的前一半是前3个
            expected_last_three = [91, 83, 78]
            expected_pass_count = 6

            assert high_scores == expected_high_scores, f"偶数长度高分错误:期望{expected_high_scores}, 得到{high_scores}"
            assert top_half == expected_top_half, f"偶数长度前一半错误:期望{expected_top_half}, 得到{top_half}"
            assert last_three == expected_last_three, f"偶数长度最后3个错误:期望{expected_last_three}, 得到{last_three}"
            assert pass_count == expected_pass_count, f"偶数长度及格人数错误:期望{expected_pass_count}, 得到{pass_count}"

            # 测试用例3:包含不及格分数
            scores = [45, 92, 55, 89, 67, 94, 38]
            result = target(scores)
            high_scores, top_half, last_three, pass_count = result

            expected_high_scores = [92, 94]
            expected_top_half = [45, 92, 55]
            expected_last_three = [38, 94, 67]
            expected_pass_count = 4  # 92, 89, 67, 94

            assert high_scores == expected_high_scores, f"含不及格高分错误:期望{expected_high_scores}, 得到{high_scores}"
            assert top_half == expected_top_half, f"含不及格前一半错误:期望{expected_top_half}, 得到{top_half}"
            assert last_three == expected_last_three, f"含不及格最后3个错误:期望{expected_last_three}, 得到{last_three}"
            assert pass_count == expected_pass_count, f"含不及格及格人数错误:期望{expected_pass_count}, 得到{pass_count}"

            # 测试用例4:所有分数都很高
            scores = [95, 96, 91, 98, 92]
            result = target(scores)
            high_scores, top_half, last_three, pass_count = result

            expected_high_scores = [95, 96, 91, 98, 92]
            expected_top_half = [95, 96]
            expected_last_three = [92, 98, 91]
            expected_pass_count = 5

            assert high_scores == expected_high_scores, f"全高分测试错误:期望{expected_high_scores}, 得到{high_scores}"
            assert pass_count == expected_pass_count, f"全高分及格人数错误:期望{expected_pass_count}, 得到{pass_count}"

            # 测试用例5:边界值测试
            scores = [60, 89, 90, 59, 100]
            result = target(scores)
            high_scores, top_half, last_three, pass_count = result

            expected_high_scores = [90, 100]
            expected_top_half = [60, 89]
            expected_last_three = [100, 59, 90]
            expected_pass_count = 4  # 60, 89, 90, 100

            assert high_scores == expected_high_scores, f"边界值高分错误:期望{expected_high_scores}, 得到{high_scores}"
            assert pass_count == expected_pass_count, f"边界值及格人数错误:期望{expected_pass_count}, 得到{pass_count}"

            # 检查返回值类型
            assert isinstance(result, tuple), f"返回值应为元组, 得到{type(result)}"
            assert len(result) == 4, f"返回值应包含4个元素, 得到{len(result)}个"
            assert isinstance(high_scores, list), f"high_scores应为列表, 得到{type(high_scores)}"
            assert isinstance(top_half, list), f"top_half应为列表, 得到{type(top_half)}"
            assert isinstance(last_three, list), f"last_three应为列表, 得到{type(last_three)}"
            assert isinstance(pass_count, int), f"pass_count应为整数, 得到{type(pass_count)}"


            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题三 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_createDict(self, target):
        """测试习题四 - 智能字典创建器"""
        test_name = "test_createDict"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1:values不够的情况
            result = target(['a', 'b', 'c', 'd'], [1, 2, 3])
            expected = {'a': 1, 'b': 2, 'c': 3, 'd': None}
            assert result == expected, f"values不够时错误:期望{expected}, 得到{result}"

            # 测试用例2:keys不够的情况
            result = target(['a', 'b', 'c'], [1, 2, 3, 4])
            expected = {'a': 1, 'b': 2, 'c': 3}
            assert result == expected, f"keys不够时错误:期望{expected}, 得到{result}"

            # 测试用例3:长度相等
            result = target(['x', 'y'], [10, 20])
            expected = {'x': 10, 'y': 20}
            assert result == expected, f"长度相等时错误:期望{expected}, 得到{result}"

            # 测试用例4:空列表
            result = target([], [])
            expected = {}
            assert result == expected, f"空列表错误:期望{expected}, 得到{result}"

            # 测试用例5:keys有值values为空
            result = target(['a', 'b'], [])
            expected = {'a': None, 'b': None}
            assert result == expected, f"values为空错误:期望{expected}, 得到{result}"

            # 检查返回值类型
            result = target(['test'], ['value'])
            assert isinstance(result, dict), f"返回值应为字典类型, 得到{type(result)}"

            # 检查源代码
            source_code = self.get_function_source(target.__name__)
            assert "{" in source_code and "for" in source_code, "应使用字典推导式"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题四 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_smart_calculator(self, target):
        """测试习题五 - 智能计算器"""
        test_name = "test_smart_calculator"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1: 基本位置参数 - 加法
            result = target('add', 1, 2, 3, 4)
            assert result == 10.0, f"基本加法错误: 期望10.0, 得到{result}"

            # 测试用例2: 基本位置参数 - 乘法
            result = target('multiply', 2, 3, 4)
            assert result == 24.0, f"基本乘法错误: 期望24.0, 得到{result}"

            # 测试用例3: precision关键字参数
            result = target('add', 1.33, 2.67, precision=1)
            assert result == 4.0, f"精度1错误: 期望4.0, 得到{result}"

            result = target('add', 1.4, 1.7, precision=0)
            assert result == 3, f"精度0错误: 期望3, 得到{result}"

            # 测试用例4: show_steps关键字参数
            result = target('add', 1, 2, 3, show_steps=True)
            expected_patterns = ['1 + 2 + 3', '= 6']
            assert all(pattern in str(result) for pattern in expected_patterns), \
                f"加法步骤显示错误: {result}"

            result = target('multiply', 2, 3, show_steps=True)
            expected_patterns = ['2 * 3', '= 6']
            assert all(pattern in str(result) for pattern in expected_patterns), \
                f"乘法步骤显示错误: {result}"

            # 测试用例5: **options参数 - unit
            result = target('add', 10, 20, unit='kg')
            assert '30' in str(result) and 'kg' in str(result), \
                f"单位显示错误: {result}"

            # 测试用例6: **options参数 - name
            result = target('add', 5, 15, name='总和')
            assert '总和' in str(result) and '20' in str(result), \
                f"名称显示错误: {result}"

            # 测试用例7: 多个关键字参数组合
            result = target('multiply', 2, 3, 4, precision=1,
                        unit='个', name='总数量')
            assert all(x in str(result) for x in ['总数量', '24', '个']), \
                f"组合参数错误: {result}"

            # 测试用例8: show_steps + options组合
            result = target('add', 10, 20, 30, show_steps=True,
                        name='总重量', unit='kg')
            result_str = str(result)
            assert '总重量' in result_str and '60kg' in result_str, \
                f"步骤+选项组合错误: {result}"

            # 测试用例9: 单个数字
            result = target('add', 5)
            assert result == 5, f"单数字加法错误: 期望5, 得到{result}"

            result = target('multiply', 7)
            assert result == 7, f"单数字乘法错误: 期望7, 得到{result}"

            # 测试用例10: 空数字列表
            result = target('add')
            assert result == 0.0, f"空列表加法错误: 期望0, 得到{result}"

            # 测试用例11: 不支持的操作
            result = target('subtract', 5, 3)
            assert '不支持' in str(result), f"不支持操作处理错误: {result}"

            # 测试用例12: 浮点数处理
            result = target('add', 1.5, 2.3, 3.4, precision=1)
            assert result == 7.2, f"浮点数加法错误: 期望7.2, 得到{result}"

            # 测试用例13:  precision为负数
            result = target('add', 22,  33, precision=-1)
            assert result == 60, f"负数精度处理错误: 期望60, 获得{result}"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题五 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))

    def test_find_senior(self, target):
        """测试习题六 - 查找最年长的开发人员"""
        test_name = "test_find_senior"
        self.test_results[test_name] = 0
        self.test_targets[test_name] = target

        try:
            # 测试用例1: 基本功能 - 多个最年长者
            programmers1 = [
                {'firstName': 'Gabriel', 'lastName': 'X.', 'country': 'Monaco',
                'continent': 'Europe', 'age': 49, 'language': 'PHP'},
                {'firstName': 'Odval', 'lastName': 'F.', 'country': 'Mongolia',
                'continent': 'Asia', 'age': 38, 'language': 'Python'},
                {'firstName': 'Emilija', 'lastName': 'S.', 'country': 'Lithuania',
                'continent': 'Europe', 'age': 19, 'language': 'Python'},
                {'firstName': 'Sou', 'lastName': 'B.', 'country': 'Japan',
                'continent': 'Asia', 'age': 49, 'language': 'PHP'}
            ]

            result = target(programmers1)
            expected = [
                {'firstName': 'Gabriel', 'lastName': 'X.', 'country': 'Monaco',
                'continent': 'Europe', 'age': 49, 'language': 'PHP'},
                {'firstName': 'Sou', 'lastName': 'B.', 'country': 'Japan',
                'continent': 'Asia', 'age': 49, 'language': 'PHP'}
            ]

            assert len(result) == 2, f"应返回2个最年长者, 实际返回{len(result)}个"
            assert result == expected, f"多个最年长者测试失败: 期望{expected}, 得到{result}"

            # 测试用例2: 只有一个最年长者
            programmers2 = [
                {'firstName': 'Alice', 'lastName': 'A.', 'country': 'USA',
                'continent': 'North America', 'age': 25, 'language': 'JavaScript'},
                {'firstName': 'Bob', 'lastName': 'B.', 'country': 'Canada',
                'continent': 'North America', 'age': 30, 'language': 'Python'},
                {'firstName': 'Carol', 'lastName': 'C.', 'country': 'UK',
                'continent': 'Europe', 'age': 35, 'language': 'Java'}
            ]

            result = target(programmers2)
            expected = [
                {'firstName': 'Carol', 'lastName': 'C.', 'country': 'UK',
                'continent': 'Europe', 'age': 35, 'language': 'Java'}
            ]

            assert len(result) == 1, f"应返回1个最年长者, 实际返回{len(result)}个"
            assert result == expected, f"单个最年长者测试失败: 期望{expected}, 得到{result}"

            # 测试用例3: 所有人年龄相同
            programmers3 = [
                {'firstName': 'John', 'lastName': 'D.', 'country': 'Australia',
                'continent': 'Oceania', 'age': 28, 'language': 'C++'},
                {'firstName': 'Jane', 'lastName': 'E.', 'country': 'New Zealand',
                'continent': 'Oceania', 'age': 28, 'language': 'Ruby'},
                {'firstName': 'Jack', 'lastName': 'F.', 'country': 'Fiji',
                'continent': 'Oceania', 'age': 28, 'language': 'Go'}
            ]

            result = target(programmers3)
            assert len(result) == 3, f"所有人同龄应返回3人, 实际返回{len(result)}人"
            assert result == programmers3, f"所有人同龄测试失败: 期望{programmers3}, 得到{result}"

            # 测试用例5: 单个元素列表
            programmers5 = [
                {'firstName': 'Solo', 'lastName': 'S.', 'country': 'Iceland',
                'continent': 'Europe', 'age': 42, 'language': 'Haskell'}
            ]

            result = target(programmers5)
            assert result == programmers5, f"单元素列表测试失败: 期望{programmers5}, 得到{result}"

            # 测试用例6: 年龄为0的边界情况
            programmers6 = [
                {'firstName': 'Young', 'lastName': 'Y.', 'country': 'Country1',
                'continent': 'Continent1', 'age': 0, 'language': 'Python'},
                {'firstName': 'Older', 'lastName': 'O.', 'country': 'Country2',
                'continent': 'Continent2', 'age': 25, 'language': 'Java'}
            ]

            result = target(programmers6)
            expected = [programmers6[1]]
            assert result == expected, f"年龄0边界测试失败: 期望{expected}, 得到{result}"

            self.test_results[test_name] = 1
            print(colored(f"恭喜你通过了习题六 {test_name} 测试。{sum(self.test_results.values())}/{len(self.test_results)}", "green"))

        except Exception as e:
            print(colored(f"测试失败 {test_name}: {str(e)}", "red"))