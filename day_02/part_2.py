import numpy as np
import numpy.typing as npt
from collections import Counter

Hand = npt.NDArray[np.int8]
GameInfo = tuple[int, list[Hand]]


allowed_colors = ["red", "green", "blue"]


def parse_hand(hand: str) -> Hand:
    colors_and_numbers = [color_and_number.strip().split(" ") for color_and_number in hand.split(", ")]
    hand = np.zeros(len(allowed_colors))
    for number_word, color in colors_and_numbers:
        hand[allowed_colors.index(color)] = int(number_word)
    return hand


def parse_game(line: str) -> GameInfo:
    game_name, record = line.split(":")
    game_id = int(game_name[len("Game "):])
    hand_strings = record.split(";")
    hands = [parse_hand(hand) for hand in hand_strings]
    return game_id, hands


def compute_power(game: GameInfo) -> int:
    _, record = game
    return int(np.prod(np.max(np.array(record), axis=0)))


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    games = list(map(parse_game, lines))
    powers = list(map(compute_power, games))
    return sum(powers)


def main():
    assert solution("test_input.txt") == 2286
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
