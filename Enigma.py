import itertools
import threading
import numpy
from datetime import datetime
alph = "abcdefghijklmnopqrstuvwxyz"




def isLetter(char):
    return (char in alph)


def countLetters(text):
    count = 0
    for i in text:
        if (isLetter(i)):
            count += 1
    return count


def getIOC(text):
    letterCounts = []

    # Loop through each letter in the alphabet - count number of times it appears
    for i in range(len(alph)):
        count = 0
        for j in text:
            if j == alph[i]:
                count += 1
        letterCounts.append(count)

    # Loop through all letter counts, applying the calculation (the sigma part)
    total = 0
    for i in range(len(letterCounts)):
        ni = letterCounts[i]
        total += ni * (ni - 1)

    N = countLetters(text)
    c = 26.0  # Number of letters in the alphabet
    total = float(total) / ((N * (N - 1)))
    return total


chargrid = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def chartoint(character):
    return chargrid.index(character) % 26


def inttochar(integer):
    return chargrid[integer]


def classicprint(string):
    for i in range(len(string)):
        print(string[i], end="")
        if ((i + 1) % 5 == 0):
            print(" ", end="")


class Enigma:
    def __init__(self, w1, position1, w2, position2, w3, position3, umkehrwalze, steckbrettpaare=[]):
        self.walzen = [Walze(w1, chartoint(position1)), Walze(w2, chartoint(position2)),
                       Walze(w3, chartoint(position3)), Walze(umkehrwalze, 0)]
        self.steckbrett = Steckbrett(steckbrettpaare)

    def walzenschalten(self):
        if (self.walzen[0].position + 1 in self.walzen[0].übertragskerbe):
            self.walzen[1].position = (self.walzen[1].position + 1) % 26
        else:
            if (self.walzen[1].position + 1 in self.walzen[1].übertragskerbe):
                self.walzen[1].position = (self.walzen[1].position + 1) % 26
        if (self.walzen[1].position + 1 in self.walzen[1].übertragskerbe):
            self.walzen[2].position = (self.walzen[2].position + 1) % 26
        self.walzen[0].position = (self.walzen[0].position + 1) % 26

    def schlüsselnChar(self, integer):
        self.walzenschalten()
        curint = integer
        curint = (self.steckbrett.verdrahtung[curint] - 1) % 26
        for i in range(3):
            curint = (self.walzen[i].verdrahtung[(curint + self.walzen[i].position) % 26] - 1 - self.walzen[
                i].position) % 26
        curint = self.walzen[3].verdrahtung[curint] - 1
        for i in range(3):
            curint = (self.walzen[2 - i].verdrahtung.index((curint + self.walzen[2 - i].position) % 26 + 1) -
                      self.walzen[2 - i].position) % 26
        curint = (self.steckbrett.verdrahtung.index(curint + 1)) % 26
        return curint

    def schlüsselnstr(self, string):
        newstring = ""
        for i in string:
            if (i in chargrid):
                integer = chartoint(i)
                newstring += inttochar(self.schlüsselnChar(integer))
        return newstring


class Steckbrett:
    def __init__(self, paare):
        self.verdrahtung = [i + 1 for i in range(26)]
        for i in range(int(len(paare) / 2)):
            self.verdrahtung[chartoint(paare[2 * i])] = chartoint(paare[2 * i + 1]) + 1
            self.verdrahtung[chartoint(paare[2 * i + 1])] = chartoint(paare[2 * i]) + 1


