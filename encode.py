import random
import database

def create_dictionary():
    alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
    digits = '1 2 3 4 5 6 7 8 9 0'
    alpha_low = alphabet.split(" ")
    alpha_high = alphabet.upper().split(" ")
    digits_list = digits.split(" ")
    dictionary = []
    dictionary.extend(alpha_low)
    dictionary.extend(alpha_high)
    dictionary.extend(digits_list)
    return dictionary


def create_short_url():
    letters = create_dictionary()
    new_url = ''
    for i in range(8):
        random_ind = int(random.random() * len(letters))
        random_ch = letters[random_ind]
        new_url = new_url + random_ch
    return new_url


def encode_url(url):
    if database.is_exist(url):
        return database.local_storage[url]
    new_url = create_short_url()
    return new_url

