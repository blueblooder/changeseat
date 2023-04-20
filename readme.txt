import re

text = "some text DEFAULT nextval('sequence'::regclass)) some more text"
pattern = r"DEFAULT nextval.*?\)"
new_text = re.sub(pattern, "", text)

print(new_text)
