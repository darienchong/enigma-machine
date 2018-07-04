from Rotor import Rotor
from Reflector import Reflector
from Plugboard import Plugboard
from Util import Util

# The EnigmaMachine class simulates the action of an Enigma Machine, used for cryptographical purposes.
class EnigmaMachine:
    verbose = False
    alphabetPos = Util.alphabetPos

    # C'tor for EnigmaMachine.
    # @param rotorOrder A string indicating the order of the rotors in Roman numerals e.g. 'III II IV' indicates Rotors III, II, and IV from left to right.
    # @param rotorPos A string indicating the starting positions of the rotors, from left to right (e.g. 'A A A'). The default position is 'A A A', if an empty string is given.
    # @param ringSetting A string indicating the ring setting for the rotors, from left to right (e.g. '5 10 18'). The default setting is '1 1 1', if an empty string is given. 
    # @param plugboardPairs A string of character pairs indicating the pairs to be used in the plugboard e.g. 'AB CD EF GH'. The default setting is '', if an empty string is given.
    def __init__(self, rotorOrder, rotorPos, ringSetting, plugboardPairs):
        # Whether to advance the middle rotor on this step.
        self.doubleStep = False

        # Rotors I, II, III, IV, and V from Enigma I and M3 Army version.
        self.config = [['EKMFLGDQVZNTOWYHXUSPAIBRCJ',['R']],['AJDKSIRUXBLHWTMCQGZNPYFVOE',['F']],['BDFHJLCPRTXVZNYEIWGAKMUSQO',['W']],['ESOVPZJAYQUIRHXLNFTGKDCMWB',['K']],['VZBRGITYUPSDNHLXAWMJQOFECK',['A']]]

        # A list of all the rotors we have.
        self.rotorRef = []

        # An ordered list of the rotors, from leftmost to rightmost. 
        self.rotors = []

        # Initialising our rotors.
        for g in range(0, len(self.config)):
            self.rotorRef.append(Rotor(self.config[g]))
        
        # Putting our rotors in the specified order.
        rotorOrder = rotorOrder.split(" ")
        # Convert our string into an easier form to read for rotor placement.
        rotorOrder = [r.replace('IV', '4').replace('V', '5').replace('III', '3').replace('II', '2').replace('I', '1') for r in rotorOrder]
        for h in range(0, len(rotorOrder)):
            temp = int(rotorOrder[h])
            self.rotors.append(self.rotorRef[temp - 1])

        # We set our starting rotor position, as specified.
        # For more information, check Rotor::setRotorPos.
        if (not rotorPos == ''):
            rotorPos = rotorPos.split(' ')
            for j in range(0, len(rotorPos)):
                self.rotors[j].setRotorPos(rotorPos[j])
        
        # We modify the ring-setting according to our ring-setting offsets, as specified.
        # For more info, see Rotor::setRingSetting.
        if (not ringSetting == ''):
            ringSetting = ringSetting.split(" ")
            for i in range(0, len(ringSetting)):
                if (ringSetting[i] in self.alphabetPos):
                    ringSetting[i] = Util.alphabetToNum(ringSetting[i])
                if (not isinstance(ringSetting[i], int)):
                    ringSetting[i] = int(ringSetting[i])
                self.rotors[i].setRingSetting(ringSetting[i])
        
        # Initialising plugboard and reflector.
        # TODO: Allow for choice of reflectors?
        self.plugboard = Plugboard(plugboardPairs)
        self.reflector = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT') # Reflector B-Wide

    # Initialises the Enigma Machine with the two trigrams given at the start of a message.
    # @param trigramStr A string consisting of the two trigrams to be used e.g 'ABC DEF'
    # @return null
    def setTrigramSettingsDecrypt(self, trigramStr):
        trigramStrLs = trigramStr.split(' ')
        self.setRotorPos(trigramStrLs[0].replace('', ' ')[1:-1])
        self.setRotorPos(self.input(trigramStrLs[1]).replace('',' ')[1:-1])

    # Initialises the Enigma Machine with the two trigrams given at the start of a message.
    # @param trigramStr A string consisting of the two trigrams to be used e.g 'ABC DEF'
    # @return The encoded trigram sequence, to use in decrypting the message.
    def setTrigramSettingsEncrypt(self, trigramStr):
        trigramStrLs = trigramStr.split(' ')
        self.setRotorPos(trigramStrLs[0].replace('', ' ')[1:-1])
        encodedTrigram = self.input(trigramStrLs[1])
        self.setRotorPos(trigramStrLs[1].replace('', ' ')[1:-1])
        return trigramStrLs[0] + ' ' + encodedTrigram
        
        
    # Sets the rotor positions to new ones.
    # @param rotorPos A string consisting of the new rotor positions, e.g. 'A A A'
    # @return null
    def setRotorPos(self, rotorPos):
        if (not rotorPos == ''):
            rotorPos = rotorPos.split(' ')
            for j in range(0, len(rotorPos)):
                self.rotors[j].setRotorPos(rotorPos[j])

    # Returns a string that has been passed through the EnigmaMachine.
    # @param words The string to encode/decode. If not in uppercase, it will be converted to uppercase before en/decoding.
    # @return The encoded/decoded string, in capital letters.
    def input(self, words):
        words = words.upper()
        returnText = ''

        # Inner function to simulate passing a single character through the Enigma Machine.
        # @param char The character to pass through.
        # @return The encoded/decoded character.
        def passThrough(char):
            rightRotor = self.rotors[len(self.rotors) - 1]
            midRotor = self.rotors[len(self.rotors) - 2]
            leftRotor = self.rotors[len(self.rotors) - 3]
            
            # Advance the rotor positions before encoding.
            rightRotor.rotate()
            if (self.doubleStep):
                midRotor.rotate()
                leftRotor.rotate()
                if (self.verbose):
                    print("Double stepped.")
                self.doubleStep = False

            # Right rotor has advanced to its step position, causing the middle rotor to rotate.
            if (rightRotor.rotorPos in rightRotor.stepLs):
                if (self.verbose):
                    print("Right rotor caused middle rotor to rotate.")
                midRotor.rotate()
              
                # Double stepping is where the middle rotor has advanced to the position before its step position e.g. if it steps the left rotor as it goes from E to F, it would be in position to double step at E. Once in position to double step, the middle rotor will advance to its step position upon the next rotation of the right rotor, causing the left rotor to step as well.
                # e.g. say the middle rotor advances the left rotor at E -> F
                # A-D-V (right rotor in position to rotate middle rotor)
                # A-E-W (middle rotor in position to double step)
                # B-F-X (right rotor rotated -> middle rotor double stepped -> left rotor rotated)
                if ((midRotor.rotorPos + 1) % len(self.alphabetPos) in midRotor.stepLs):
                    if (self.verbose):
                        print("Middle rotor in position to double step.")
                    self.doubleStep = True

            if (self.verbose):
                # Exposing rotor positions, for debugging purposes.
                print(self.alphabetPos[leftRotor.rotorPos] + "-" + self.alphabetPos[midRotor.rotorPos] + "-" + self.alphabetPos[rightRotor.rotorPos])        

            # Now encoding the character.
            # Plugboard
            char = self.plugboard.passThrough(char)

            # Rotors (from the right)
            for i in range(0, len(self.rotors)):
                char = self.rotors[len(self.rotors) - 1 - i].passThroughFromRight(char)

            # Reflector
            char = self.reflector.passThrough(char)

            # Rotors (from the left)
            for j in range(0, len(self.rotors)):
                char = self.rotors[j].passThroughFromLeft(char)
            
            # Plugboard again
            char = self.plugboard.passThrough(char)

            return char
        
        # Only encrypt words in our alphabet, ignore punctuation, lowercase characters, etc.
        for i in range(0, len(words)):
            if not (words[i] in Util.alphabet):
                returnText += words[i]
            else:
                returnText += passThrough(words[i])
        
        return returnText