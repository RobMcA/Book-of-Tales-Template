#!/usr/bin/env python3
"""Merge a JSON array of entries into book.json entries array."""
import json, sys

book_path = sys.argv[1]
entries_path = sys.argv[2]

with open(book_path, 'r') as f:
    book = json.load(f)

with open(entries_path, 'r') as f:
    new_entries = json.load(f)

existing_ids = {e['id'] for e in book['entries']}
added = 0
for e in new_entries:
    if e['id'] in existing_ids:
        print(f"  WARNING: duplicate id {e['id']}, skipping")
    else:
        book['entries'].append(e)
        existing_ids.add(e['id'])
        added += 1

with open(book_path, 'w') as f:
    json.dump(book, f, indent=2, ensure_ascii=False)

print(f"Added {added} entries. Total: {len(book['entries'])}")
