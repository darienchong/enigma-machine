import re

# Utility class with useful functions that do not belong to a specific component of the Enigma Machine.
class Util:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabetPos = []
    for i in range(0, len(alphabet)):
        alphabetPos.append(alphabet[i])

    # Converts a letter of the alphabet to its numerical equivalent, i.e. A=1 ... Z=26.
    # @param char The character to convert.
    @staticmethod
    def alphabetToNum(char):
        return Util.alphabetPos.index(char) + 1

    
    # Converts a number to its alphabet equivalent.
    # @param num The number (in [1, 26]) to convert.
    @staticmethod
    def numToAlphabet(num):
        return Util.alphabetPos[num - 1]

    # Converts decrypted text (typically in 5-letter segments with various annotations) into legible form.
    # @param text The text to parse.
    # @return Legible text, with converted annotations.
    @staticmethod
    def parseText(text):
        insideBracket = False

        # Inner method to switch between brackets.
        # @param matchObj Unused parameter for re.sub(..)
        # @return The bracket to be used.
        def bracketChooser(matchObj):
            nonlocal insideBracket
            if (not insideBracket):
                insideBracket = True
                return '('
            insideBracket = False
            return ')'

        # Annotations here are based on the historical standards used by Germany in WW2
        # See http://users.telenet.be/d.rijmenants/Enigma%20Sim%20Manual.pdf for more details.

        # Merge 5-letter blocks, separate words by X
        text = text.replace(' ', '')
        text = re.sub(r'(?<!X)X(?!X)', ' ', text)

        # Conversion of numbers
        text = text.replace('NULL', '0')
        text = text.replace('CENTA', '00')
        text = text.replace('MILLE', '000')
        text = text.replace('MYRIA', '0000')
        text = text.replace('EINZ', '1')
        text = text.replace('EINS', '1')
        text = text.replace('ZWO', '2')
        text = text.replace('DREI', '3')
        text = text.replace('VIER', '4')
        text = text.replace('FUNF', '5')
        text = text.replace('SEQS', '6')
        text = text.replace('SIEBEN', '7')
        text = text.replace('AQT', '8')
        text = text.replace('NEUN', '9')

        # Conversion of abbreviations/code
        text = text.replace('Q', 'CH')
        text = text.replace('UD', '?')
        text = text.replace('XX', ':')
        text = text.replace('YY', '-')
        text = text.replace('J', '*')
        text = re.sub(r'KK', bracketChooser, text) # Convert KK...KK into (...)
        text = re.sub(r'\bK\b|\bK^(\d|\D|\W|\w)', '.', text) # Convert single K into a fullstop.
        text = re.sub(r'\s[.]|\s[.]', '.', text) # Remove incorrect spaces before full stops
        text = re.sub(r'\b(\D+)\1\b', r'\1', text) # Remove duplicate words
        
        return text
    
    # Convert numbers into German enigma format.
    # @param num The number to convert. Can either be in number format, or string format.
    # @return A string containing the number, formatted for transmission by Enigma.
    @staticmethod
    def formatNum(num):
        if (not isinstance(num, str)):
            num = str(num) # We're largely using regex to convert it.
        num = num.replace('0000', 'MYRIA')
        num = num.replace('000', 'MILLE')
        num = num.replace('00', 'CENTA')
        num = num.replace('0', 'NULL')
        num = num.replace('9', 'NEUN')
        num = num.replace('8', 'AQT')
        num = num.replace('7', 'SIEBEN')
        num = num.replace('6', 'SEQS')
        num = num.replace('5', 'FUNF')
        num = num.replace('4', 'VIER')
        num = num.replace('3', 'DREI')
        num = num.replace('2', 'ZWO')
        num = num.replace('1', 'EINS')

        # Convert separators
        num = num.replace(':', 'XX')
        
        return num
    
    # Formats a string into 5-letter segments.
    # @param string The string to format.
    # @return A formatted string, in 5 letter segments. If the last segment is less than 5 letters, it will be padded with spaces.
    @staticmethod
    def formatStr(string):
        if (not isinstance(string, str)):
            string = str(string)
        string = re.sub(r'\s', '', string)
        string = re.sub(r'(.{5})', r'\1 ', string)
        if (not (len(string) % 6 == 0)):
            string += ' ' * (5 - (len(string) % 6))
        
        return string
    
    # Formats a string by converting special characters to their German Enigma annotation equivalent.
    # @param text The string to encode.
    # @return An encoded string.
    @staticmethod
    def convertSpecialChar(text):
        if (not isinstance(text, str)):
            text = str(text)
            return text
        text = text.replace('CH', 'Q')
        text = text.replace('?', 'UD')
        text = text.replace(':', 'XX')
        text = text.replace('-', 'YY')
        text = text.replace('*', 'J')
        text = text.replace('.', 'K')
        text = text.replace(' ', 'X')
        
        return text