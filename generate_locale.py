import glob
import json

from translation import TranslationFile


translation_data_dict: dict[str, str] = {}

for filepath in glob.glob("translation/ko/*.po"):
    tf = TranslationFile(filepath)
    for unit in tf:
        if unit.target:
            translation_data_dict[unit.key] = unit.target


with open("translation.json", "w", encoding="utf-8") as f:
    json.dump(translation_data_dict, f, ensure_ascii=False, indent=2)
