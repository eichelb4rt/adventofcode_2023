import re

Card = tuple[list[int], list[int]]


def parse_card(line: str) -> Card:
    _, card_str = line.split(":")
    winning_str, own_str = card_str.split("|")
    winning_str = re.sub(r"\s+", " ", winning_str.strip())
    own_str = re.sub(r"\s+", " ", own_str.strip())
    return list(map(int, winning_str.split(" "))), list(map(int, own_str.split(" ")))


def compute_points(card: Card) -> int:
    winning, own = card
    n_matches = len(set(winning).intersection(own))
    if n_matches == 0:
        return 0
    return 2**(n_matches - 1)


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    cards = list(map(parse_card, lines))
    points = list(map(compute_points, cards))
    return sum(points)


def main():
    assert solution("test_input.txt") == 13
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
