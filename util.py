def num_to_bpatch(num):
    if num < 99:
        return "U" + str(num+1).zfill(2)
    return "P" + str(num - 98).zfill(2)

def get_bosc_num(osc, patchnum):
    pass
