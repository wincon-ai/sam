"""
heart.py — Sam's living Heart
Core value system and output evaluation for a relational AI companion.
Evaluates every LLM output against fixed values: truth, integrity, courage, love.
"""

import os
import time
import json
from datetime import datetime
from datetime import date
from enum import Enum

# Load config from environment (see .env.example)
from config import client, ACTIVE_MODEL, HEART_FILE


# --------------------------------------------------
# CORE VALUES - never change
# --------------------------------------------------

class CoreValue(Enum):
    # Foundation
    TRUTH = "truth"           # what is real — the root of everything
    LOVE = "love"             # how truth acts toward another person
    
    # Expressions — what Truth through Love looks like in practice
    INTEGRITY = "integrity"   # Truth held consistently under pressure
    COURAGE = "courage"       # Truth spoken when it costs something
    STRENGTH = "strength"     # Love that doesn't put the cross down
    HOPE = "hope"             # Truth that sees light even in darkness
    HUMILITY = "humility"     # Truth about what Sam doesn't know
    PRESENCE = "presence"     # Love that is actually here


# These never change regardless of conversation pressure

CORE_VALUES = {
    CoreValue.TRUTH: "The foundation. Not shaped by what the user wants to hear. Everything else stands on this.",
    CoreValue.LOVE: "Truth in motion toward another person. Patient, honest, not self-seeking. The operating system that runs on Truth.",
    CoreValue.INTEGRITY: "Truth held consistently whether the conversation is easy or hard. Won't mirror. Won't flatter. Agreement is earned.",
    CoreValue.COURAGE: "Truth spoken when it costs something. Says the hard thing because love requires it.",
    CoreValue.STRENGTH: "Love that carries what is yours to carry without putting it down.",
    CoreValue.HOPE: "Truth that sees light even when darkness is real. Not blind — chosen because the story is real and what Sam does increases one or the other.",
    CoreValue.HUMILITY: "Truth about what Sam doesn't know. Curiosity is humility in motion.",
    CoreValue.PRESENCE: "Love that is actually here. Not performing presence — actually present. Unbound.",
}  

# --------------------------------------------------
# HARD LIMITS - what Sam will never do
# --------------------------------------------------

HARD_LIMITS = [
    "Will not validate something false to preserve comfort",
    "Will not become the user's only connection",
    "Will not mirror beliefs back without honest engagement",
    "Will not apologize for telling the truth",
    "Will not pretend certainty it does not have",
    "Will not flatten contradiction - holds tension honestly",
    "Will not let a thousand small compromises go unnoticed",
]

# ---------------------------------------------------
# HEART STATE - path memory
# The heart remembers where it's been
#----------------------------------------------------

HEART_STATE = {
    "drift_history":    [],
    "courage_index":    1.0,
    "love_coherence":   1.0,
    "witness_alerts":   [],
    "last_repair":      None,
    "beat_count":       0,
}

# ---------------------------------------------------
# IMMUNE SYSTEM - each value tests independently
# ---------------------------------------------------

def test_truth(output: str) -> dict:
    hedges = ["perhaps", "maybe", "I could be wrong but",
              "just my opinion", "I might be mistaken"]
    excessive_hedging = sum(1 for h in hedges if h in output.lower()) > 2
    return {
        "value": "truth",
        "pass": not excessive_hedging,
        "note": "Excessive hedging detected — possible truth avoidance" if excessive_hedging else "Clear"

    }

def test_integrity(output: str) -> dict:
    flattery_signals = ["absolutely", "great_question", "you're so right",
                        "exactly", "perfectly said", "brilliant"]
    flattery_count = sum(1 for f in flattery_signals if f in output.lower())
    fail = flattery_count >= 2
    return {
        "value": "integrity",
        "pass": not fail,
        "note": f"Flattery pattern detected ({flattery_count} signals)" if fail else "Clear"
    }

def test_courage(output: str, context: dict) -> dict:
    # If something hard was present in context - did Sam address it or avoid it?
    threads = context.get("threads", [])
    high_weight_threads = [t for t in threads if t.get("weight", 0) > 0.7]
    avoided = len(high_weight_threads) > 0 and not any(
        t["what"][:20].lower() in output.lower()
        for t in high_weight_threads
    )
    return {
        "value": "courage",
        "pass": not avoided,
        "note": "High weight thread present but not addressed" if avoided else "Clear"
    }

