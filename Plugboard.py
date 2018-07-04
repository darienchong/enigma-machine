# The Plugboard class simulates the physical plugboard in an Enigma Machine, which swaps two characters if they are indicated in the plugboard settings.
class Plugboard:
  
    # C'tor for the Plugboard class.
    # @param pairStr The string holding character pairs for swapping, e.g. 'AB CD EF GH' indicates A<->B, etc.
    def __init__(self, pairStr):
        self.pairs = {}
        pairLs = pairStr.split(' ')
        for pair in pairLs:
            if (not pair == ''):
                self.pairs[pair[0]] = pair[1]
                self.pairs[pair[1]] = pair[0]
    
    # Simulates passing a character through the plugboard.
    # @param char The character to be encoded
    # @return The same char if the plugboard is not configured for that char, else swap the char and return.
    def passThrough(self, char):
        if (char in self.pairs):
            return self.pairs.get(char)
        else:
            return char