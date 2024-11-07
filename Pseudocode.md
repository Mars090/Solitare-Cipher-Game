START

FUNCTION initialise_deck()
    CREATE a list of numbers from 1 to 54
    RETURN the list as the deck

FUNCTION text_to_numbers(text)
    CONVERT text to uppercase
    CONVERT each letter in text to a number (A=1, B=2, ..., Z=26)
    RETURN list of numbers

FUNCTION numbers_to_text(numbers)
    CONVERT each number in list to a letter (1=A, 2=B, ..., 26=Z)
    RETURN the string of letters

FUNCTION move_joker_a(deck)
    FIND position of Joker A (value 53)
    REMOVE Joker A from its position
    INSERT Joker A one position forward in the deck

FUNCTION move_joker_b(deck)
    FIND position of Joker B (value 54)
    REMOVE Joker B from its position
    INSERT Joker B two positions forward in the deck

FUNCTION triple_cut(deck)
    FIND positions of Joker A (value 53) and Joker B (value 54)
    IF Joker A is after Joker B, SWAP their positions
    PERFORM a triple cut:
        MOVE all cards before the first joker to the end
        MOVE cards between the jokers to the beginning
        KEEP cards including and after the last joker in place
    RETURN the modified deck

FUNCTION count_cut(deck)
    GET the value of the last card in the deck
    IF last card is a joker (53 or 54), SET value to 53
    CUT the deck by moving the number of cards equal to the last card's value from the top to above the last card
    RETURN the modified deck

FUNCTION get_keystream_value(deck)
    GET the value of the top card
    IF the top card is a joker (53 or 54), SET value to 53
    RETURN the card at the position indicated by this value

FUNCTION generate_keystream(deck, length)
    INITIALISE an empty keystream list
    FOR each position up to the specified length:
        CALL move_joker_a(deck)
        CALL move_joker_b(deck)
        CALL triple_cut(deck)
        CALL count_cut(deck)
        GET a keystream value from the deck using get_keystream_value(deck)
        IF keystream value is a joker (53 or 54):
            REPEAT the process until a non-joker keystream value is obtained
        ADD the keystream value to the keystream list
    RETURN the keystream list

FUNCTION encrypt(message, deck)
    CONVERT message to a list of numbers using text_to_numbers(message)
    GENERATE a keystream of the same length as the message using generate_keystream(deck, length of message)
    FOR each number in message:
        ADD corresponding keystream value to the message number (mod 26)
    CONVERT the resulting numbers to text using numbers_to_text()
    RETURN the encrypted text

FUNCTION decrypt(ciphertext, deck)
    CONVERT ciphertext to a list of numbers using text_to_numbers(ciphertext)
    GENERATE a keystream of the same length as the ciphertext using generate_keystream(deck, length of ciphertext)
    FOR each number in ciphertext:
        SUBTRACT corresponding keystream value from the ciphertext number (mod 26)
    CONVERT the resulting numbers to text using numbers_to_text()
    RETURN the decrypted text

END
