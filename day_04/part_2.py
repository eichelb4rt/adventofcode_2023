import numpy as np
import re

Card = tuple[list[int], list[int]]


def parse_card(line: str) -> Card:
    _, card_str = line.split(":")
    winning_str, own_str = card_str.split("|")
    winning_str = re.sub(r"\s+", " ", winning_str.strip())
    own_str = re.sub(r"\s+", " ", own_str.strip())
    return list(map(int, winning_str.split(" "))), list(map(int, own_str.split(" ")))


def compute_n_matches(card: Card) -> int:
    winning, own = card
    return len(set(winning).intersection(own))


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    cards = list(map(parse_card, lines))
    n_matches_per_card = list(map(compute_n_matches, cards))
    n_copies_per_card = np.full(len(cards), 1)
    for i, n_matches in enumerate(n_matches_per_card):
        n_copies_per_card[i + 1: i + n_matches + 1] += n_copies_per_card[i]
    return np.sum(n_copies_per_card)


def main():
    assert solution("test_input.txt") == 30
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
