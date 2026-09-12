from util.notebook_info_extractor import is_valid_email, normalize_email


def test_is_valid_email_accepts_student_address():
    assert is_valid_email("student@example.com")
    assert is_valid_email(" student.name+lab@example.edu.cn ")


def test_is_valid_email_rejects_missing_or_malformed_address():
    for value in (None, "", "未填写", "student@", "@example.com", "a b@example.com"):
        assert not is_valid_email(value)


def test_normalize_email_lowercases_only_the_domain():
    assert normalize_email("Student.Name@QQ.COM") == "Student.Name@qq.com"
