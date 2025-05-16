import re

def extract_section(text: str | None, start: str, end: str) -> str:
    pattern = re.compile(f"{re.escape(start)}(.*?){re.escape(end)}", re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else f"Раздел между '{start}' и '{end}' не найден"
