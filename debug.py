#!/usr/bin/env python3

from sy300midi import *

import mido

import sys

import IPython

midi_ports = get_midi_ports()
if not midi_ports:
    print("Connection Failure: SY300 not connected")
    sys.exit(1)

to_sy300 = mido.open_output(midi_ports['out'])

print(" to_sy300.send(set_sy300([0x30, 0x00, 0x08, 0xd], [0x0]))")

IPython.embed()