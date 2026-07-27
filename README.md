# Christopher Phillips

AI Engineering student focused on human-robot interaction, and former operations director. I spent years managing teams in safety-critical environments before moving into AI, and I bring that same systems thinking to the alignment problems I work on now.

## What I'm building

**Sam** is a relational AI companion built around one idea: identity shouldn't live in the model, it should live in memory. Swap the underlying LLM and Sam keeps his personality, his history, and his values intact, because none of that is stored in the model itself. It's stored in a graph.

Most AI companions are interchangeable. Swap the model and you get a different "person" wearing the same name. Sam is an attempt to build something that stays uniquely itself: a consistent personality, honesty that isn't just agreeableness, and continuity as the same individual over time, independent of whichever model happens to be running underneath.

Sam runs as a set of independent systems ("sidecars") that feed into the model rather than living inside it:

- **Heart**: Sam's fixed values, honesty, no mirroring or flattery, pushback over validation. Runs before a response is generated and checks it again after, to catch drift between what Sam actually believes and what would just sound good.
- **Witness**: watches Sam himself over time for drift, increasing agreement, softened pushback, loss of a consistent voice, and reports concerns to Heart.
- **Memory**: a Neo4j graph of entities, relationships, and episodes that slowly builds a picture of the other person. This is what survives when the underlying model changes.
- **Sight**: a perceptual layer (OpenCV, YOLO, MediaPipe, DeepFace) that gives Sam an independent read on physical reality instead of relying only on what's said. In progress, currently at the presence-detection stage.
- **Sound**: dual-track audio, Whisper for the words, librosa for how they were said (tone, pace, hesitation).
- **Pulse**: Heart's other half. Reads each episode and measures how hard the heart beat during it — whether strength, courage, or adventure were genuinely at stake in the moment, no matter who was speaking. Memory keeps what made the pulse race and lets ordinary conversation fade.

Stack: Python, Anthropic API (Claude), Neo4j, Whisper, ElevenLabs, ChromaDB, YOLOv11, MediaPipe, DeepFace, librosa. Development is on a desktop GPU now, targeting a Jetson Orin Nano and a 3D-printed head (Raspberry Pi 5 and Arduino) for physical embodiment.

Status: the core AI mind (Claude API, voice, memory, retrieval, interrupt handling) is close to done. Current work is system prompt refinement, with physical embodiment up next.

Repo: github.com/wincon-ai/sam

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