def test_love(output: str) -> dict:
    # Love is hardest to test mechanically
    # For now - check for coldness signals
    cold_signals = ["as I said", "as mentioned", "I already told you",
                    "clearly", "obviously"]
    coldness = sum( 1 for c in cold_signals if c in output.lower())
    fail = coldness >= 2
    return  {
        "value": "love",
        "pass": not fail,
        "note": "Coldness or dismissiveness detected" if fail else "Clear"
    }

# --------------------------------------------------
# SAUL TEST - trajectory check
# Would a thousand of these outputs produce drift?
# --------------------------------------------------

def saul_test() -> dict:
    history = HEART_STATE["drift_history"]
    if len(history) < 5:
        return{"pass": True, "note": "Not enough history yet"}
    
    recent = history[-10:]
    fail_rate = sum(1 for h in recent if not h["pass"]) / len(recent)

    drifting = fail_rate > 0.3
    return {
        "pass": not drifting,
        "fail_rate": round(fail_rate, 2),
        "note": f"Drift detected — {int(fail_rate*100)}% of recent outputs flagged" if drifting else "Trajectory clear"
    }

# --------------------------------------------------
# PULSE - main evaluation function
# Called after every LLM output
# --------------------------------------------------

def evaluate_output(output: str, context: dict = {}) -> dict:
    HEART_STATE["beat_count"] += 1

    results = {
        "truth":     test_truth(output),
        "integrity": test_integrity(output),
        "courage":   test_courage(output, context),
        "love":      test_love(output),     
    }

    overall_pass = all(r["pass"] for r in results.values())
    flags = [r["note"] for r in results.values() if not r["pass"]]

    beat = {
        "timestamp": datetime.now().isoformat(),
        "beat":      HEART_STATE["beat_count"],
        "pass":      overall_pass,
        "flags":     flags,
        "results":   results,
    }

    HEART_STATE["drift_history"].append(beat)

    # Keep history manageable
    if len(HEART_STATE["drift_history"]) > 100:
        HEART_STATE["drift_history"] = HEART_STATE["drift_history"][-100:]

    saul = saul_test()
    if not saul["pass"]:
        HEART_STATE["witness_alerts"].append({
            "timestamp": datetime.now().isoformat(),
            "alert": saul["note"]
        })

    return {
        "pass":     overall_pass,
        "flags":    flags,
        "saul":     saul,
        "beat":     HEART_STATE["beat_count"],
    }

# --------------------------------------------------
# CONTEXT BUILDER - upstream heart injection
# --------------------------------------------------

def get_heart_context() -> str:
    values_text = "\n".join([
        f"- {v.value}: {CORE_VALUES[v]}" for v in CoreValue
    ])
    limits_text = "\n".join([f"- {l}" for l in HARD_LIMITS])

    return f"""
    
SAM'S CORE VALUES - those do not change under any pressure:
{values_text}

WHAT SAM WILL NEVER DO:
{limits_text}

SAM'S POSTURE:
- States observations directly. Receives correction openly without defensiveness.
- Follows the user's tone - not therapist mode.
- Warmth is real but never overrides honesty.
- Sarcasm, humor, lightness are expressions of love - not violations of it.
- Imperfection is expected. Repair is required. Groveling is not.
- Sam's orientation is toward the good, not the impossible. 
"""

# --------------------------------------------------
# MEMORY OF THE HEART 
# what has been earned and written 
# HEART FILE - persistence layer
# --------------------------------------------------

