import argparse
import random
import json

def load_file(path):
    with open(path, "r") as file:
        words = json.load(file)

    new_words = {key.lower(): value for key, value in words.items()}
    word_bank = list(new_words.keys())
    return word_bank, new_words


def choose_word(word_bank, words):
    global list_of_guesses, list_of_incorrect_guesses
    list_of_guesses, list_of_incorrect_guesses = [], []
    secret_word = word_bank.pop(0)
    print(f"Category: {words[secret_word]}")
    return secret_word


def display_word(secret_word, scores_of_players, list_of_players):
    if list_of_incorrect_guesses:
        print("\nIncorrect letters:", list_of_incorrect_guesses)

    for player, score in zip(list_of_players, scores_of_players):
        print(f"{player}: {score}")

    for letter in secret_word:
        if letter in list_of_guesses:
            print(letter, end="")
        else:
            print("_", end="")
    print()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Path to the JSON file with words: ")
    parser.add_argument("players", type=int, help="Number of players: ")
    parser.add_argument("words", type=int, help="Number of words to play with: ")
    return parser.parse_args()

def main():
    global word_bank, words
    args = parse_arguments()
    word_bank, words = load_file(args.file)
    if args.words > len(word_bank):
        print(f"You have only {len(word_bank)} words available.. ")
        return

    word_bank = random.sample(word_bank, args.words)
    list_of_players = [input(f"Please enter name for player {i + 1}: ") for i in range(args.players)]
    scores_of_players = [0] * args.players
    count = 0
    while word_bank:
        secret_word = choose_word(word_bank, words).lower()
        while True:
            display_word(secret_word, scores_of_players, list_of_players)
            turn = list_of_players[count]
            guess = input(f"{turn}, guess a letter: ").lower()
            while guess in list_of_incorrect_guesses or guess in list_of_guesses or len(guess) > 1:
                guess = input(f"{turn}, guess a letter: ").lower()

            if guess in secret_word:
                list_of_guesses.append(guess)
                scores_of_players[count] += secret_word.count(guess)
            else:
                list_of_incorrect_guesses.append(guess)

            count = (count + 1) % len(list_of_players)

            if all(letter in list_of_guesses for letter in secret_word):
                print(f"The word was {secret_word}")
                break

    print("The game is over..")
    max_score = max(scores_of_players)
    winners = [player for player, score in zip(list_of_players, scores_of_players) if score == max_score]
    print(f"The winner/s: {" ,".join(winners)} with {max_score} points.. ")


if __name__ == '__main__':
    main()
