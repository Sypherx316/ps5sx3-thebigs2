#!/usr/bin/env python3
"""Writes reference_tb20.json from the untouched PS5SX3 TB20 eboot.bin (sha256 f207c681...).
Only needed again if the reference build is ever changed. Usage: make_reference.py <TB20 eboot.bin>"""
import hashlib, json, sys
from autopatch import FakeSelf

data = open(sys.argv[1], "rb").read()
assert hashlib.sha256(data).hexdigest() == "f207c6818a93948591ad35d908560d897b8e27a392c0ab07c778186c9333955a"
sf = FakeSelf(bytearray(data))
CALC, CALC_END = 0xE62010, 0xE625CA   # the function, then its two lambdas
RAW, RAW_END = 0xE7BC50, 0xE7BD5F
ref = {
    "build": "PS5SX3 TB20",
    "calc": {
        "va": CALC, "code": sf.read(CALC, CALC_END - CALC).hex(), "first_xref": 0xE6235F,
        "addresses": {
            "start": 0xE622F0, "join": 0xE623CB, "fail": 0xE623FD, "b_start": 0xE62410, "b_end": 0xE62430,
            "lambda_u32": 0xE62430, "lambda_u16": 0xE62500, "get_address": 0xE61C10,
            "fxo": 0x6E71700, "srcloc": 0x68AF918, "sudo": 0xA14E1A0,
        },
        "fields": {
            "command": 0x14444, "immediate": 0x14448,
            "push_buffer_data": 0x208E30, "push_buffer_size": 0x208E38,
            "index_array_address": 0x181C, "registers": [0x1820, 0x181C, 0x1DAC, 0x1DB0],
        },
    },
    "raw": {"va": RAW, "code": sf.read(RAW, RAW_END - RAW).hex(), "first_xref": 0xE7BC9A},
}
json.dump(ref, open("reference_tb20.json", "w"), indent=1)
print("reference_tb20.json written:", len(ref["calc"]["code"]) // 2, "+", len(ref["raw"]["code"]) // 2, "bytes of code")
