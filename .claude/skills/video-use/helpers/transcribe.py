"""Transcribe a video with faster-whisper (local, open-source, free).

Extracts mono 16kHz audio via ffmpeg, runs it through a local Whisper
model (CTranslate2 / faster-whisper) with word-level timestamps, writes
a Scribe-shaped payload to <edit_dir>/transcripts/<video_stem>.json so
it stays compatible with pack_transcripts.py / render.py downstream.

No API key, no per-minute cost, no network call after the model is
cached locally (~/.cache/huggingface). Optional speaker diarization via
pyannote.audio (also free/open-source) behind --diarize; requires a
free Hugging Face token and accepting the pyannote model terms once.

Cached: if the output file already exists, transcription is skipped.

Usage:
    python helpers/transcribe.py <video_path>
    python helpers/transcribe.py <video_path> --edit-dir /custom/edit
    python helpers/transcribe.py <video_path> --language en
    python helpers/transcribe.py <video_path> --model small
    python helpers/transcribe.py <video_path> --diarize --num-speakers 2
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


DEFAULT_MODEL = "small"  # tiny/base/small/medium/large-v3 — bigger = slower + more accurate


def extract_audio(video_path: Path, dest: Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_whisper(
    audio_path: Path,
    model_size: str,
    language: str | None,
) -> list[dict]:
    """Run faster-whisper with word timestamps. Returns a flat word list
    shaped like Scribe's: {"type": "word", "text", "start", "end"}.
    """
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        vad_filter=True,
    )

    words: list[dict] = []
    for seg in segments:
        for w in (seg.words or []):
            text = w.word.strip()
            if not text:
                continue
            words.append({
                "type": "word",
                "text": text,
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "speaker_id": None,
            })
    return words


def apply_diarization(words: list[dict], audio_path: Path, num_speakers: int | None) -> None:
    """Tag each word with a speaker_id in place, using pyannote.audio.

    Free and open-source, but requires a Hugging Face token (also free)
    with the pyannote/speaker-diarization model terms accepted once at
    https://huggingface.co/pyannote/speaker-diarization-3.1. Skips
    quietly (leaving speaker_id=None) if the dependency or token is
    unavailable — diarization is optional, transcription is not.
    """
    try:
        from pyannote.audio import Pipeline
    except ImportError:
        print("  ! pyannote.audio not installed, skipping diarization "
              "(pip install pyannote.audio)", file=sys.stderr)
        return

    import os
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        print("  ! no HF_TOKEN set, skipping diarization "
              "(free token: https://huggingface.co/settings/tokens)", file=sys.stderr)
        return

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", use_auth_token=token
    )
    diarization = pipeline(str(audio_path), num_speakers=num_speakers)

    turns = [(t.start, t.end, spk) for t, _, spk in diarization.itertracks(yield_label=True)]
    for w in words:
        mid = (w["start"] + w["end"]) / 2
        for start, end, spk in turns:
            if start <= mid <= end:
                w["speaker_id"] = spk
                break


def transcribe_one(
    video: Path,
    edit_dir: Path,
    model_size: str = DEFAULT_MODEL,
    language: str | None = None,
    num_speakers: int | None = None,
    diarize: bool = False,
    verbose: bool = True,
    **_ignored,
) -> Path:
    """Transcribe a single video. Returns path to transcript JSON.

    Cached: returns existing path immediately if the transcript already exists.
    """
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  extracting audio from {video.name}", flush=True)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio)
        size_mb = audio.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  transcribing {video.stem}.wav ({size_mb:.1f} MB) with "
                  f"faster-whisper/{model_size}", flush=True)
        words = run_whisper(audio, model_size, language)
        if diarize:
            if verbose:
                print("  diarizing speakers", flush=True)
            apply_diarization(words, audio, num_speakers)

    payload = {"words": words}
    out_path.write_text(json.dumps(payload, indent=2))
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  saved: {out_path.name} ({kb:.1f} KB) in {dt:.1f}s")
        print(f"    words: {len(words)}")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Transcribe a video locally with faster-whisper (free, no API key)"
    )
    ap.add_argument("video", type=Path, help="Path to video file")
    ap.add_argument(
        "--edit-dir",
        type=Path,
        default=None,
        help="Edit output directory (default: <video_parent>/edit)",
    )
    ap.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="faster-whisper model size: tiny/base/small/medium/large-v3 (default: small)",
    )
    ap.add_argument(
        "--language",
        type=str,
        default=None,
        help="Optional ISO language code (e.g., 'en', 'es'). Omit to auto-detect.",
    )
    ap.add_argument(
        "--diarize",
        action="store_true",
        help="Tag words with speaker IDs via pyannote.audio (needs free HF_TOKEN).",
    )
    ap.add_argument(
        "--num-speakers",
        type=int,
        default=None,
        help="Optional number of speakers when known. Only used with --diarize.",
    )
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()

    transcribe_one(
        video=video,
        edit_dir=edit_dir,
        model_size=args.model,
        language=args.language,
        num_speakers=args.num_speakers,
        diarize=args.diarize,
    )


if __name__ == "__main__":
    main()
