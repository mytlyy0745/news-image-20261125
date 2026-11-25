#!/usr/bin/env python3
"""Entrypoint for make.fun competition news-image-20261125.

Validates the front-page image (entry.png, shipped in this repo) and
copies it byte-identical to the grader's output directory.
Standard library only; no network, no clock, no randomness.

Run:  python3 main.py
Writes: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
"""
import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
EXPECT_W, EXPECT_H = 1024, 1024


def fail(msg):
    print("main.py: error: " + msg, file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Validate PNG structure: magic, IHDR size, chunk CRCs, trailing IEND."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file (bad magic)")
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    pos = 8
    seen_ihdr = False
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header at offset %d" % pos)
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            fail("truncated %s chunk at offset %d" % (ctype.decode("latin1"), pos))
        chunk = data[pos + 4:pos + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        if zlib.crc32(chunk) & 0xFFFFFFFF != stored_crc:
            fail("bad CRC in %s chunk" % ctype.decode("latin1"))
        if ctype == b"IHDR":
            if length != 13:
                fail("IHDR must be 13 bytes")
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
            if (width, height) != (EXPECT_W, EXPECT_H):
                fail("expected %dx%d, got %dx%d"
                     % (EXPECT_W, EXPECT_H, width, height))
            bit_depth = data[pos + 16]
            color_type = data[pos + 17]
            if bit_depth != 8 or color_type not in (2, 6):
                fail("expected 8-bit RGB/RGBA, got depth %d type %d"
                     % (bit_depth, color_type))
            seen_ihdr = True
        if ctype == b"IEND":
            if length != 0:
                fail("IEND must be empty")
            if pos + 12 != len(data):
                fail("trailing bytes after IEND")
            seen_iend = True
            break
        pos += 12 + length
    if not seen_ihdr:
        fail("no IHDR chunk")
    if not seen_iend:
        fail("no trailing IEND chunk")


def main():
    if not os.path.isfile(SRC):
        fail("entry.png missing next to main.py")
    with open(SRC, "rb") as fh:
        data = fh.read()
    check_png(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)

    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output differs from entry.png after copy")
    print("main.py: wrote %s (%d bytes, %dx%d, sha256 %s, verified "
          "byte-identical)"
          % (dst, len(data), EXPECT_W, EXPECT_H,
             hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
