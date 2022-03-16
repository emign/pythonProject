# Title: IOC Calculator
# Author: William Banks
# Description: Calculator for finding the IOC (Index Of Coincidence) of a piece of text

# Formula for IOC: <https://en.wikipedia.org/wiki/Index_of_coincidence>
# c * ((n_a/N * (n_a - 1)/(N - 1)) + (n_b/N * (n_b - 1)/(N - 1)) + ... + (n_z/N * (n_z - 1)/(N - 1))
# Or as a summation:
# Sigma n_i(n_i - 1)/((N(N - 1))/c)
# Where:
# c is the normalising coefficient, 26 for English
# n_{letter} is the count of that letter
# n_i is the count for any letter
# N is the length of the text

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


text = input("Enter text:\n").lower()
total = getIOC(text)
print("IOC: " + str(total))
print("Normalised IOC: " + str(total * 26.0))
# In English, the standard normalised IOC is around 1.73
