import json

# Load dictionary
pronunciation_dict = {}

def load_dictionary():
    global pronunciation_dict
    with open('ipa_dict.json', 'r', encoding='utf-8') as file:
        pronunciation_dict = json.load(file)

load_dictionary()

def get_pronunciation(word: str) -> str:
    return "".join(pronunciation_dict.get(letter, "") if letter != " " else " " for letter in word)
