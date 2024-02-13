import os

script_dir = os.path.dirname(os.path.realpath(__file__))
def GetProfilePath(pos):
    return os.path.join(script_dir, "profile"+str(pos))

def GetActivationKey(chainnumber, storenumber, posnumber):
    return str(chainnumber)+"-"+str(storenumber)+"-"+str(posnumber)
