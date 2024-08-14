import random
from colorama import init, Fore, Back, Style
from tabulate import tabulate
import json, os

init()

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

def createRandomWord(length):
    word = ''
    while len(word) < length:
        if length == 4:
            word += randomWordGenerator()
        elif length == 6:
            word += complexRandomWordGenerator()
        elif length == 8:
            word += moreComplexRandomWordGenerator()
        else:
            print(Fore.RED + "Invalid choice, please try again. @lengthError")
            noMenu()

    return word[:length]

def generateRandomWord(complexity):
    if complexity == 1:
        return createRandomWord(4)
    elif complexity == 2:
        return createRandomWord(6)
    elif complexity == 3:
        return createRandomWord(8)
    else:
        print(Fore.RED + "Invalid choice, please try again. @complexityError")
        noMenu()

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
        print(Fore.RED + "Invalid choice, please try again. @choiceErrorNoMenu")
        noMenu()

def createCipher(name, complexity):
    try:
        with open(f'{name}.json', 'r') as f:
            jsonCipher = json.load(f)
    except FileNotFoundError:
        jsonCipher = {}
    except json.JSONDecodeError:
        jsonCipher = {}

    if name in jsonCipher:
        print(Fore.RED + "Cipher already exists!")
        return
    
    jsonCipher = {
        'cipherName': name,
        'cipherComplexity': complexity
    }

    jsonCipher["cipherName"] = name
    jsonCipher["cipherComplexity"] = complexity

    with open(f'{name}.json', 'w') as f:
        json.dump(jsonCipher, f, indent=4)

    with open(f'{name}.json', 'w') as f:
        json.dump(jsonCipher, f, indent=4)

    noMenu()

def readCipher(cipherName):
    with open(f'{cipherName}.json', 'r') as f:
        jsonCipher = json.load(f)
        return jsonCipher
    
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

def dictCreate(cipherName, complexity):
    cipher = readCipher(cipherName)

    print(Fore.GREEN + "Enter cipher name: ('back' to go back) ")
    enterWord = input(Fore.GREEN + "$: ")
    enterWord = enterWord.lower()

    if enterWord in cipher:
        print(Fore.RED + "Such word already exists!")
    elif enterWord == '':
        print(Fore.RED + "Invalid choice, please try again. @valueEmptyError")
        noMenu()
    elif enterWord == 'back':
        manageCipher(cipherName)
    elif enterWord != '' and enterWord not in cipher:
        generatedValue = generateRandomWord(int(complexity))  # Store the generated word
        if generatedValue in cipher.values():
            print(Fore.RED + "Value already exists!")
            manageCipher(cipherName)
        else:
            print(Fore.GREEN + "Generated Value: " + Fore.CYAN + generatedValue + Fore.GREEN + " | Writing value..." )
            cipher[enterWord] = generatedValue  # Use the stored value
            with open(f'{cipherName}.json', 'w') as f:
                json.dump(cipher, f, indent=4)
    else:
        print(Fore.RED + "Invalid choice, please try again. @elseError")

    dictCreate(cipherName, complexity)


def dictRemove(cipherName):
    cipher = readCipher(cipherName)

    while True:
        print(Fore.GREEN + "Enter cipher name to remove: ('back' to go back)")
        enterWord = input(Fore.GREEN + "$: ").lower()

        if enterWord == 'back':
            break  # Exit the loop and function
        elif enterWord in ('', 'ciphername', 'complexity'):
            print(Fore.RED + "Invalid choice, please try again. @valueEmptyErrorRemove")
        elif enterWord not in cipher:
            print(Fore.RED + "Such word doesn't exist!")
        else:
            # Remove the word from the cipher
            cipher.pop(enterWord)
            
            # Write the updated cipher back to the same JSON file
            with open(f'{cipherName}.json', 'w') as f:
                json.dump(cipher, f, indent=4)
            print(Fore.GREEN + f"Word '{enterWord}' successfully removed!")
        
    # When the loop exits, return to manageCipher or previous menu
    manageCipher(cipherName)

def dictReassign(cipherName, complexity):
    cipher = readCipher(cipherName)

    while True:
        print(Fore.GREEN + "Enter word to reassign: ('back' to go back)")
        enterWord = input(Fore.GREEN + "$: ").lower()

        if enterWord == 'back':
            break  # Exit the loop and function
        elif enterWord in ('', 'ciphername', 'complexity'):
            print(Fore.RED + "Invalid choice, please try again. @valueEmptyErrorReassign")
        elif enterWord not in cipher:
            print(Fore.RED + "Such word doesn't exist!")
        else:
            # Remove the word from the cipher
            cipher.pop(enterWord)
            # Generate new value for word
            generatedValue = generateRandomWord(int(complexity))  # Store the generated word

            # Check if there's already same value in the cipher
            if generatedValue in cipher.values():
                print(Fore.RED + "Value already exists!")
                manageCipher(cipherName)
            else:
                print(Fore.GREEN + "Generated Value: " + Fore.CYAN + generatedValue + Fore.GREEN + " | Writing value..." )
                cipher[enterWord] = generatedValue  # Use the stored value
                with open(f'{cipherName}.json', 'w') as f:
                    json.dump(cipher, f, indent=4)
                print(Fore.GREEN + f"Word '{enterWord}' successfully reassigned!")

    # When the loop exits, return to manageCipher or previous menu
    manageCipher(cipherName)

