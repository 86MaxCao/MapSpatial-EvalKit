"""Unified media handling — single entry for image loading, URL download, video frames.

Consolidates 3 categories of duplication from gate2building:
  - URL download (5 places, 3 strategies; SenseNovaU1Backend had none → crash)
  - Video frame extraction (4 places; frame limits inconsistent: U1=8, others=16)
  - Temp file lifecycle (scattered tempfile + manual cleanup lists)
"""

from __future__ import annotations

import hashlib
import io
import os
import tempfile
from pathlib import Path
from typing import Union

from PIL import Image

ImageSource = Union[Path, str, Image.Image]


def load_image(src: ImageSource, *, cache: "MediaCache | None" = None) -> Image.Image:
    """Load an image from a local path, http(s) URL, data URI, or pass through PIL.

    URL results are cached to disk by URL hash when a MediaCache is provided.
    """
    if isinstance(src, Image.Image):
        return src

    s = str(src)

    # data URI
    if s.startswith("data:"):
        header, _, data = s.partition(",")
        import base64
        raw = base64.b64decode(data)
        return Image.open(io.BytesIO(raw)).convert("RGB")

    # http(s) URL
    if s.startswith(("http://", "https://")):
        if cache is not None:
            cached = cache.cache_dir / _url_hash(s)
            if cached.exists():
                return Image.open(cached).convert("RGB")
        import requests
        resp = requests.get(s, timeout=60)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
        if cache is not None:
            cached = cache.cache_dir / _url_hash(s)
            img.save(cached)
        return img

    # local path
    p = Path(s)
    if not p.exists():
        raise FileNotFoundError(f"image not found: {p}")
    return Image.open(p).convert("RGB")


def sample_frames(video: Path, *, n: int = 16, reader: str = "auto") -> list[Image.Image]:
    """Uniformly sample n frames from a video file.

    reader='auto' tries decord → cv2 → imageio in order of availability.
    """
    if reader == "auto":
        for r in ("decord", "cv2", "imageio"):
            try:
                return _sample_frames(video, n, r)
            except ImportError:
                continue
        raise ImportError("no video reader available (tried decord, cv2, imageio)")
    return _sample_frames(video, n, reader)


def _sample_frames(video: Path, n: int, reader: str) -> list[Image.Image]:
    video = str(video)
    if reader == "decord":
        import decord  # type: ignore
        vr = decord.VideoReader(video)
        total = len(vr)
        indices = _even_indices(total, n)
        frames = vr.get_batch(indices).asnumpy()  # (N, H, W, C)
        return [Image.fromarray(f) for f in frames]

    if reader == "cv2":
        import cv2  # type: ignore
        import numpy as np
        cap = cv2.VideoCapture(video)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        indices = _even_indices(total, n)
        frames = []
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(frame))
        cap.release()
        return frames

    if reader == "imageio":
        import imageio.v3 as iio  # type: ignore
        import numpy as np
        frames_np = iio.imread(video, index=None)  # may load all
        total = len(frames_np)
        indices = _even_indices(total, n)
        return [Image.fromarray(frames_np[i]) for i in indices]

    raise ValueError(f"unknown reader: {reader!r}")


def _even_indices(total: int, n: int) -> list[int]:
    if total <= 0:
        return []
    n = min(n, total)
    return [int(i * total / n) for i in range(n)]


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


class MediaCache:
    """Context manager for temporary media files.

    Cleanup on exit prevents temp file leakage that plagued gate2building.
    """

    def __init__(self, cache_dir: Path | None = None):
        if cache_dir is None:
            self._tmp = tempfile.TemporaryDirectory(prefix="mapspatial_media_")
            self.cache_dir = Path(self._tmp.name)
        else:
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._tmp = None
        self._materialized: list[Path] = []

    def __enter__(self) -> "MediaCache":
        return self

    def __exit__(self, *exc) -> None:
        self.cleanup()

    def materialize(self, img: Image.Image, *, suffix: str = ".jpg") -> Path:
        """Save a PIL image to disk, return the path. Tracked for cleanup."""
        fd, path = tempfile.mkstemp(
            dir=str(self.cache_dir), suffix=suffix, prefix="mspat_"
        )
        os.close(fd)
        img.save(path)
        self._materialized.append(Path(path))
        return Path(path)

    def cleanup(self) -> None:
        for p in self._materialized:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass
        self._materialized.clear()
        if self._tmp is not None:
            self._tmp.cleanup()
