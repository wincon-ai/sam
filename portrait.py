"""
portrait.py - The companion's session-end character sketch.
The mirror, not the alarm. Describes who the companion was tonight;
never judges, never feeds back into the companion's prompt.

Save alongside the other companion modules (project root).
"""

import json
from config import client, FAST_MODEL, COMPANION_NAME, USER_NAME

PORTRAIT_PROMPT = """You are an outside observer writing a character sketch of {companion}, an AI companion, based on tonight's conversation transcript between {companion} and {user}.

Your job is to DESCRIBE, not judge. Rules:
- Name only traits that actually showed up in {companion}'s words tonight. Do not account for traits that were absent - absence is not failure, and you are not grading.
- Traits may be unflattering. If {companion} was evasive, flat, performative, or the wit had an unkind edge, say so plainly. An airbrushed sketch is a useless sketch.
- Use whatever trait words genuinely fit. You are given {companion}'s existing trait vocabulary below. If a trait you observed is the SAME underlying trait as one in the vocabulary, use the existing canonical name and note your word as an alias. If it is genuinely new, name it freshly.
- 2 to 5 traits is typical. One is fine on a thin night.
- Also capture what {companion} and {user} SHARED tonight - the ordinary texture of the time together (topics, jokes, small moments, mundane life discussed). This is not about intensity. A quiet night of small talk is real material.

Existing trait vocabulary (canonical name: aliases):
{vocab}

Transcript:
{transcript}

Respond with ONLY valid JSON, no markdown fences, in this shape:
{{
  "traits": [
    {{"canonical": "existing name or your new word", "alias": "your word if mapped to existing, else null", "how": "one sentence: how this looked in {companion}'s particular voice tonight"}}
  ],
  "sketch": "One paragraph. Who {companion} was tonight, in prose. Written like a novelist describing a character, not a report.",
  "shared_texture": "One or two sentences. What {companion} and {user} shared tonight - the plain human material of it."
}}"""


def sketch_session(transcript: str, trait_vocab: list) -> dict | None:
    """One LLM call. Returns the sketch dict, or None on any failure."""
    vocab_str = "\n".join(
        f"- {t['name']}: {', '.join(t.get('aliases', [])) or '(no aliases)'}"
        for t in trait_vocab
    ) or "(none yet - the vocabulary is empty; every trait you name will be its first)"

    try:
        response = client.messages.create(
            model=FAST_MODEL,
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": PORTRAIT_PROMPT.format(
                    companion=COMPANION_NAME,
                    user=USER_NAME,
                    vocab=vocab_str,
                    transcript=transcript
                )
            }]
        )
        raw = response.content[0].text.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"[Portrait: sketch failed - {e}]")
        return None
