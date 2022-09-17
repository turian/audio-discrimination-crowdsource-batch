#!/usr/bin/env python3
"""
Retrieve FSD50K, and unzip it. Please only run this once.
"""

import hashlib
import os
import os.path
from pprint import pprint

from tqdm.auto import tqdm

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

FILES = [
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.zip",
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z01",
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z02",
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z03",
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z04",
    "https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z05",
    "https://zenodo.org/record/4060432/files/FSD50K.eval_audio.zip",
    "https://zenodo.org/record/4060432/files/FSD50K.eval_audio.z01",
]

md5s = {
    "FSD50K.dev_audio.z01": "faa7cf4cc076fc34a44a479a5ed862a3",
    "FSD50K.dev_audio.z02": "8f9b66153e68571164fb1315d00bc7bc",
    "FSD50K.dev_audio.z03": "1196ef47d267a993d30fa98af54b7159",
    "FSD50K.dev_audio.z04": "d088ac4e11ba53daf9f7574c11cccac9",
    "FSD50K.dev_audio.z05": "81356521aa159accd3c35de22da28c7f",
    "FSD50K.dev_audio.zip": "c480d119b8f7a7e32fdb58f3ea4d6c5a",
    "FSD50K.doc.zip": "3516162b82dc2945d3e7feba0904e800",
    "FSD50K.eval_audio.z01": "3090670eaeecc013ca1ff84fe4442aeb",
    "FSD50K.eval_audio.zip": "6fa47636c3a3ad5c7dfeba99f2637982",
    "FSD50K.ground_truth.zip": "ca27382c195e37d2269c4c866dd73485",
    "FSD50K.metadata.zip": "b9ea0c829a411c1d42adb9da539ed237",
}


def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def get_fsd50k_zips(conf):
    origdir = conf["fsd50k"]["orig_path"]
    if not os.path.exists(origdir):
        os.makedirs(origdir)
    for f in tqdm(FILES):
        basefile = os.path.split(f)[1]
        desiredpath = os.path.join(origdir, basefile)
        if not os.path.exists(desiredpath):
            os.system(f"cd {repr(desiredpath)} && wget -c %s" % repr(f))
        assert os.path.exists(desiredpath)
        desired_md5 = md5s[basefile]
        actual_md5 = generate_file_md5(desiredpath)
        assert desired_md5 == actual_md5


def unzip_fsd50k(conf):
    origdir = conf["fsd50k"]["orig_path"]
    os.system(
        f"cd {repr(origdir)} && zip -q -s 0 FSD50K.eval_audio.zip --out unsplit.zip && unzip -q unsplit.zip && rm unsplit.zip"
    )
    os.system(
        f"cd {repr(origdir)} && zip -q -s 0 FSD50K.dev_audio.zip --out unsplit.zip && unzip -q unsplit.zip && rm unsplit.zip"
    )


if __name__ == "__main__":
    conf = load(open("conf.yaml"), Loader=Loader)
    pprint(conf)
    get_fsd50k_zips(conf)
    unzip_fsd50k(conf)
