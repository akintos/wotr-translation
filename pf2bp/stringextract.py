import glob
import json
import os


def extract_strings(json_input, basepath):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if isinstance(v, str) and v.startswith("LocalizedString"):
                _, key, text = v.split(":", 2)
                if key:
                    yield basepath + k, key, text
            else:
                yield from extract_strings(v, basepath + k + "/")
    elif isinstance(json_input, list):
        for i, item in enumerate(json_input):
            yield from extract_strings(item, basepath + str(i) + "/")

def get_category(path):
    for part in path.split("\\")[0].split("."):
        if part == "Kingmaker" or part == "Blueprints":
            continue
        return part

def extract_all(blueprints_dir: str):
    filelist = list(glob.glob(os.path.join(blueprints_dir, "**", "*.json"), recursive=True))

    data = []

    for filepath in filelist:
        relpath = os.path.relpath(filepath, blueprints_dir)
        
        with open(filepath, "r", encoding="utf-8") as f:
            bp = json.load(f)
        
        for path, key, text in extract_strings(bp, ""):
            data.append((get_category(relpath), relpath, path, key, text))
    
    with open("strings.csv", "w", encoding="utf-8", newline="") as f:
        import csv
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(["path", "key", "eng"])
        w.writerows(data)
