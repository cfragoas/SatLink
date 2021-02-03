from numpy import log10

def FreeSpaceAtt(d, f): #d em km e f em MHz

    AttFs = 32.4 + 20 * log10(d) + 20 * log10(f* 1000)

    return AttFs