def advancedOptions(cipherName):
    # Bulk functions like bulk modification, deletion or creation
    # Search functions, filtering functions, etc.
    # 2 way encryption, decryption, etc.
    pass

def translate(cipherName):
    print(Fore.GREEN + "Encryption (e) or Decryption (d): ('back' to go back) ")
    enterWord = input(Fore.GREEN + "$: ")
    enterWord = enterWord.lower()

    if enterWord == 'back':
        manageCipher(cipherName)

    if enterWord != 'e' and enterWord != 'd':
        print(Fore.RED + "Invalid choice, please try again. @elseError")
        translate(cipherName)

    if enterWord == 'd':
        decrypt(cipherName)
    
    if enterWord == 'e':
        print(Fore.GREEN + "Enter sentence to translate: ")
        sentence = input(Fore.GREEN + "$: ")

        if sentence == '':
            print(Fore.RED + "Invalid choice, please try again. @valueEmptyError")
            noMenu()

        with open(f'{cipherName}.json', 'r') as f:
            jsonCipher = json.load(f)
            for key, value in jsonCipher.items():
                sentence = sentence.replace(key, value)
            print(Fore.GREEN + sentence)

    noMenu()


def decrypt(cipherName):
    print(Fore.GREEN + "Enter sentence to decrypt: ")
    sentence = input(Fore.GREEN + "$: ")

    if sentence == '':
        print(Fore.RED + "Invalid choice, please try again. @valueEmptyError")
        noMenu()

    with open(f'{cipherName}.json', 'r') as f:
        jsonCipher = json.load(f)
        for key, value in jsonCipher.items():
            sentence = sentence.replace(value, key)
        print(Fore.GREEN + sentence)

    noMenu()
    

def manageCipher(cipherName):
    with open(f'{cipherName}.json', 'r') as f:
        jsonCipher = json.load(f)
        
        headers = ["Key", "Value"]
        table = []
        for key, value in jsonCipher.items():
            table.append([key, value])

        print(Fore.GREEN + tabulate(table, headers, tablefmt="fancy_grid"))

        print(Fore.YELLOW + "To open translation menu, type 'T'")

        print(Fore.GREEN + "1. Change name")
        print(Fore.GREEN + "2. Change complexity")
        print(Fore.GREEN + "3. Add new words to cipher")
        print(Fore.GREEN + "4. Remove words from cipher")
        print(Fore.GREEN + "5. Reassign words in cipher")
        print(Fore.GREEN + "6. Delete cipher")
        print(Fore.GREEN + "7. Back")
        print(Fore.GREEN + "8. Advanced Options")
        choice = input(Fore.GREEN + "$: ")

        if choice == '1':
            newCipherName = input(Fore.GREEN + "Enter new name: ")
            jsonCipher['ciphername'] = newCipherName
            # Also change file name
            os.rename(f'{cipherName}.json', f'{newCipherName}.json')
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
            dictCreate(cipherName, jsonCipher['cipherComplexity'])
        elif choice == '4':
            dictRemove(cipherName)
        elif choice == '5':
            dictReassign(cipherName, jsonCipher['cipherComplexity'])
        elif choice == '6':
            with open(f'{cipherName}.json', 'r') as f:
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

                    with open(f'{cipherName}.json', 'w') as f:
                        json.dump(jsonCipher, f, indent=4)

                    print(Fore.GREEN + "Cipher deleted successfully!")
                    manageCipher(cipherName)
                else:
                    print(Fore.RED + "Cipher doesn't exist!")
                    manageCipher(cipherName)
        elif choice == '7':
            browse()
        elif choice == '8':
            advancedOptions(cipherName)
        elif choice == 'T':
            translate(cipherName)
        else:
            print(Fore.RED + "Invalid choice, please try again. @cipherManagementError")
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

                        Made by: Grigol Mersadze
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
        print(Fore.RED + "Invalid choice, please try again. @mainError")
        noMenu()


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
        print(Fore.RED + "Invalid choice, please try again. @browserInvalidChoiceError")
        main()
    elif chosenCipher + '.json' in json_files:
        manageCipher(chosenCipher)
    elif chosenCipher == '1':
        create()
    elif chosenCipher == '2':
        browse()
    elif chosenCipher == '3':
        options()
    else:
        print(Fore.RED + "Invalid choice, please try again. @browserElseError")
        main()

def create():
    print(Fore.GREEN, "1. Choose a name for cipher: ")
    name = input()

    if name == '':
        print(Fore.RED + "Invalid choice, please try again. @nameEmptyError")
        create()
    elif name == 'menu':
        main()

    print(Fore.GREEN, "2. Choose a complexity of your cipher: (1 - 3) ")
    complexity = input()

    if complexity not in ['1', '2', '3']:
        print(Fore.RED + "Invalid choice, please try again. @creationError")
        create()

    createCipher(name, complexity)


def options():
    noMenu()

main()