"""Copy the prepared competition image to the requested output directory."""

import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entry.png").write_bytes(source.read_bytes())


if __name__ == "__main__":
    main()
