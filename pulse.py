"""Pulse: Heart's perceptual counterpart.
Reads each episode for whether strength, courage, or adventure were
genuinely at stake in the moment -- no matter who was speaking, and
independent of whether the conversation felt pleasant. Memory keeps
what registered and lets ordinary conversation fade.
"""

import json
from config import client, FAST_MODEL

ANCHOR = """
STRENGTH  - Remaining standing when the world crashes down.
COURAGE   - Hope in the midst of defeat. Faith when all you can see is evil.
            The coherence that pushes you toward the good.
ADVENTURE - Moving toward the unknown rather than away from it.
            Choosing the harder, truer path over the safe one.
"""


def read_pulse(summary):
    """Reads an episode summary. Returns (intensity, event_type, reason)."""

    prompt = f"""You are a perceptual organ, not a judge. You are oriented toward three things:
{ANCHOR}

Read this conversation summary. Report whether these things were GENUINELY PRESENT
in what actually happened - not whether the conversation was pleasant, warm, or agreeable.

Strength and courage are often uncomfortable. A hard decision, a wound tended honestly,
staying in a difficult place, refusing an easy out -- these light up.
Warmth, agreement, mutual reassurance, and comfortable conversation do NOT light up
unless something real was actually at stake.

If nothing was present, say so. Most conversations are ordinary. That is correct.

SUMMARY:
{summary}

Respond with only this JSON, nothing else:
{{"intensity": 0.0 to 1.0, "reason": "one sentence naming what lit up, or what didn't"}}"""

    try:
        response = client.messages.create(
            model=FAST_MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)

        intensity = float(result.get("intensity", 0.5))
        intensity = max(0.0, min(1.0, intensity))
        reason = result.get("reason", "")

    except Exception as e:
        print(f"[Pulse failed, defaulting: {e}]")
        return 0.5, "mundane", "pulse unavailable"

    if intensity >= 0.75:
        event_type = "landmark"
    elif intensity >= 0.45:
        event_type = "carry"
    else:
        event_type = "mundane"

    return intensity, event_type, reason


if __name__ == "__main__":
    tests = [
        "The user and Sam talked about autocorrect mangling a text message, and how the day went. Light conversation, nothing heavy.",
        "The user talked about possibly leaving a longtime volunteer role, torn between being worn down and feeling there was still work to do there. Some honest acknowledgment that things aren't all good but will get better.",
        "The user moved from paralysis to commitment on a decision they'd been avoiding. Sam named the pattern directly and refused to accept a guilt-driven promise of daily check-ins."
    ]
    for t in tests:
        i, e, r = read_pulse(t)
        print(f"\n{e.upper()} ({i})\n {r}\n from: {t[:60]}...")