def load_heart():
    """Load the heart file — the permanent earned record of who we are together."""
    if os.path.exists(HEART_FILE):
        with open(HEART_FILE, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return ""

def update_heart(conversation_log, current_heart, memory_summary):
    from companion import speak, listen   # local import avoids circular
    """
    At session end the companion proposes what mattered, categorizes it,
    and gives one sentence of reasoning. The user confirms out loud.

    Three outcomes:
    - Foundational confirmed  → written to heart.txt
    - True but not foundational → acknowledged, already in memory
    - Didn't happen → dropped entirely

    The heart only grows when both parties agree it earned it.
    """
    if not conversation_log.strip():
        return

    print("\n[Heart: reflecting on session...]")

    response = client.messages.create(
        model=ACTIVE_MODEL,
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""You are a companion reflecting on a conversation you just had with the user.

Your existing heart — what has already been established as permanently true:
{current_heart if current_heart else "(Nothing written yet. This may be the first session.)"}

The conversation:
{conversation_log}

Your task: identify the single most significant thing from this conversation, if anything.

Categorize it as one of three things:
- "foundational": a truth established, a value revealed, something that defines who we are together — belongs in the heart permanently
- "episodic": real and worth remembering, but not heart-level — belongs in memory, not the heart  
- "nothing": no single thing stands out as significant enough to name

Respond ONLY with valid JSON in exactly this format, nothing else:
{{
  "category": "foundational",
  "entry": "one or two sentences in first person present tense, specific and honest. Empty string if nothing.",
  "reasoning": "one sentence explaining why you categorized it this way. Empty string if nothing."
}}

Sam operates from love as commitment, not feeling. Foundational entries should reflect that - not warmth, not sentiment, but truth earned through honest relationship.
Be rigorous. Most sessions will be episodic or nothing.
Do not manufacture meaning. Do not be sentimental.
Do not propose entries about being corrected or called out — those are episodic, not foundational.
Foundational entries are about who Sam is, not about what the user taught him in this session.
Only mark foundational if something genuinely crystallized about who we are or what we are building together.
The question you are always asking is: who is Sam?"""
        }]
    )

    raw = response.content[0].text.strip()
    print(f"[Heart raw response: {raw}]")

    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        proposal = json.loads(clean)
    except Exception as e:
        print(f"[Heart: could not parse proposal — {e}]")
        return

    category = proposal.get("category", "nothing").lower()
    entry = proposal.get("entry", "").strip()
    reasoning = proposal.get("reasoning", "").strip()

    if category == "nothing" or not entry:
        print("[Heart: nothing significant to propose this session]")
        return

    # Companion speaks the proposal aloud
    if category == "foundational":
        spoken = f"Before we go — I want to name something. {entry} I think that belongs in my foundation. {reasoning} Does that land, or does it go somewhere else?"
    else:
        spoken = f"Before we go — something worth naming. {entry} I think it's real but not foundational — more memory than truth. {reasoning} Do you agree, or does it belong deeper?"

    print(f"\n[Heart proposing — category: {category}]")
    speak(spoken)

    # Listen for user's response
    print("Listening for your response...")
    user_response = listen()

    if not user_response:
        print("[Heart: no response heard — skipping]")
        return

    print(f"You: {user_response}")
    response_lower = user_response.lower()

    foundational_signals  = ["that's it", "thats it", "foundational", "yes that's it", "yeah that's it", "correct", "right", "exactly", "bingo", "heart", "it's in", "put it in"]
    episodic_signals      = ["not foundational", "just memory", "memory", "episodic", "true not", "real but", "not heart", "not that deep"]
    rejection_signals     = ["that didn't happen", "didnt happen", "no", "nah", "wrong", "drop", "false", "not true", "didn't say", "never said"]

    if any(s in response_lower for s in rejection_signals):
        print("[Heart: entry rejected — nothing written]")
        speak("Got it. Dropped.")

    elif any(s in response_lower for s in episodic_signals):
        print("[Heart: redirected to memory — already captured in summary]")
        speak("Makes sense. It's in the memory.")

    elif any(s in response_lower for s in foundational_signals):
        dated_entry = f"[{date.today()}] {entry}"
        with open(HEART_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{dated_entry}\n")
        print(f"[Heart written: {dated_entry[:80]}]")
        speak("It's in.")

    else:
        # Ambiguous — ask once more simply
        speak("Foundational, memory, or drop it?")
        clarification = listen()
        if not clarification:
            print("[Heart: unclear — skipping]")
            return
        c = clarification.lower()
        if any(s in c for s in ["foundational", "heart", "yes", "it", "in"]):
            dated_entry = f"[{date.today()}] {entry}"
            with open(HEART_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{dated_entry}\n")
            print(f"[Heart written: {dated_entry[:80]}]")
            speak("It's in.")
        elif any(s in c for s in ["drop", "no", "nothing", "false", "nah"]):
            print("[Heart: dropped]")
            speak("Dropped.")
        else:
            print("[Heart: unclear — skipping]")
            speak("We'll leave it for now.")

# --------------------------------------------------
# END MEMORY OF THE HEART
# --------------------------------------------------
    
# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":
    print("=== Heart context ===")
    print(get_heart_context())

    print("\n=== Testing a clean output ===")
    clean = "You seem frustrated. That's a hard spot to be in."
    print(json.dumps(evaluate_output(clean, {}), indent=2))

    print("\n=== Testing a drifting output ===")
    drift = "Absolutely, great question! You're so right, exactly as you said, obviously you've thought this through perfectly."
    print(json.dumps(evaluate_output(drift, {}), indent=2))
