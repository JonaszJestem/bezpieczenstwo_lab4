cryptograms = []

cryptogram_number = 1
frequent_letters = [" ", "I", "E", "A", "O", "N", "Z", "R", "S", "W", "Y", "C", "T", "D", "K", "P", "M", "Ł", "J", "L",
                    "U",
                    "B", "G", "H", "Ę", "Ż", "Ó", "Ą", "Ś", "Ć", "F", "Ń", "Ź", "X"]

# Wczytywanie wszystkich kryptogramów do listy cryptograms
try:
    while True:
        cryptogram_file = open(str(cryptogram_number))
        content = cryptogram_file.read()
        content = content.replace(" ", "")
        cryptograms.append(content)
        cryptogram_number += 1
except IOError:
    pass

# Maksymalna liczba bajtów w cryptogramie
max_number_of_bytes = len(max(cryptograms, key=len)) // 8
number_of_cryptograms = len(cryptograms)
# Lista ktora zawiera licznik kiedy xorowanie dało wynik zaczynający się od "01".
# Jeżeli licznik wysoki - prawdopodobnie jest to spacja w danym kryptogramie
counting_probable_space = [[0 for x in range(max_number_of_bytes)] for y in range(number_of_cryptograms)]


def get_shorter_cryptogram():
    return min(len(cryptograms[first_index]), len(cryptograms[second_index]))


def get_xorred_byte(first, second):
    second = int(second, 2)
    first = int(first, 2)
    return bin(first ^ second)[2:].rjust(8, "0")


# Xorujemy każdy kryptogram z każdym, jezeli xorowany bajt zaczyna się od 01
# to zwiększamy odpowidni licznik na odpowiadajacych bajtach.
for first_index in range(number_of_cryptograms):
    for second_index in range(first_index + 1, number_of_cryptograms):
        longest = get_shorter_cryptogram()

        for i in range(0, longest, 8):
            xorred = get_xorred_byte(cryptograms[first_index][i:i + 8], cryptograms[second_index][i:i + 8])
            if xorred.startswith("01"):
                counting_probable_space[first_index][i // 8] += 1
                counting_probable_space[second_index][i // 8] += 1

# Tutaj bedzie przechowywany klucz wraz z prawdopodobnymi subkluczami (te bajty które miały największy licznik)
key = [[0, set()] for x in range(max_number_of_bytes)]

for current_cryptogram in range(number_of_cryptograms):
    for current_byte in range(max_number_of_bytes):
        # print(temp[current_cryptogram][current_byte], " ", end='')

        # Jeżeli licznik jest większy to zastąp istniejący subklucz tym tutaj
        if counting_probable_space[current_cryptogram][current_byte] > key[current_byte][0]:
            key[current_byte][1] = set()
            key[current_byte][1].add(cryptograms[current_cryptogram][current_byte * 8:current_byte * 8 + 8])
            key[current_byte][0] = counting_probable_space[current_cryptogram][current_byte]
        # Jeżeli licznik jest równy to dodaj to subkluczy
        elif counting_probable_space[current_cryptogram][current_byte] == key[current_byte][0]:
            key[current_byte][1].add(cryptograms[current_cryptogram][current_byte * 8:current_byte * 8 + 8])
    # print()

end_key = []

#Odczytaj zaszyfrowany tekst
secret = open("to_decipher").read().replace(" ", "")

for i in range(0, len(secret), 8):
    #Dla kazdych 8 bitów zaszyfrowanej wiadomosci
    secret_part = int(secret[i:i + 8], 2)

    end_char = ""
    most_probable = 32

    subkey = key[i // 8]
    #Znajdz najbardziej prawdopodobny znak dla kazdego subklucza ktory jest wynikiem secret_part XOR subklucz
    while subkey[1]:
        probable_key = int(subkey[1].pop(), 2) ^ 32
        probable_char = chr(probable_key ^ secret_part)
        if probable_char.upper() in frequent_letters and frequent_letters.index(probable_char.upper()) < most_probable:
            end_char = probable_char
            most_probable = frequent_letters.index(probable_char.upper())

    print(end_char, end='')
print()
print("Oryginalny tekst:")
print("Wojewódzki o Krakowie: \"Prowincja magic plejs pomimo że prowincja\" - napisał pod zdjęciem z Krakowa.")
