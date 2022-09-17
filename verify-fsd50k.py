#!/usr/bin/env python3
"""
Verify that you have all fsd50k wav files, and they are the correct size.
"""

import glob
import gzip
import hashlib
import json
import os
import os.path
from pathlib import Path
from pprint import pprint

from tqdm.auto import tqdm

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


def verify_fsd50k(conf):
    with gzip.open("fsd50k-orig-sizes.json.gz", "r") as f:
        file_sizes = json.loads(f.read())
    origdir = Path(conf["fsd50k"]["orig_path"])
    files = sorted(origdir.rglob("FSD50K.eval_audio/*wav")) + sorted(
        origdir.rglob("FSD50K.dev_audio/*wav")
    )
    for f in tqdm(files):
        basef = f.relative_to(origdir).as_posix()
        assert file_sizes[basef] == f.stat().st_size


if __name__ == "__main__":
    conf = load(open("conf.yaml"), Loader=Loader)
    pprint(conf)
    verify_fsd50k(conf)