class Walze:
    def __init__(self, nummer, position):
        self.position = position
        if (nummer == '1'):
            self.verdrahtung = [5, 11, 13, 6, 12, 7, 4, 17, 22, 26, 14, 20, 15, 23, 25, 8, 24, 21, 19, 16, 1, 9, 2, 18,
                                3, 10]
            self.übertragskerbe = [17]

        if (nummer == '2'):
            self.verdrahtung = [1, 10, 4, 11, 19, 9, 18, 21, 24, 2, 12, 8, 23, 20, 13, 3, 17, 7, 26, 14, 16, 25, 6, 22,
                                15, 5]
            self.übertragskerbe = [5]

        if (nummer == '3'):
            self.verdrahtung = [2, 4, 6, 8, 10, 12, 3, 16, 18, 20, 24, 22, 26, 14, 25, 5, 9, 23, 7, 1, 11, 13, 21, 19,
                                17, 15]
            self.übertragskerbe = [22]

        if (nummer == '4'):
            self.verdrahtung = [5, 19, 15, 22, 16, 26, 10, 1, 25, 17, 21, 9, 18, 8, 24, 12, 14, 6, 20, 7, 11, 4, 3, 13,
                                23, 2]
            self.übertragskerbe = [10]

        if (nummer == '5'):
            self.verdrahtung = [22, 26, 2, 18, 7, 9, 20, 25, 21, 16, 19, 4, 14, 8, 12, 24, 1, 23, 13, 10, 17, 15, 6, 5,
                                3, 11]
            self.übertragskerbe = [26]

        if (nummer == '6'):
            self.verdrahtung = [10, 16, 7, 22, 15, 21, 13, 6, 25, 17, 2, 5, 14, 8, 26, 18, 4, 11, 1, 19, 24, 12, 9, 3,
                                20, 23]
            self.übertragskerbe = [13, 26]  # zwei Kerben!

        if (nummer == '7'):
            self.verdrahtung = [14, 26, 10, 8, 7, 18, 3, 24, 13, 25, 19, 23, 2, 15, 21, 6, 1, 9, 22, 12, 16, 5, 11, 17,
                                4, 20]
            self.übertragskerbe = [13, 26]  # zwei Kerben!

        if (nummer == '8'):
            self.verdrahtung = [6, 11, 17, 8, 20, 12, 24, 15, 3, 2, 10, 19, 16, 4, 26, 18, 1, 13, 5, 23, 14, 9, 21, 25,
                                7, 22]
            self.übertragskerbe = [13, 26]  # zwei Kerben!

        if (nummer == 'A'):
            self.verdrahtung = [5, 10, 13, 26, 1, 12, 25, 24, 22, 2, 23, 6, 3, 18, 17, 21, 15, 14, 20, 19, 16, 9, 11, 8,
                                7, 4]
        if (nummer == 'B'):
            self.verdrahtung = [25, 18, 21, 8, 17, 19, 12, 4, 16, 24, 14, 7, 15, 11, 13, 9, 5, 2, 6, 26, 3, 23, 22, 10,
                                1, 20]
        if (nummer == 'C'):
            self.verdrahtung = [6, 22, 16, 10, 9, 1, 15, 25, 5, 4, 18, 26, 24, 23, 7, 3, 20, 11, 21, 17, 19, 2, 14, 13,
                                8, 12]


Enigma1 = Enigma("1", "F", "4", "Z", "2", "A", "A")
output = Enigma1.schlüsselnstr(
    "Dies ist ein ganz normaler Text in deutsher Sprache")
ciphertext = output
walzen = ["1", "2", "3", "4", "5", "6", "7", "8"]
positionen = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ukw = ["A", "B", "C", "D"]

alle_walzen_kombinationen = numpy.asarray(list(itertools.permutations(walzen, 3)))
alle_pos_kombinationen = numpy.asarray(list(itertools.permutations(positionen, 3)))



def print_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def decryptPart(walzen_kombination,pos_kombination, ukw):
    print_time()
    for ukw in ukw:
        for walzen_kombination in walzen_kombination:
            for pos_kombination in itertools.permutations(positionen, 3):
                decryptedText = Enigma(walzen_kombination[0], pos_kombination[0], walzen_kombination[1],
                                       pos_kombination[1],
                                       walzen_kombination[2], pos_kombination[2], ukw).schlüsselnstr(ciphertext)
                ioc = getIOC(decryptedText.lower())

                if ioc > 0.09:

                    print(
                        f"Walzen: {walzen_kombination[0]}({pos_kombination[0]}), {walzen_kombination[1]}({pos_kombination[1]}), {walzen_kombination[2]}({pos_kombination[2]}) : {ioc}")
                    print(decryptedText)
                    print_time()
                    """"
                    text = walzen_kombination[0] + ";" + pos_kombination[0] + ";" + walzen_kombination[1] + ";" + \
                           pos_kombination[1] + ";" + walzen_kombination[2] + ";" + pos_kombination[
                               2] + ";" + ukw + ";" + str(ioc) + ";" + decryptedText + "\n"
                    
                    file.write(text)
                                """
    print("finished")


anz_threads = 100


walzen_kombinationen_sublists = numpy.array_split(alle_walzen_kombinationen, anz_threads)
for e in walzen_kombinationen_sublists:
    x = threading.Thread(target=decryptPart, args=(e,alle_pos_kombinationen, ukw))
    x.start()
    print(x.name + "started")
