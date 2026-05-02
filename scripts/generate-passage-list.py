#!/usr/bin/env python3
"""
Reads a components.json and prints every required passage number + description.
Usage: python generate-passage-list.py <components.json> [--json]

Output order:
  1. Character encounters (character × feature)
  2. Quest and Status special encounters
  3. Milieu encounters, grouped by age (with age start at the top of each group)
  4. Location encounters and their Places of Power
  5. Epilogue
"""

import json
import sys


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python generate-passage-list.py <components.json> [--json]", file=sys.stderr)
        sys.exit(1)

    output_json = "--json" in args
    file_path = next(a for a in args if not a.startswith("--"))

    with open(file_path) as f:
        c = json.load(f)

    sections = []  # list of (section_label, list of {passage, description})

    def section(label):
        entries = []
        sections.append((label, entries))
        return entries

    def add(entries, passage, description):
        entries.append({"passage": str(passage), "description": description})

    def sort_entries(entries):
        def key(p):
            try:
                return (0, int(p["passage"]), "")
            except ValueError:
                return (1, 0, p["passage"])
        entries.sort(key=key)

    # 1. Character encounters (character × feature)
    char_entries = section("Character encounters")
    for character in c.get("characters", []):
        for feature in c.get("features", []):
            add(char_entries, character["base"] + feature["offset"], f"{feature['name']} {character['name']}")
    sort_entries(char_entries)

    # 2. Quest and Status special encounters
    special_entries = section("Quest and Status special encounters")
    for quest in c.get("quests", []):
        add(special_entries, quest["passage"], f"Quest — {quest['name']}")
    for status in c.get("statuses", []):
        for encounter in status.get("encounters", []):
            add(special_entries, encounter["passage"], f"Status — {status['name']}: {encounter['label']}")
    sort_entries(special_entries)

    # 3. Milieu encounters grouped by age (age start pinned first, then milieus sorted)
    for age in c.get("ages", []):
        milieu_base = age.get("milieuBase")
        age_entries = section(f"Milieu encounters — {age['name']}")
        start = []
        milieus = []
        if age.get("startPassage"):
            add(start, age["startPassage"], f"Age start — {age['name']}")
        if milieu_base is not None:
            for milieu in c.get("milieus", []):
                for terrain in c.get("terrains", []):
                    offset = milieu.get("terrainOffsets", {}).get(terrain["id"])
                    if offset is not None:
                        add(milieus, milieu_base + offset, f"Milieu — {milieu['name']} × {terrain['name']}")
        sort_entries(milieus)
        age_entries.extend(start + milieus)

    # 4. Location encounters and their Places of Power (grouped per location)
    for location in c.get("locations", []):
        loc_entries = section(f"Location — {location['name']}")
        add(loc_entries, location["passage"], f"Location — {location['name']}")
        for age in c.get("ages", []):
            visit_id = location.get("visitPassages", {}).get(age["id"])
            if visit_id:
                add(loc_entries, visit_id, f"Place of Power — {location['name']} ({age['name']})")
        sort_entries(loc_entries)

    # 5. Epilogue
    if c.get("epiloguePassage"):
        ep_entries = section("Epilogue")
        add(ep_entries, c["epiloguePassage"], "Epilogue")

    # Flatten
    all_passages = [p for _, entries in sections for p in entries]

    if output_json:
        print(json.dumps(all_passages, indent=2))
    else:
        for label, entries in sections:
            print(f"\n# {label}")
            for p in entries:
                print(f"{p['passage']}\t{p['description']}")


if __name__ == "__main__":
    main()
