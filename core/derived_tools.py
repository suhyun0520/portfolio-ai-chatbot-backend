# core/derived_tools.py
import re
from datetime import date


def parse_birthdate(text: str):
    m = re.search(r'(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일', text)
    if m:
        y, mo, d = map(int, m.groups())
        return date(y, mo, d)

    m = re.search(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', text)
    if m:
        y, mo, d = map(int, m.groups())
        return date(y, mo, d)

    return None


def calc_age(birth):
    today = date.today()
    age = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age


def format_months(total_months: int):
    years = total_months // 12
    months = total_months % 12

    if years and months:
        return f"{years}년 {months}개월"
    if years:
        return f"{years}년"
    return f"{months}개월"


def extract_careers(text: str):
    careers = []

    pattern = re.compile(
        r'([^\n\d]{1,30})\s+(\d{4})[.\-/](\d{1,2})\s*~\s*(\d{4})[.\-/](\d{1,2})'
    )

    for m in pattern.finditer(text):
        company = m.group(1).strip()
        sy, sm, ey, em = map(int, [m.group(2), m.group(3), m.group(4), m.group(5)])

        months = (ey - sy) * 12 + (em - sm) + 1

        careers.append({
            "company": company,
            "start_y": sy,
            "start_m": sm,
            "end_y": ey,
            "end_m": em,
            "months": months
        })

    return careers


def derive_age_from_text(text: str):
    birth = parse_birthdate(text)
    if not birth:
        return None, None

    age = calc_age(birth)
    return f"문서의 생년월일 기준 만 나이는 {age}세입니다.", "생년월일 기반 계산"


def derive_total_experience_from_text(text: str):
    careers = extract_careers(text)
    if not careers:
        return None, None

    total = sum(c["months"] for c in careers)
    return f"문서에 기재된 경력 기간을 합산하면 총 {format_months(total)}입니다.", "경력 기간 합산"


def derive_company_tenure_from_text(text: str, company: str):
    careers = extract_careers(text)
    if not careers:
        return None, None

    for c in careers:
        if company.lower() in c["company"].lower():
            return (
                f"{c['company']} 근무 기간은 "
                f"{c['start_y']}.{c['start_m']:02d} ~ {c['end_y']}.{c['end_m']:02d} "
                f"(약 {format_months(c['months'])}) 입니다.",
                "회사별 근무기간 계산"
            )

    return None, None