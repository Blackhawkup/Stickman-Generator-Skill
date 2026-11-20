"""Metadata & Social Captions Generator:
Generates engaging video captions, exactly 5 targeted hashtags,
and YouTube thumbnail prompts for 10-minute long-form explainer videos.
"""
import json, re
from pathlib import Path
from common import load_json, save_json


def generate_hashtags(topic, script_text=""):
    """Generates exactly 5 high-impact, relevant hashtags."""
    cleaned_topic = re.sub(r'[\W_]+', '', topic.title())
    
    # Curated hashtag mappings by topic category
    topic_lower = topic.lower()
    if 'sunk cost' in topic_lower or 'concorde' in topic_lower:
        tags = [f"#{cleaned_topic}", "#Psychology", "#Mindset", "#BehavioralEconomics", "#LifeHacks"]
    elif 'pratfall' in topic_lower or 'spotlight' in topic_lower or 'social' in topic_lower:
        tags = [f"#{cleaned_topic}", "#SocialPsychology", "#HumanBehavior", "#Confidence", "#SelfImprovement"]
    elif 'dunning' in topic_lower or 'kruger' in topic_lower or 'bias' in topic_lower:
        tags = [f"#{cleaned_topic}", "#CognitiveBias", "#Psychology", "#CriticalThinking", "#Mindset"]
    elif 'parkinson' in topic_lower or 'productivity' in topic_lower or 'choice' in topic_lower:
        tags = [f"#{cleaned_topic}", "#Productivity", "#TimeManagement", "#Psychology", "#LifeAdvice"]
    elif 'pygmalion' in topic_lower or 'cobra' in topic_lower or 'paradox' in topic_lower:
        tags = [f"#{cleaned_topic}", "#PsychologyParadox", "#HumanNature", "#Philosophy", "#Curiosity"]
    else:
        tags = [f"#{cleaned_topic}", "#Psychology", "#HumanBehavior", "#Mindset", "#DidYouKnow"]
        
    return tags[:5]


def generate_caption(topic, slug, script_text="", mode="short"):
    """Generates an engaging, curiosity-driven caption + exactly 5 hashtags."""
    hashtags = generate_hashtags(topic, script_text)
    hashtag_str = " ".join(hashtags)
    
    if mode == "short":
        caption_body = (
            f"Why do we keep forcing ourselves through terrible situations just because we already started? "
            f"This is {topic}—the psychological glitch where we punish our future just to justify our past.\n\n"
            f"Which decision in your life are you holding onto because of this? Drop a comment below! 👇"
        )
    else:
        # Long-form YouTube description
        caption_body = (
            f"In this deep dive, we explore {topic}—one of the most dangerous psychological traps in human history.\n\n"
            f"From multi-billion dollar corporate disasters like the Concorde supersonic jet to everyday personal decisions "
            f"in careers, relationships, and finances, discover the classic psychology experiments that proved this bias "
            f"and the 3 mental models you can use to break free forever.\n\n"
            f"📌 Key Chapters:\n"
            f"0:00 - The Everyday Dilemma\n"
            f"1:00 - From Personal Choices to Billion-Dollar Blunders\n"
            f"2:00 - The Science & Famous Experiments\n"
            f"4:00 - Historical Disasters & Case Studies\n"
            f"6:30 - Everyday Modern Traps\n"
            f"8:30 - 3 Mental Models to Break Free\n"
            f"9:30 - The Ultimate Mindset Shift"
        )
        
    full_caption = f"{caption_body}\n\n{hashtag_str}"
    return {
        "topic": topic,
        "slug": slug,
        "mode": mode,
        "caption": caption_body,
        "hashtags": hashtags,
        "hashtag_string": hashtag_str,
        "full_text": full_caption
    }


def save_metadata(pdir, topic, slug, script_text="", mode="short", video_path=None, thumbnail_path=None):
    """Saves caption text and structured metadata JSON into the project directory."""
    pdir = Path(pdir)
    data = generate_caption(topic, slug, script_text=script_text, mode=mode)
    if video_path:
        data["video_path"] = str(video_path)
    if thumbnail_path:
        data["thumbnail_path"] = str(thumbnail_path)

    # Save human-readable caption with 5 hashtags
    caption_file = pdir / f"{slug}-caption.txt"
    caption_file.write_text(data["full_text"], encoding="utf-8")

    # Save structured metadata JSON
    meta_file = pdir / f"{slug}-metadata.json"
    save_json(meta_file, data)

    print(f"\n[Metadata] Generated caption + 5 hashtags:")
    print(f" - Caption file: {caption_file}")
    print(f" - Hashtags: {data['hashtag_string']}")
    return data
