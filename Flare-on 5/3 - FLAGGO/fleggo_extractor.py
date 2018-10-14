import os, subprocess

BINARIES_PATH = 'C:\\Users\\bbian\\Desktop\\FlareOn5_Challenges\\03_FLEGGO\\FLEGGO'

def shell(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except Exception, e:
        output = str(e.output)
    return output.split('\n')

def get_pswd(binary):
    pswd = ''
    bina = open(binary, 'rb').read()
    i = 0x2ab0 #password fixed position
    while bina[i] != chr(0):
        pswd += bina[i]
        i += 2
    return pswd

binaries = os.listdir(BINARIES_PATH)

for pe in binaries:
    pe = BINARIES_PATH + '\\' + pe
    out = shell('echo %s | %s' % (get_pswd(pe), pe))
    print out[2]
