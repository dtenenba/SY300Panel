import time
from sy300midi import *


midi_ports = get_midi_ports()
to_sy300 = mido.open_output(midi_ports['out'])
to_sy300.send(set_sy300([0x7F, 0x00, 0x00, 0x01], [0x01]))  # set the SY300 into verbose or editor mode 
from_sy300 = mido.open_input(midi_ports['in'])

print("Waiting...")


def get_top_level(adr):
    f2 = adr[0:2]
    if f2 == ['0x0', '0x0']:
        return "SETUP"
    if  f2 == ['0x10', '0x0']:
        return "SYSTEM"
    if f2 == ['0x20', '0x0']:
        return "PATCH (Temporary)"
    if f2 == ['0x20', '0x04']:   
        return "PATCH (User 1)"
    if f2 == ['0x23', '0x0C']:
        return "PATCH (User 99)"
    if f2 == ['0x30', '0x0']:
        return "SYSTEMP"
    if f2 == ['0x7F', '0x0']:
        return "EDITOR/VERBOSE"
    return f"UNKNOWN {f2}"

top  = {''}

while True:
    for msg in from_sy300.iter_pending():
        if msg.type == 'sysex':
            data = [hex(x) for x in msg.data]
            adr = data[7:11]
            top_level = get_top_level(adr)
            if top_level != "SYSTEMP":
                continue
            print(f"got sysex msg: {msg.hex()}")
            if data[6] == '0x11':
                print("request")
            elif data[6] == '0x12':
                print("fromsy300")
            payload = data[11:]
            print(f"adr: {adr}")
            print(f"payload: {payload} ({len(payload)})")
            print(f"len: {len(msg.data)}, hex: {hex(len(msg.data))}")
            print(top_level)
            print()
    time.sleep(0.01)
