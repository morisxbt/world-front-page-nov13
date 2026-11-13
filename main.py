"""Copy the prepared competition image to the requested output directory."""

import os
import shutil


output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(output_dir, exist_ok=True)
shutil.copyfile("entry.png", os.path.join(output_dir, "entry.png"))
