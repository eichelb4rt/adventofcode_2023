from enum import Enum
from collections import Counter
from functools import cmp_to_key

Card = str
Hand = str


class HandType(Enum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


CARD_ORDER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def parse_line(line: str) -> tuple[Hand, int]:
    hand, bid_str = line.split()
    return hand, int(bid_str)


def compute_type(hand: Hand) -> HandType:
    card_counts = Counter(hand)
    n_jokers = card_counts.pop("J") if "J" in card_counts else 0
    if n_jokers == 5:
        return HandType.FiveOfAKind
    most_common_cards = card_counts.most_common()
    _, sorted_card_counts = list(zip(*most_common_cards))
    if sorted_card_counts[0] + n_jokers == 5:
        return HandType.FiveOfAKind
    if sorted_card_counts[0] + n_jokers == 4:
        return HandType.FourOfAKind
    if sorted_card_counts[0] + n_jokers == 3:
        if sorted_card_counts[1] == 2:
            return HandType.FullHouse
        return HandType.ThreeOfAKind
    if sorted_card_counts[0] + n_jokers == 2:
        if sorted_card_counts[1] == 2:
            return HandType.TwoPair
        return HandType.OnePair
    return HandType.HighCard


def card_value(card: Card) -> int:
    """Higher is better."""

    return CARD_ORDER.index(card)


def compare_hands(hand_1: Hand, hand_2: Hand) -> int:
    """hand_1 < hand_2: <0, hand_1 == hand_2: 0, hand_1 > hand_2: >0"""

    type_1 = compute_type(hand_1)
    type_2 = compute_type(hand_2)
    # types aren't equal, then return that
    if type_1 != type_2:
        return type_1.value - type_2.value
    # if types are equal, find the first difference
    for card_1, card_2 in zip(hand_1, hand_2):
        if card_1 != card_2:
            return card_value(card_1) - card_value(card_2)
    # cards are truly equal
    return 0


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    hands_and_bids = list(map(parse_line, lines))
    hands_and_bids.sort(key=cmp_to_key(lambda a, b: compare_hands(a[0], b[0])))
    return sum([rank * bid for rank, (_, bid) in enumerate(hands_and_bids, 1)])


def main():
    assert solution("test_input.txt") == 5905
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
