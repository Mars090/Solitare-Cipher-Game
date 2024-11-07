import time
import matplotlib.pyplot as plt
import string

# Solitaire Cipher Graph


def initialise_deck():
    return list(range(1, 55))


def text_to_numbers(text):
    text = text.upper()
    return [ord(char) - ord('A') + 1 for char in text if char in string.ascii_uppercase]


def numbers_to_text(numbers):
    return ''.join(chr((num - 1) % 26 + ord('A')) for num in numbers)


def move_joker_a(deck):
    joker_a_index = deck.index(53)
    deck.insert((joker_a_index + 1) % len(deck), deck.pop(joker_a_index))


def move_joker_b(deck):
    joker_b_index = deck.index(54)
    deck.insert((joker_b_index + 2) % len(deck), deck.pop(joker_b_index))


def triple_cut(deck):
    joker_a_index = deck.index(53)
    joker_b_index = deck.index(54)
    if joker_a_index > joker_b_index:
        joker_a_index, joker_b_index = joker_b_index, joker_a_index
    return deck[joker_b_index+1:] + deck[joker_a_index:joker_b_index+1] + deck[:joker_a_index]


def count_cut(deck):
    bottom_value = deck[-1]
    if bottom_value in [53, 54]:
        bottom_value = 53
    return deck[bottom_value:-1] + deck[:bottom_value] + [deck[-1]]


def get_keystream_value(deck):
    top_value = deck[0]
    if top_value in [53, 54]:
        top_value = 53
    return deck[top_value]


def generate_keystream(deck, length):
    keystream = []
    for _ in range(length):
        move_joker_a(deck)
        move_joker_b(deck)
        deck = triple_cut(deck)
        deck = count_cut(deck)
        keystream_value = get_keystream_value(deck)
        while keystream_value in [53, 54]:
            move_joker_a(deck)
            move_joker_b(deck)
            deck = triple_cut(deck)
            deck = count_cut(deck)
            keystream_value = get_keystream_value(deck)
        keystream.append(keystream_value)
    return keystream


def encrypt(message, deck):
    message_numbers = text_to_numbers(message)
    keystream = generate_keystream(deck, len(message_numbers))
    encrypted_numbers = [(m + k - 1) % 26 + 1 for m,
                         k in zip(message_numbers, keystream)]
    return numbers_to_text(encrypted_numbers)


def decrypt(ciphertext, deck):
    ciphertext_numbers = text_to_numbers(ciphertext)
    keystream = generate_keystream(deck, len(ciphertext_numbers))
    decrypted_numbers = [(c - k - 1) % 26 + 1 for c,
                         k in zip(ciphertext_numbers, keystream)]
    return numbers_to_text(decrypted_numbers)


# Measuring time for different input sizes
message_lengths = [10, 50, 100, 200, 300, 400, 500]
encryption_times = []
decryption_times = []

# ENCRYPTION ANALYSIS
for length in message_lengths:
    message = "A" * length  # create a sample message of 'A's with the specified length
    deck = initialise_deck()  # fresh deck for each run
    start_time = time.time()
    encrypt(message, deck)  # run encryption
    end_time = time.time()
    encryption_times.append(end_time - start_time)

# DECRYPTION ANALYSIS
for length in message_lengths:
    message = "A" * length  # create a sample message of 'A's with the specified length
    deck = initialise_deck()  # fresh deck for each run
    encrypted_message = encrypt(message, deck)  # First encrypt the message
    start_time = time.time()
    decrypt(encrypted_message, deck)  # run decryption
    end_time = time.time()
    decryption_times.append(end_time - start_time)

# Plotting the results
plt.plot(message_lengths, encryption_times, marker='o', label='Encryption')
plt.plot(message_lengths, decryption_times, marker='x', label='Decryption')
plt.xlabel("Message Length")
plt.ylabel("Time (seconds)")
plt.title("Efficiency Analysis of Solitaire Cipher Encryption and Decryption")
plt.legend()
plt.show()
