---
name: video-use-install
description: Install video-use into this project (Claude Code) and wire up ffmpeg + local, free speech-to-text so the user can start editing immediately. No paid APIs, no accounts required.
---

# video-use install (project-local, free-only)

Use this file only for first-time install or reconnect. For daily editing, read `SKILL.md`. Always read `helpers/` — that's where the scripts live.

## What you're doing

This is a conversation-driven video editor, installed as a project skill at `.claude/skills/video-use/` in this repo (not a global `~/.claude/skills/` symlink). After install, the user drops raw footage into any folder, runs `claude` there, and says "edit these into a video." You do the rest by reading `SKILL.md`.

Every piece of this stack is free and open-source — no ElevenLabs, no paid transcription API, no account signup required for the core path:

1. **Transcription** — `faster-whisper` (CTranslate2-optimized OpenAI Whisper), runs 100% locally on CPU. No API key.
2. **Editing / rendering** — `ffmpeg` + Python (`librosa`, `matplotlib`, `pillow`, `numpy`). All open-source.
3. **Animations (optional, on-demand)** — HyperFrames, Remotion, Manim: all free/open-source, installed lazily per slot only if a session needs one.
4. **Diarization (optional)** — `pyannote.audio`, also open-source, but its pretrained models are gated behind a free Hugging Face account + accepting model terms once. Skip entirely if the user doesn't need speaker separation.

## Steps

### 1. The skill is already in place

It lives at `.claude/skills/video-use/` in this repo — `SKILL.md` and `helpers/` ship together as siblings, which is all Claude Code needs to discover and use it project-wide. No symlinking into a global directory required.

### 2. Install Python deps

```bash
cd .claude/skills/video-use
pip install -e .
# or, if uv is available:
# uv sync
```

`pyproject.toml` lists `faster-whisper`, `librosa`, `matplotlib`, `pillow`, `numpy`. No console scripts — helpers are invoked directly as `python helpers/<name>.py`.

### 3. Install ffmpeg (+ optional yt-dlp)

`ffmpeg` and `ffprobe` are hard requirements. `yt-dlp` (also free/open-source) is only needed if the user wants to pull sources from URLs.

```bash
# Debian / Ubuntu
sudo apt-get update && sudo apt-get install -y ffmpeg
pip install yt-dlp   # optional

# macOS
brew install ffmpeg
brew install yt-dlp  # optional
```

If a package manager needs a sudo prompt, tell the user the exact command and wait — do not invent a password.

### 4. First transcription downloads the model once

The first call to `transcribe.py` or `transcribe_batch.py` pulls the chosen Whisper model (default `small`, override with `--model`) from Hugging Face's public model hub and caches it under `~/.cache/huggingface`. This is a one-time download per model size, fully anonymous — no token, no login. After that, transcription is offline.

Model size vs. speed/accuracy tradeoff (CPU, `compute_type=int8`):
- `tiny` / `base` — fastest, roughest. Good for quick previews.
- `small` (default) — solid balance for most footage.
- `medium` / `large-v3` — best accuracy, noticeably slower on CPU. Use for noisy or accented audio when quality matters more than turnaround.

### 5. Optional: diarization

Skip unless the user specifically needs speaker separation (interviews, multi-person footage). It's still free, but requires one manual step:

1. Create a free Hugging Face account and token at https://huggingface.co/settings/tokens.
2. Accept the model terms once at https://huggingface.co/pyannote/speaker-diarization-3.1.
3. `pip install -e '.[diarize]'` (or `pip install pyannote.audio`).
4. Export `HF_TOKEN=<token>` in the environment before running `transcribe.py --diarize`.

If any of this is missing, `transcribe.py --diarize` degrades gracefully — it still transcribes, just without speaker tags — rather than failing.

### 6. Verify end-to-end

Run one real thing against one real file rather than declaring success on file-existence checks alone:

```bash
python .claude/skills/video-use/helpers/timeline_view.py --help >/dev/null && echo "helpers OK"
ffprobe -version | head -1
python .claude/skills/video-use/helpers/transcribe.py <one_real_clip> --model tiny
```

### 7. Hand off

Tell the user, in one short message:

- The skill is installed project-locally at `.claude/skills/video-use/` — it only applies inside this repo/folder.
- Transcription is fully local and free (`faster-whisper`) — first run downloads the model once, then works offline.
- All outputs land in `<videos_dir>/edit/` next to their source footage.
- A good first message is: *"edit these into a promo video"* or *"inventory these takes and propose a strategy."*

## Keeping the skill current

- Re-run `pip install -e .` after pulling upstream changes if `pyproject.toml` deps changed.
- Node.js/npm are only needed for HyperFrames or Remotion slots (HyperFrames needs Node.js 22+). Neither is installed at setup time — pick the animation engine per slot in `SKILL.md`.

## Cold-start reminders

- Never assume a paid API is available or required — this install is free-only by design. If asked to reach for ElevenLabs or another paid STT service, decline and use `faster-whisper` instead.
- `ffmpeg` from any modern (≥ 4.x) build is enough.
- `yt-dlp` is optional. Install lazily the first time a user asks to pull from a URL.
- HyperFrames, Remotion, and Manim are optional animation engines — don't install one globally during setup, pick per animation slot in `SKILL.md`.
- If the user is on Linux without a package manager Claude recognizes, print the manual `ffmpeg` install URL and wait rather than guessing.
