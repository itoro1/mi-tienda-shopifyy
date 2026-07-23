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
2. **Editing / rendering** — `ffmpeg` + `ffprobe` (hard requirement, verified at install time and before every render) + Python (`librosa`, `matplotlib`, `pillow`, `numpy`). All open-source.
3. **Animations** — Remotion is set up now, as a standing part of the workflow (pre-vendored, tested template at `templates/remotion-slot/`). HyperFrames and Manim stay free/open-source but lazy — installed per slot only if a session needs one.
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

Verify both binaries actually work before moving on — this is a hard blocker for every later step (extraction, cuts, grading, rendering all shell out to ffmpeg):

```bash
ffmpeg -version | head -1
ffprobe -version | head -1
```

### 3b. Remotion (standing part of the workflow, not lazy)

Unlike HyperFrames/Manim/yt-dlp, Remotion is installed as a ready-to-copy template now, at setup time, because it's the default engine for React/CSS-driven overlay animations. Verify Node.js 22+ is present, then confirm the template renders:

```bash
node --version   # expect v22+
cd .claude/skills/video-use/templates/remotion-slot
npm install
npx remotion render src/index.ts Main out/render.mp4
ffprobe -v error -show_entries stream=width,height,codec_name -show_entries format=duration out/render.mp4
rm -rf out   # test artifact, not part of the template
```

A successful render (h264, matches the `Root.tsx` dimensions/duration) confirms Remotion is ready. Every future animation slot copies this folder (`cp -r templates/remotion-slot edit/animations/slot_<id>`) instead of re-scaffolding with `npx create-video@latest` — faster and deterministic via the committed `package-lock.json`.

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
ffmpeg -version | head -1 && ffprobe -version | head -1
python .claude/skills/video-use/helpers/transcribe.py <one_real_clip> --model tiny
```

If step 3b (Remotion) hasn't been run yet this install, run its render+ffprobe check now rather than skipping it — Remotion is part of the standard workflow, not an optional extra to verify only when first needed.

### 7. Hand off

Tell the user, in one short message:

- The skill is installed project-locally at `.claude/skills/video-use/` — it only applies inside this repo/folder.
- Transcription is fully local and free (`faster-whisper`) — first run downloads the model once, then works offline.
- ffmpeg/ffprobe and a ready-to-use Remotion template are verified working — animation slots can start from `templates/remotion-slot/` immediately.
- All outputs land in `<videos_dir>/edit/` next to their source footage.
- A good first message is: *"edit these into a promo video"* or *"inventory these takes and propose a strategy."*

## Keeping the skill current

- Re-run `pip install -e .` after pulling upstream changes if `pyproject.toml` deps changed.
- If `templates/remotion-slot/package.json` changes upstream, re-run `npm install` inside it and re-verify with a render before trusting it for a new slot.
- Node.js/npm are needed for Remotion (standing, step 3b) and for HyperFrames slots (lazy, needs Node.js 22+).

## Cold-start reminders

- Never assume a paid API is available or required — this install is free-only by design. If asked to reach for ElevenLabs or another paid STT service, decline and use `faster-whisper` instead.
- `ffmpeg` + `ffprobe` are hard requirements, not optional — verify both with `-version` before any editing work, not just at first install.
- `yt-dlp` is optional. Install lazily the first time a user asks to pull from a URL.
- Remotion is pre-installed as a template and part of the standard workflow (step 3b) — don't treat it as lazy/on-demand like HyperFrames and Manim still are.
- If the user is on Linux without a package manager Claude recognizes, print the manual `ffmpeg` install URL and wait rather than guessing.
