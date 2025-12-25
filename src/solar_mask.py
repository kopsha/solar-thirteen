#!/usr/bin/env python3
"""
Takes a ppm image as input and renders a calendar on it.
"""

import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeSans.ttf", 89)


def mask_image(buffer: bytes):
    format_id, _, buffer = buffer.partition(b"\n")
    if format_id != b"P6":
        raise ValueError("Image is not valid PPM format.")

    size, _, buffer = buffer.partition(b"\n")
    width, height = map(int, size.decode().split())
    color_space, _, buffer = buffer.partition(b"\n")

    img16 = Image.frombuffer("RGB", (width, height), buffer, "raw", "RGB;16B", 0, 1)

    # Render text into an 8-bit alpha mask
    mask8 = Image.new("L", img16.size, 0)
    draw = ImageDraw.Draw(mask8)
    draw.text((250, 250), "Hello, world", fill=255, font=FONT)

    # Create 16 bit mask image for the text
    text_color = (65535, 32767, 16535)
    mask16 = Image.new("RGB", img16.size, text_color)

    masked_image = Image.composite(mask16, img16, mask8)
    arr16 = np.array(masked_image, dtype=np.uint16)
    masked_buffer = arr16.astype('<u2').tobytes()  # little-endian RGB;16L

    sys.stdout.buffer.write(b"\n".join((b"P6", size, color_space, b"")))
    sys.stdout.buffer.write(masked_buffer)

if __name__ == "__main__":
    original_image = sys.stdin.buffer.read()
    mask_image(original_image)
