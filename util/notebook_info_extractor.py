import json

from bs4 import BeautifulSoup

def extract_info(html_content):
    # print('html_contents:', html_content)
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

        field_name = cols[0].get_text(strip=True)
        if field_name in target_fields:
            value = cols[1].get_text(strip=True)
            result[target_fields[field_name]] = value if value else None

    return result


def extract_from_ipynb(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # print("len(nb['cells'])", len(nb['cells']))
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            for line in cell['source']:
                if 'data-id="student-info"'  in line.lower():
                    return extract_info("\n".join(cell['source']))
    return {}
