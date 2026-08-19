"""Minimal file I/O utilities for image downloading.

Adapted from outdoor-spatial-intelligence-scripts/utils/file_io.py.
Only includes download_image_from_url (needed by backends for URL images).
"""

from __future__ import annotations

import logging
from io import BytesIO
from typing import Optional

import requests
from PIL import Image

logger = logging.getLogger(__name__)
_thread_session = None


def _thread_requests_session() -> requests.Session:
    global _thread_session
    if _thread_session is None:
        _thread_session = requests.Session()
    return _thread_session


def normalize_image_url(url: str) -> str:
    """Normalize image URL (replace gaode with gaode-office for reliability)."""
    return url.replace("gaode.com", "gaode-office.com")


def download_image_from_url(
    image_url: str,
    timeout: int = 30,
    stream: bool = False,
    convert_to_rgb: bool = True,
) -> Optional[Image.Image]:
    """Download an image from URL, return PIL Image or None on failure."""
    try:
        session = _thread_requests_session()
        response = session.get(image_url, timeout=timeout, stream=stream)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        if convert_to_rgb and img.mode != "RGB":
            img = img.convert("RGB")
        return img
    except Exception as e:
        logger.debug(f"Failed to download image from {image_url}: {e}")
        return None
