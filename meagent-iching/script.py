#!/usr/bin/env python3
"""Print an I Ching hexagram and its moving line."""

import argparse
import json
from pathlib import Path


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("n0", type=int)
parser.add_argument("n1", type=int)
parser.add_argument("n2", type=int)
args = parser.parse_args()

trigram0 = args.n0 % 8 or 8
trigram1 = args.n1 % 8 or 8
moving_line = args.n2 % 6 or 6
hexagram = f"{trigram0}x{trigram1}"

with (Path(__file__).parent / "iching_hexagrams.json").open(encoding="utf-8") as file:
    hexagrams = json.load(file)

print("My base hex is:\n"+hexagrams[hexagram])
print("\nMy moving line is:\n"+hexagrams[f"{hexagram}.{moving_line}"])
print("\nExplain phrase by phrase then interpret.")
