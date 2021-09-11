import argparse
import csv
import json


parser = argparse.ArgumentParser("locale2csv")

parser.add_argument("locale_path", help="input locale json file path")
parser.add_argument("csv_path", help="converted csv file output path")

args = parser.parse_args()

locale_path = args.locale_path
csv_path = args.csv_path

with open(locale_path, "r", encoding="utf-8") as f:
    locale = json.load(f)

with open(csv_path, "w", encoding="utf-8", newline="") as of:
    w = csv.writer(of, quoting=csv.QUOTE_ALL)
    w.writerow(["key", "src", "dst"])
    w.writerows(kvpair for kvpair in locale["strings"].items() if kvpair[1])

print(f"saved csv file to {csv_path}")
