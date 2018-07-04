from Util import Util

# The Rotor class simulates the action of the rotors in an Enigma Machine.
class Rotor:
  
    # C'tor for the Rotor class.
    # @param config The configuration for the Rotor, which should be a list of two elements, the first being the configuration string e.g. 'YZABCD...', which would indicate A -> Y, B -> Z, etc. The second should be a list of letters at which the rotor steps over i.e. if the window is over that letter, the next rotor will have been stepped. In this case, when the rotor arrives at those letters, it will cause the next rotor to be stepped.
    def __init__(self, config):
        self.alphabetPos = Util.alphabetPos
        self.rotorMapping = []
        self.stepLs = []
        self.ringSetting = 0
        self.rotorPos = 0

        for j in range(0, len(config[0])):
            self.rotorMapping.append(config[0][j])
        
        for h in range(0, len(config[1])):
            config[1][h] = self.alphabetPos.index(config[1][h])
        self.stepLs = config[1]

    # Setter method for ring setting.
    # @param ringSetting This should be a number from 1 to 26. 
    def setRingSetting(self, ringSetting):
        self.ringSetting = ringSetting - 1

    # Setter method for rotor position.
    # @param rotorPos This should be a letter indicating the starting position of the rotor e.g. 'A'
    def setRotorPos(self, rotorPos):
        self.rotorPos = self.alphabetPos.index(rotorPos)
    
    # Simulates passing a character through the rotor from the right side of the rotor.
    # e.g. passing the letter A through:
    # A --(ring setting)--> * --(rotor mapping)--> ** --(ring setting)--> end result 
    # @param char The character to encode.
    # @return The encoded character.
    def passThroughFromRight(self, char):
        temp = self.alphabetPos[(self.alphabetPos.index(char) - self.ringSetting + self.rotorPos) % len(self.alphabetPos)]
        temp = self.rotorMapping[self.alphabetPos.index(temp)]
        temp = self.alphabetPos[(self.alphabetPos.index(temp) + self.ringSetting - self.rotorPos) % len(self.alphabetPos)]
        return temp
    
    # Simulates passing a character through the rotor from the left side of the rotor.
    # @param char The character to encode.
    # @return The encoded character.
    def passThroughFromLeft(self, char):
        temp = self.alphabetPos[(self.alphabetPos.index(char) - self.ringSetting + self.rotorPos) % len(self.alphabetPos)]
        temp = self.alphabetPos[self.rotorMapping.index(temp)]
        temp = self.alphabetPos[(self.alphabetPos.index(temp) + self.ringSetting - self.rotorPos) % len(self.alphabetPos)]
        return temp

    # Simulates a rotation of the rotor (step).
    # @return null
    def rotate(self):
        self.rotorPos += 1
        self.rotorPos = self.rotorPos % len(self.alphabetPos)