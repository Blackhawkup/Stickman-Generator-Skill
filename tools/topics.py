#!/usr/bin/env python3
"""Topic registry & deduplication manager for the Timed Slideshow Explainer system.

Prevents repeats by verifying all requested topics against completed_topics.json.
Picks the next available topic idea from example_topics.json when none is specified.

Usage:
  python tools/topics.py next
  python tools/topics.py list
  python tools/topics.py completed
  python tools/topics.py add "Topic Name" [--category "Category"] [--scenario "Hook scenario"] [--concept "Core concept"]
"""
import argparse, datetime, json, re, sys
from pathlib import Path

TOPICS_DIR = Path(__file__).resolve().parent.parent / 'topics'
COMPLETED_FILE = TOPICS_DIR / 'completed_topics.json'
EXAMPLES_FILE = TOPICS_DIR / 'example_topics.json'


def norm_str(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def slugify(s):
    s = re.sub(r'[^\w\s-]', '', (s or '').lower()).strip()
    return re.sub(r'[-\s]+', '-', s)


def load_json_file(path, default=None):
    if not path.exists():
        return default if default is not None else []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default if default is not None else []


def save_json_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def get_completed_topics():
    return load_json_file(COMPLETED_FILE, [])


def get_example_topics():
    return load_json_file(EXAMPLES_FILE, [])


def is_topic_completed(name_or_slug):
    n = norm_str(name_or_slug)
    for item in get_completed_topics():
        if norm_str(item.get('topic', '')) == n or norm_str(item.get('slug', '')) == n:
            return True
    return False


def get_next_topic():
    completed = {norm_str(x.get('topic', '')) for x in get_completed_topics()}
    completed.update(norm_str(x.get('slug', '')) for x in get_completed_topics())
    
    for item in get_example_topics():
        t_norm = norm_str(item.get('topic', ''))
        s_norm = norm_str(item.get('slug', ''))
        if t_norm not in completed and s_norm not in completed:
            return item
    return None


def mark_completed(topic_name, slug=None, title=None, duration=0.0, slides=0, video_path=None, music=None, thumbnail=None):
    slug = slug or slugify(topic_name)
    title = title or topic_name.upper()
    completed = get_completed_topics()
    
    # Check if already present and update, else append
    entry = None
    for item in completed:
        if norm_str(item.get('topic', '')) == norm_str(topic_name) or norm_str(item.get('slug', '')) == norm_str(slug):
            entry = item
            break
            
    if not entry:
        entry = {'topic': topic_name, 'slug': slug}
        completed.append(entry)
        
    entry['title'] = title
    entry['completed_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if duration:
        entry['duration_seconds'] = round(duration, 2)
    if slides:
        entry['slides_count'] = slides
    if video_path:
        entry['video_path'] = str(video_path).replace('\\', '/')
    if music:
        entry['music'] = music
    if thumbnail:
        entry['thumbnail'] = str(thumbnail).replace('\\', '/')
    entry['status'] = 'completed'
    
    save_json_file(COMPLETED_FILE, completed)
    print(f"[Topic Registry] Marked '{topic_name}' as completed (music: {music or 'default'}) in {COMPLETED_FILE.name}")


def add_topic_idea(topic_name, category="General Psychology", hook_scenario="", core_concept="", researcher=""):
    examples = get_example_topics()
    slug = slugify(topic_name)
    
    # Check if already in example list
    for ex in examples:
        if norm_str(ex.get('topic', '')) == norm_str(topic_name):
            print(f"[Topic Registry] '{topic_name}' is already in example topics.")
            return ex
            
    new_entry = {
        'topic': topic_name,
        'slug': slug,
        'category': category,
        'hook_scenario': hook_scenario,
        'core_concept': core_concept,
        'researcher': researcher
    }
    examples.append(new_entry)
    save_json_file(EXAMPLES_FILE, examples)
    print(f"[Topic Registry] Added '{topic_name}' to {EXAMPLES_FILE.name}")
    return new_entry


def main():
    parser = argparse.ArgumentParser(description="Manage explainer topics and deduplication ledger")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("next", help="Get the next unproduced candidate topic")
    subparsers.add_parser("list", help="List all candidate topics that have not been produced")
    subparsers.add_parser("completed", help="List all produced topics")

    add_parser = subparsers.add_parser("add", help="Add a new topic idea to the queue")
    add_parser.add_argument("topic", help="Topic name")
    add_parser.add_argument("--category", default="General Psychology")
    add_parser.add_argument("--scenario", default="")
    add_parser.add_argument("--concept", default="")
    add_parser.add_argument("--researcher", default="")

    args = parser.parse_args()

    if args.command == "next":
        nxt = get_next_topic()
        if nxt:
            print(json.dumps(nxt, indent=2))
        else:
            print(json.dumps({"error": "No more unproduced topics in example_topics.json. Please add more!"}))

    elif args.command == "list":
        completed_names = {norm_str(x.get('topic', '')) for x in get_completed_topics()}
        pending = [x for x in get_example_topics() if norm_str(x.get('topic', '')) not in completed_names]
        print(f"\n--- Pending Candidate Topics ({len(pending)} available) ---")
        for i, p in enumerate(pending, 1):
            print(f"{i:02d}. {p['topic']} ({p.get('category', 'General')})")
            if p.get('core_concept'):
                print(f"    Concept: {p['core_concept']}")

    elif args.command == "completed":
        comp = get_completed_topics()
        print(f"\n--- Completed Topics Ledger ({len(comp)} videos) ---")
        for i, c in enumerate(comp, 1):
            dur = f"({c.get('duration_seconds', 0):.1f}s, {c.get('slides_count', 0)} slides)" if 'duration_seconds' in c else ""
            print(f"{i:02d}. {c['topic']} {dur} -> {c.get('video_path', 'done')}")

    elif args.command == "add":
        add_topic_idea(args.topic, args.category, args.scenario, args.concept, args.researcher)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
