# 0 = auto, 1 = stop
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0D], [0x00]))
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0D], [0x01]))

# set history to -1 where it is already, probably:
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0C], [0x01]))

# set to -2:
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0C], [0x02]))


# before:
# blender osc 1: u01 osc 1

to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0], [0x0, 0x0, 0x1]))

# after:
# blender osc 1: u01 osc 2

to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x0], [0x0, 0x0, 0x1]))

# after:
# blender osc 1: u01 osc 3

# so the final number is the osc number

# blender chain
# U20 = 1, 3, 3b

# U01 = 0, 0, 3f
# U02 = 0, 1, 3e
# U03 = 0, 2, 3d

# setting blender chain: (fz = from zero)
# range: 0-168 (168/2 = 84) (U01-U99, P01-P70)
# 0, 0 = U01
# 0, 1 = U02
# 0, 2, = U03
# 0, 3 = U04
# 0, 9, = U10
# 0, x62 (98) = U03 # wtf?
# 0, xa = U11
# 0, xf = U16
# 0, x10 = U01
# 1, 0, = U17
# 1, xf, = U32 
# 2, 0, = U33 (fz32)
# 5, 8 = U89 (fz88)
# 6, 2 = U99 
# 6, 3 = P01
# xa, 0 = P62
# xa, 8 = P70 # maximum

# bl osc 1 - 3 bytes - range 0-506 (0-0x1fa) oscs 1-3, patches U01-U99, P01-P70
# it seems like none of the values can be > 0xf
# max = 1, xf, xa = P70 OSC3
# min = 0, 0, 0 = U01 OSC1
# So the counting goes: U01 OSC1, U01 OSC2, U01 OSC3, U02 OSC1, ...

# find out if we are in auto mode:
to_SY300.send(req_sy300([0x30, 0x00, 0x8, 0xd], [1])) # 0 means yes, 1 means no




# chain:
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x09], [0x00,0x0a,0x08])) # sets to U11
to_SY300.send(set_sy300([0x30, 0x00, 0x08, 0x09], [0x00,0x0a,0x00])) # " " " "

