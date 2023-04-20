import re

def change_timestamp(text: str) -> str:
    pattern = r'time\[stamp\]\[(\d+)\] with\[out\] time zone([,\n ])'
    replacement = r'datetime\2'
    return re.sub(pattern, replacement, text)
