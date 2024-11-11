'''NOTE READ THE README FIRST'''

import string

# Initialize the deck with values from 1 to 54 (including jokers as 53 and 54)
def initialise_deck():
    deck = list(range(1, 55))
    return deck

# Convert a text message to numerical values (A=1, B=2, ..., Z=26)
def text_to_numbers(text):
    text = text.upper()
    return [ord(char) - ord('A') + 1 for char in text if char in string.ascii_uppercase]

# Convert a list of numbers back to text (1=A, 2=B, ..., 26=Z)
def numbers_to_text(numbers):
    return ''.join(chr((num - 1) % 26 + ord('A')) for num in numbers)

# Move the "A" joker (53) one step down the deck
def move_joker_a(deck):
    joker_a_index = deck.index(53)
    deck.insert((joker_a_index + 1) % len(deck), deck.pop(joker_a_index))

# Move the "B" joker (54) two steps down the deck
def move_joker_b(deck):
    joker_b_index = deck.index(54)
    deck.insert((joker_b_index + 2) % len(deck), deck.pop(joker_b_index))

# Perform a triple cut around the two jokers, rearranging the deck
def triple_cut(deck):
    joker_a_index = deck.index(53)
    joker_b_index = deck.index(54)
    if joker_a_index > joker_b_index:
        joker_a_index, joker_b_index = joker_b_index, joker_a_index  # swap positions in deck
    deck = deck[joker_b_index+1:] + \
        deck[joker_a_index:joker_b_index+1] + \
        deck[:joker_a_index]  # redefine deck again
    return deck

# Perform a count cut based on the value of the bottom card (but ignore jokers for count)
def count_cut(deck):
    bottom_value = deck[-1]
    if bottom_value in [53, 54]:  # Treat jokers as 53 for simplicity
        bottom_value = 53
    deck = deck[bottom_value:-1] + deck[:bottom_value] + [deck[-1]]
    return deck

# Get a keystream value based on the top card's value
def get_keystream_value(deck):
    top_value = deck[0]
    if top_value in [53, 54]:  # If the top card is a joker, use 52 instead
        top_value = 52
    return deck[top_value]

# main function to generate keystream value
def generate_keystream(deck, length):
    keystream = []
    for _ in range(length):
        move_joker_a(deck)
        move_joker_b(deck)
        deck = triple_cut(deck)
        deck = count_cut(deck)
        keystream_value = get_keystream_value(deck)
        # If the keystream value is a joker, repeat the process
        while keystream_value in [53, 54]:
            move_joker_a(deck)
            move_joker_b(deck)
            deck = triple_cut(deck)
            deck = count_cut(deck)
            keystream_value = get_keystream_value(deck)
        keystream.append(keystream_value)
    return keystream

# Encrypt a message by adding keystream values to message letters


def encrypt(message, deck):
    # needs to be converted to num for keystream
    message_numbers = text_to_numbers(message)
    keystream = generate_keystream(deck, len(message_numbers))
    encrypted_numbers = [(m + k - 1) % 26 + 1 for m,
                         k in zip(message_numbers, keystream)]
    return numbers_to_text(encrypted_numbers)

# Decrypt a ciphertext by subtracting keystream values from ciphertext letters


def decrypt(ciphertext, deck):
    ciphertext_numbers = text_to_numbers(ciphertext)
    keystream = generate_keystream(deck, len(ciphertext_numbers))
    decrypted_numbers = [(c - k - 1) % 26 + 1 for c,
                         k in zip(ciphertext_numbers, keystream)]
    return numbers_to_text(decrypted_numbers)
