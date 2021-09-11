import glob
import os

from pf2bp import TranslationFile, TranslationEntry

prev_translations: dict[str, TranslationEntry] = {}

for filepath in glob.glob("km/*.po"):
    tf = TranslationFile(filepath)
    for unit in tf:
        prev_translations[unit.key] = unit

matching = 0
mismatch = 0

for filename in os.listdir("templates"):
    filepath = os.path.join("templates", filename)
    tf = TranslationFile(filepath)
    for unit in tf:
        prev_tr = prev_translations.get(unit.key, None)
        if not prev_tr: continue

        if unit.source == prev_tr.source:
            matching += 1
        else:
            mismatch += 1
            # print(unit)
            # print(prev_tr)
            # print()
            unit.prev_source = prev_tr.source
        unit.fuzzy = True
        unit.target = prev_tr.target
    
    tf.export(os.path.join("translation", "ko", filename[:-1]))

print(matching)
print(mismatch)
