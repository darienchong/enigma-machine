from Util import Util

# The Reflector class simulates the physical reflector in an Enigma Machine.
class Reflector:
  
    # C'tor for the Reflector class.
    # @param config The configuration for the Reflector, which should consist of a string indicating which letters are mapped to which other letters. For example, 'YZABCD...' would indicate A -> Y, B -> Z, etc. This mapping should be bidirectional (e.g. (A -> Y) -> (Y -> A))
    def __init__(self, config):
        configLen = len(config)
        self.reflector = []
        for i in range(0, configLen):
            self.reflector.append(config[i])
        self.alphabetPos = Util.alphabetPos
    
    # Simulates passing a character through the reflector.
    # @param char The character to be passed through.
    # @return The encoded character.
    def passThrough(self, char):
        temp = self.reflector[self.alphabetPos.index(char)]
        return temp