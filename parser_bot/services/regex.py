import re
from http.client import HTTPException


def extract_section(text: str | None) -> str | list:
    start = "Навыки"
    end = "Резюме"
    pattern = re.compile(f"{re.escape(start)}(.*?){re.escape(end)}", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError(f"Раздел между '{start}' и '{end}' не найден")

def individual_word(text: str | None) -> list:
    pattern = re.findall(r'\b[a-zA-Z]+\b', text)
    return pattern
