import random
from colorama import Fore, Back, Style
from tabulate import tabulate
import json, os

x = random.randint(10, 20)

vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

randomConsonant = random.choice(consonants)

def generateRandomVowel():
    return random.choice(vowels)

def generateRandomConsonant():
    return random.choice(consonants)

def randomWordGenerator():
    return generateRandomConsonant() + generateRandomVowel()

def complexRandomWordGenerator():
    return generateRandomConsonant() + generateRandomVowel() + generateRandomConsonant()

def moreComplexRandomWordGenerator():
    word = ''

    x = random.randint(1, 3)
    y = random.randint(1, 3)
    
    for i in range(x):
        word += generateRandomConsonant()
    for i in range(y):
        word += generateRandomVowel()

    return word

def skipWordGenerator(skipLength):
    word = ''
    while len(word) < skipLength:
        word += complexRandomWordGenerator()
    return word[:skipLength]

def createRandomWord(length):
    word = ''
    while len(word) < length:
        word += complexRandomWordGenerator()
    return word[:length] 

x = random.randint(4, 8)
skipLength = 2

# GLOBALS

cipher = {}

def noMenu():
    choice = input(Fore.GREEN + "$: ")
    if choice == '1':
        browse()
    elif choice == '2':
        create()
    elif choice == '3':
        options()
    else:
        print(Fore.RED + "Invalid choice, please try again.")
        noMenu()

def cipherCount():
    with open('ciphers.json', 'r') as f:

        if f.read() == '':
            return 0
        jsonCipher = json.load(f)
        return len(jsonCipher)

def createCipher(name, complexity):
    try:
        with open('ciphers.json', 'r') as f:
            jsonCipher = json.load(f)
    except FileNotFoundError:
        jsonCipher = {}
    except json.JSONDecodeError:
        jsonCipher = {}

    if name in jsonCipher:
        print(Fore.RED + "Cipher already exists!")
        return
    
    data = {
        "ciphername": name,
        "complexity": complexity
    }

    with open(f'{name}.json', 'w') as f:
        json.dump(data, f, indent=4)

    jsonCipher[data["ciphername"]] = name
    jsonCipher[data["complexity"]] = complexity

    with open('ciphers.json', 'w') as f:
        json.dump(jsonCipher, f, indent=4)

def readCipher(cipherName):
    with open('ciphers.json', 'r') as f:
        jsonCipher = json.load(f)
        return jsonCipher[cipherName]
    
def cipherBrowser(cipherName):
    # List ciphers using tabulate
    with open(f'{cipherName}.json', 'r') as f:
        jsonCipher = json.load(f)

        if jsonCipher == {}:
            print(Fore.RED + "No ciphers found!")

        headers = ["Key", "Value"]
        table = []
        for cipherName, complexity in jsonCipher.items():
            table.append([cipherName, complexity])

        print(Fore.GREEN + tabulate(table, headers, tablefmt="fancy_grid"))

        noMenu()

def manageCipher(cipherName):
    with open(f'{cipherName}.json', 'r') as f:
        jsonCipher = json.load(f)
        
        headers = ["Key", "Value"]
        table = []
        for key, value in jsonCipher.items():
            table.append([key, value])

        print(Fore.GREEN + tabulate(table, headers, tablefmt="fancy_grid"))

        print(Fore.GREEN + "1. Change name")
        print(Fore.GREEN + "2. Change complexity")
        print(Fore.GREEN + "3. Delete cipher")
        print(Fore.GREEN + "4. Back")
        choice = input(Fore.GREEN + "$: ")

        if choice == '1':
            newCipherName = input(Fore.GREEN + "Enter new name: ")
            jsonCipher['ciphername'] = newCipherName
            with open(f'{cipherName}.json', 'w') as f:
                json.dump(jsonCipher, f, indent=4)
            manageCipher(cipherName)
        elif choice == '2':
            newComplexity = input(Fore.GREEN + "Enter new complexity: ")
            jsonCipher['complexity'] = newComplexity
            with open(f'{cipherName}.json', 'w') as f:
                json.dump(jsonCipher, f, indent=4)
            manageCipher(cipherName)
        elif choice == '3':
            with open('ciphers.json', 'r') as f:
                jsonCipher = json.load(f)

                if jsonCipher == {}:
                    print(Fore.RED + "No ciphers found!")

                headers = ["Key", "Value"]
                table = []
                for cipherName, complexity in jsonCipher.items():
                    table.append([cipherName, complexity])

                print(Fore.GREEN + tabulate(table, headers, tablefmt="fancy_grid"))

                deleteCipher = input(Fore.GREEN + "Enter cipher name to delete: ")

                if deleteCipher in jsonCipher:
                    del jsonCipher[deleteCipher]

                    with open('ciphers.json', 'w') as f:
                        json.dump(jsonCipher, f, indent=4)

                    print(Fore.GREEN + "Cipher deleted successfully!")
                    manageCipher(cipherName)
                else:
                    print(Fore.RED + "Cipher doesn't exist!")
                    manageCipher(cipherName)
        elif choice == '4':
            browse()
        else:
            print(Fore.RED + "Invalid choice, please try again.")
            manageCipher(cipherName)
        
        dictionary = jsonCipher[cipherName]
        return dictionary

def main():
    ascii_art = r"""
_________ .__       .__                 .____    .__        __    
\_   ___ \|__|_____ |  |__   ___________|    |   |__| ____ |  | __
/    \  \/|  \____ \|  |  \_/ __ \_  __ \    |   |  |/    \|  |/ /
\     \___|  |  |_> >   Y  \  ___/|  | \/    |___|  |   |  \    < 
 \______  /__|   __/|___|  /\___  >__|  |_______ \__|___|  /__|_ \
        \/   |__|        \/     \/              \/       \/     \/

                        Made by: Giorgi Mirzashvili aka Grigol Mersadze
"""
    print(Fore.YELLOW + ascii_art)
    print(Fore.GREEN + "1. Browse your ciphers")
    print(Fore.GREEN + "2. Create cipher")
    print(Fore.GREEN + "3. Options")

    choice = input(Fore.GREEN + "$: ")
    if choice == '1':
        browse()
    elif choice == '2':
        create()
    elif choice == '3':
        options()
    else:
        print(Fore.RED + "Invalid choice, please try again.")
        main()


def browse():
    files = os.listdir('.')
    json_files = [file for file in files if file.endswith('.json')]

    # Tabulate the JSON files
    headers = ["File", "Name", "Complexity"]
    table = []
    for file in json_files:
        # Load the JSON file and get only name and complexity per row of this table, no duplicate rows of same json
        with open(file, 'r') as f:
            json_file = json.load(f)
            name = json_file['ciphername']
            complexity = json_file['complexity']
            table.append([file, name, complexity])

    print(Fore.GREEN + tabulate(table, headers, tablefmt="fancy_grid"))
    chosenCipher = input(Fore.GREEN + "$: ")

    if chosenCipher + '.json' not in json_files:
        print(Fore.RED + "Invalid choice, please try again.")
        browse()
    elif chosenCipher + '.json' in json_files:
        manageCipher(chosenCipher)
    elif chosenCipher == '1' or chosenCipher == '2' or chosenCipher == '3':
        noMenu()


def create():
    print(Fore.GREEN, "1. Choose a name for cipher: ")
    name = input()
    print(Fore.GREEN, "2. Choose a complexity of your cipher: (1 - 3) ")
    complexity = input()

    if complexity not in ['1', '2', '3']:
        print(Fore.RED + "Invalid choice, please try again.")
        create()

    createCipher(name, complexity)


def options():
    pass

main()