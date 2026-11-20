# Explainer Topics Management & Deduplication

This folder manages topic selection and prevents topic repeats across all generated explainer videos.

---

## 1. Candidate Topics Queue: `example_topics.json`

This file is where candidate topics live. You can edit this file directly to add your own topic ideas, angles, or custom scenarios.

### Format to Add a Topic:
```json
{
  "topic": "The Pratfall Effect",
  "slug": "pratfall-effect",
  "category": "Social Psychology",
  "hook_scenario": "A brilliant, flawless presenter spills coffee all over his shirt, and suddenly everyone in the room likes him twice as much.",
  "core_concept": "Competent people become significantly more likable and relatable when they make a small, clumsy mistake.",
  "researcher": "Elliot Aronson (1966)"
}
```

You can also add a topic via CLI:
```bash
python tools/topics.py add "The Bystander Effect" --category "Social Psychology" --scenario "A person drops groceries on a crowded street and nobody stops." --concept "Individuals are less likely to offer help when other people are present."
```

---

## 2. Completed Topics Ledger: `completed_topics.json`

Every time a video is rendered through `cli.py auto`, it is automatically recorded in `completed_topics.json` with its metadata:
- Topic name and slug
- Timestamp of generation
- Duration in seconds
- Slide count
- Rendered MP4 path and interactive player link

**Deduplication Guarantee**: The system checks this file before producing any video. If a topic has already been completed, it is skipped or flagged so no topic is ever repeated.

---

## 3. CLI Commands

```bash
# View all pending topics in the queue:
python tools/cli.py topics

# View the next available unproduced topic:
python tools/cli.py topics next

# View all completed videos:
python tools/cli.py topics completed
```

---

## 4. How the Autonomous Agent Uses This

When you tell the agent:
> *"Generate a clip"* or *"Make a 1-minute short"*

The agent automatically:
1. Calls `cli.py topics next` to select the next unproduced topic from `example_topics.json` (or uses the topic you specifically named).
2. Verifies that it has not been produced in `completed_topics.json`.
3. Writes the 1-minute script (`script.md`) following our locked 10-step sequence.
4. Breaks down the script into 25–30 visual slides (`slides.json`) adhering to the strict **2–4 second pacing rule**.
5. Runs `python tools/cli.py auto <slug>`, which generates voiceover, word clocks, Flow images, ducked music, validates pacing, and renders the 60fps MP4.
6. Automatically records the new video in `completed_topics.json`.
7. Delivers the video link to you.
