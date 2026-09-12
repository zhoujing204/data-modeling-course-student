import json
import re
from bs4 import BeautifulSoup


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_valid_email(value):
    """Return whether a student supplied a usable email address."""
    if not isinstance(value, str):
        return False
    email = value.strip()
    return (
        0 < len(email) <= 254
        and EMAIL_RE.fullmatch(email) is not None
        and not any(ord(char) < 32 for char in email)
    )


def normalize_email(value):
    """Validate an email address and lowercase its domain for comparison."""
    if not is_valid_email(value):
        raise ValueError("Email地址无效")
    local, domain = value.strip().rsplit("@", 1)
    return f"{local}@{domain.casefold()}"

def clean_string(s):
    if not s:
        return s
    # 移除常见非法文件字符
    return re.sub(r'[\\/:*?"<>|]', '', s).strip()

def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    target_fields = {
        '班级': 'class_id',
        '学号': 'student_id',
        '姓名': 'name',
        'Email': 'email'
    }

    result = {}
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) != 2:
            continue

        field_name = clean_string(cols[0].get_text(strip=True))

        if field_name in target_fields:
            value = clean_string(cols[1].get_text(strip=True))
            result[target_fields[field_name]] = value if value else None

    return result


def extract_from_ipynb(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            for line in cell['source']:
                if 'data-id="student-info"' in line.lower():
                    return extract_info("\n".join(cell['source']))
    return {}
