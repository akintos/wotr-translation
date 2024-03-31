import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import TypedDict

from translation import TranslationFile


class TanslationStorage(TypedDict):
    timestamp: str
    translated: int
    total: int
    data: dict[str, str]


def main():
    parser = argparse.ArgumentParser(description="Generate locale files")
    
    parser.add_argument("input_directory", type=str, help="Input directory path")
    parser.add_argument("output_file", type=str, help="Output file path")
    
    args = parser.parse_args()

    input_dir = Path(args.input_directory)
    output_file = Path(args.output_file)

    if not input_dir.exists():
        raise FileNotFoundError(f"{input_dir} does not exist")

    translated = 0
    total = 0
    data: dict[str, str] = {}

    for filepath in input_dir.glob("*.po"):
        tf = TranslationFile(filepath)
        total += len(tf)
        for unit in tf:
            if unit.target:
                data[unit.key] = unit.target
                translated += 1

    print(f"Translated {translated}/{total} ({translated/total:.2%})")

    storage: TanslationStorage = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "translated": translated,
        "total": total,
        "data": data,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)

    if github_output_file := os.getenv('GITHUB_OUTPUT'):
        with open(github_output_file, "w", encoding="utf-8") as f:
            f.write(f"stats={translated}/{total} ({translated/total:.2%})")


if __name__ == "__main__":
    main()
