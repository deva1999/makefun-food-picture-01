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

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "food.png"


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


def main() -> None:
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    data = IMAGE.read_bytes()
    dest = dest_dir / "entry.png"
    dest.write_bytes(data)
    if dest.stat().st_size != len(data):
        raise SystemExit(f"short write: {dest} holds {dest.stat().st_size} of {len(data)} bytes")


if __name__ == "__main__":
    main()
