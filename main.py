from EnigmaMachine import EnigmaMachine
from Util import Util

# Settings for Enigma Machine.
# Note ringSetting can be either numeric or alphabetical; both work fine.
# For more examples of Enigma encrypted messages, see http://users.telenet.be/d.rijmenants/Enigma%20Sim%20Manual.pdf

encodeFlag       = False
rotorOrder       = ['I II V']
ringSetting      = ['06 22 14']
plugboardSetting = ['PO ML IU KJ NH YT GB VF RE DC']
trigramDecrypt   = ['EHZ TBS', 'EHZ TBS']
trigramEncrypt   = ['EHZ XWB', 'EHZ XWB']

cryptText        = ['ZBRIY IKTAY JJAQG ,BDIG PCHAE AUIQX AEEOB V    ','EBAFZ OYUXV LCITC CXPFG MIPSL NKLOF GRATU UTVNV QNTBA ']
plainText        = ['HELLO MY FRIEND, HOW ARE YOU TODAY?','MEET ME AT THE STATION AT 1830 HRS']

# rotorPos for decryption are typically defined by trigrams, not important.
# Only important for encryption.
rotorPos         = ['', '']

enigmaMachines = []
if (encodeFlag):
    cryptText = ''
    for i in range(0, len(plainText)):
        enigmaMachines.append(EnigmaMachine(rotorOrder[0], rotorPos[0], ringSetting[0], plugboardSetting[0]))
        trigramHeader = "\n = " + enigmaMachines[i].setTrigramSettingsEncrypt(trigramEncrypt[i]) + " = \n"
        currText = trigramHeader + "|" + Util.formatStr(enigmaMachines[i].input(Util.formatNum(Util.convertSpecialChar(plainText[i])))) + "|"
        cryptText += currText
    print(cryptText);
else:
    plainText = ''
    plainTextFormatted = ''
    for i in range(0, len(cryptText)):
        enigmaMachines.append(EnigmaMachine(rotorOrder[0], rotorPos[0], ringSetting[0], plugboardSetting[0]))
        enigmaMachines[i].setTrigramSettingsDecrypt(trigramDecrypt[i])
        currText = enigmaMachines[i].input(cryptText[i]) + "X"
        plainText += currText
        plainTextFormatted += Util.parseText(currText)
    print(plainText + "\n\n\n" + plainTextFormatted)