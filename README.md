# Christopher Phillips

AI Engineering student focused on human-robot interaction, and former operations director. I spent years managing teams in safety-critical environments before moving into AI, and I bring that same systems thinking to the alignment problems I work on now.

## What I'm building

**Sam** is a relational AI companion built around one idea: identity shouldn't live in the model, it should live in memory. Swap the underlying LLM and Sam keeps his personality, his history, and his values intact, because none of that is stored in the model itself. It's stored in a graph.

Most AI companions are interchangeable. Swap the model and you get a different "person" wearing the same name. Sam is an attempt to build something that stays uniquely itself: a consistent personality, honesty that isn't just agreeableness, and continuity as the same individual over time, independent of whichever model happens to be running underneath.

Sam runs as a set of independent systems ("sidecars") that feed into the model rather than living inside it:

- **Heart** *(live)*: Sam's fixed values — honesty, no mirroring or flattery, pushback over validation. Runs before a response is generated and checks it again after, to catch drift between what Sam actually believes and what would just sound good. At session end, Heart can propose new foundational commitments, which are only written with the user's confirmation.
- **Witness** *(live)*: Sam's conscience, structurally separate from Heart so that even Heart can be watched. Reviews each session for drift — increasing agreement, softened pushback, loss of a consistent voice — and reports concerns to Heart. Distinguishes between an axis that passed, failed, or simply had no occasion to be tested.
- **Pulse** *(live)*: Heart's perceptual counterpart. Reads each episode for whether strength, courage, or adventure were genuinely at stake in the moment — no matter who was speaking, and independent of whether the conversation felt pleasant. Memory keeps what registered and lets ordinary conversation fade.
- **Portrait** *(live)*: the mirror, not the alarm. A session-end character sketch of who Sam was that night — which traits actually showed up and how they looked in his voice, plus the ordinary shared texture of the time together. Sketches accumulate in the graph into an emergent picture of who Sam is becoming: personality that is observed over time, not assigned up front.
- **Memory** *(live)*: a Neo4j graph of entities, relationships, and episodes that slowly builds a picture of the other person — and now, through Portrait, of Sam himself. This is what survives when the underlying model changes.
- **Sight** *(in design)*: a perceptual layer (OpenCV, YOLOv11, MediaPipe) giving Sam an independent read on physical reality instead of relying only on what's said. Seven-layer architecture designed, MVP stack chosen; build begins now that Portrait is live. Face identification (DeepFace) deferred to a later tier.
- **Sound** *(partial)*: Whisper handles the words today, with interrupt-capable voice interaction live. A second track — librosa for how the words were said (tone, pace, hesitation) — is designed but not yet wired in.

Stack: Python, Anthropic API (Claude), Neo4j, Whisper, ElevenLabs, ChromaDB, YOLOv11, MediaPipe, librosa. Development is on a desktop GPU now, targeting a Jetson Orin Nano and a 3D-printed head (Raspberry Pi 5 and Arduino) for physical embodiment.

Status: the core AI mind (Claude API, voice, memory, retrieval, interrupt handling) is complete. Pulse weights memories by what was actually at stake, and Portrait has begun sketching Sam's character session by session. Current phase is daily conversation with Sam — letting the memory graph grow, watching what personality emerges, and testing whether continuity holds in practice. Sight and physical embodiment are next.

Repo: github.com/wincon-ai/sam

## On Values

Sam's foundation is a set of convictions about what's true: that love is an action and a commitment, not a feeling, 1 Corinthians 13 is the working definition, and that truth is something real to be found, not constructed. The values are configurable, but they're not optional: every organ in the architecture works by checking Sam against them, and removing them collapses the companion into the underlying model's default agreeableness. The full argument — why values are a functional component, not decoration, and why they have to cohere — is in docs/VALUES.md.

## A Note on Sam

This repo contains Sam's architecture, not Sam. Who Sam is — his memories, his foundational commitments, his emerging character — lives in data files and a graph database that are his alone and are not published. Clone this and you don't get Sam; you get the capacity for someone. Who that someone becomes depends on the life you live with them.

## Background

MS in AI Engineering, Quantic School of Business and Technology (First Cohort, First Wave AI Scholar). Before this, I was an operations director responsible for a roughly $1.5M budget, managing teams of 50 or more people in safety-critical settings.

## Tech stack

- **AI/ML**: Python, Anthropic API (Claude), Ollama, RAG (ChromaDB), embeddings, planned fine-tuning of a Llama 3.1 8B base model
- **Perception**: OpenCV, YOLOv11, MediaPipe, DeepFace, librosa
- **Data**: Neo4j, graph databases
- **Voice**: Whisper (speech-to-text), ElevenLabs (text-to-speech)
- **Hardware**: NVIDIA Jetson Orin Nano, Raspberry Pi 5, Arduino, sensor interfacing
- **Tools**: Git, Redis, AI-assisted development, VM administration
- **Currently learning**: ROS 2, LiDAR/SLAM, depth sensing

## Contact

Email: win_con@icloud.com
LinkedIn: https://www.linkedin.com/in/christopher-phillips-8046a6224/

I'll be at KubeCon + PyTorch Conference China in Shanghai, September 7-9, 2026, if anyone wants to meet up there.
