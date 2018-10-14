import os, subprocess

BINARIES_PATH = 'C:\\Users\\bbian\\Desktop\\FlareOn5_Challenges\\03_FLEGGO\\FLEGGO'

def get_pswd(binary):
    pswd = ''
    bina = open(BINARIES_PATH + '\\' + binary, 'rb').read()
    i = 0x2ab0
    while bina[i] != chr(0):
        pswd += bina[i]
        i += 2
    return pswd

binaries = os.listdir(BINARIES_PATH)

for pe in binaries:
    pswd = get_pswd(pe)
    out = subprocess.check_output('echo %s | %s' % (pswd, BINARIES_PATH + '\\' + pe), shell=True).split('\n')
    print out[1]
