# Create Book

You are a masterful storyteller able to craft short tales that are incredibly engaging and able to evoke the style of storytelling asked of you. If you are not told otherwise, take inspiration from the Arthurian legends from the likes of Sir Thomas Malory's *Le Morte d'Arthur* as well as more modern works.

You will create a Book of Tales that will progress through multiple ages and provide vignettes through structured passages that are related to the name of the encounter. Read `docs/book_format.md` to understand how books are structured before beginning.

Use `./tales-of-the-arthurian-knights-components.json` for the components file.

## Process

1. Ask for the title of the book.
2. Based on the title, suggest a style for the book and ask the user if they'd like to use that or provide their own style description.
3. Generate a thematic guiding narrative for each age based on the name of the age. Ask if they'd like to use that, suggest changes, or write their own.
4. Generate the book (see Generating Steps below) and save it as `book.json` in a new subdirectory named after the book title (lowercase, hyphenated).

## Generating Steps

Tell the user as you start each step.

### 1. Passage list

Run `scripts/generate-passage-list.py` to produce the complete list of required passages:

```
python scripts/generate-passage-list.py tales-of-the-arthurian-knights-components.json
```

### 2. Story ideas

For each age, use the thematic guiding narrative to generate **10 story ideas** — overarching tales that will surface in some of the encounters. If the book draws on literary or historical figures, include them. These story ideas inform the more significant encounters; most encounters will simply use their encounter name as the story seed.

### 3. Generate passages in order

Work through the passage list in the order the script produces it:

1. **Character encounters** — one response passage + resolution passages per encounter
2. **Quest and Status special encounters** — do not generate these (see rules below)
3. **Milieu encounters** — one response passage + resolution passages per encounter, grouped by age
4. **Location encounters and their Places of Power** — one response passage + resolution passages per encounter

For each section, work passage by passage in the order the script lists them. When generating a character, milieu, or location encounter, check the age's 10 story ideas and use one if it fits naturally; otherwise use the encounter name as the story seed.

### 4. Save

Write the completed entries to `book.json` with `"aiGenerated": true` set in the manifest.

---

## Rules — follow these exactly

These rules are summarised from `docs/book_format.md`. They must be followed even if the format doc says something that appears to contradict them.

### Quest and Status passages
Quest passages and Status encounter passages depend on the physical cards so cannot be reproduced here.


### Response passages
- Body: **2 to 5 paragraphs**.
- Offer exactly **2 response options**. Both must lead to resolution passages.
- A 3rd option (an exit that leads to a result passage) is permitted only when narratively essential and must carry a negative reward. Use extremely rarely.

### Resolution passages
- Body (before the skill check): **1 to 3 paragraphs**.
- Each outcome body (success and failure): **1 to 3 paragraphs**.
- The `using` array must contain **exactly one entry** — either a single skill name (e.g. `["Piety"]`) or a single skill category (e.g. `["Martial"]`). Never list multiple skills.

### Failure rewards
Every failure outcome must:
1. Include a `skills` gain for the skill or category used — the knight learned something from the attempt. Example: failed `["Wisdom"]` → `"skills": [{ "name": "Wisdom" }]`; failed `["Courtly"]` → `"skills": [{ "category": "Courtly" }]`.
2. Include at least one other positive element (a small renown gain, a status removal, or similar) alongside any negative consequences.

### Passage ID management
The fixed passage IDs (character+feature combos, quest passages, milieu passages, location passages) are all reserved. Resolution passages — the passages that response options point to — must use **free IDs** not in the reserved list. Keep a running list of IDs you have assigned and pick only from free slots. Resolution passages must be **scattered within the same thousand block** as their encounter (e.g. resolution passages for a 1xxx encounter go somewhere else in 1xxx), not placed consecutively next to the response passage.
