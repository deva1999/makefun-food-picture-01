"""food-picture-01 entry: write the bundled food image to the output.

The image (food.png, beside this file) was made to be the best-looking
food picture for the AI judge: a steaming bowl of tonkotsu ramen caught
at the moment of the noodle lift — glossy creamy broth with oil
droplets, seared chashu, a halved seasoned egg with a jammy yolk,
scallions and nori, steam rising, on a dark wooden table in soft
window light.

The program copies those bytes, unchanged, to <output>/entry.png, so
the two grader runs write byte-identical output. Outside the grader's
container, MAKEFUN_OUTPUT_DIR stands in for /output.
"""

import hashlib
import os
import struct
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "food.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (832, 832)  # width, height of food.png


def output_dir() -> Path:
    """Where the grader wants the image: /output, or the stand-in env var.

    MAKEFUN_OUTPUT_DIR wins when set. Otherwise /output, falling back to
    a local ./output when /output cannot be created or written (a plain
    developer machine rather than the grader's container).
    """
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override)
    system_out = Path("/output")
    try:
        system_out.mkdir(parents=True, exist_ok=True)
        if os.access(system_out, os.W_OK):
            return system_out
    except OSError:
        pass
    return HERE / "output"


def check_source_png(data: bytes) -> None:
    """Fail loudly if the bundled image is not the PNG we entered.

    The grader runs this program as-is; a truncated or swapped food.png
    would otherwise be copied verbatim and score as a broken entry.
    Parse just enough PNG structure to be sure: the 8-byte signature,
    then the IHDR chunk carrying the pixel dimensions.
    """
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit(f"{IMAGE} is not a PNG (bad signature)")
    ihdr = data[len(PNG_SIGNATURE):len(PNG_SIGNATURE) + 8]
    if len(ihdr) < 8 or ihdr[4:] != b"IHDR":
        raise SystemExit(f"{IMAGE} has no IHDR as its first chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        raise SystemExit(
            f"{IMAGE} is {width}x{height}, expected "
            f"{EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}"
        )


def main() -> None:
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    data = IMAGE.read_bytes()
    check_source_png(data)
    dest = dest_dir / "entry.png"
    # Copy atomically: write beside the destination, then rename over
    # it, so an interrupted run can never leave a partial entry.png.
    fd, tmp_name = tempfile.mkstemp(dir=dest_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
        os.chmod(tmp_name, 0o644)  # mkstemp makes 0600; match a plain write
        os.replace(tmp_name, dest)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    if dest.stat().st_size != len(data):
        raise SystemExit(f"short write: {dest} holds {dest.stat().st_size} of {len(data)} bytes")
    if hashlib.sha256(dest.read_bytes()).digest() != hashlib.sha256(data).digest():
        raise SystemExit(f"checksum mismatch: {dest} differs from {IMAGE}")


if __name__ == "__main__":
    main()
