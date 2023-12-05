from collections import Counter

Hand = dict[str, int]
GameInfo = tuple[int, list[Hand]]


MAX_ALLOWED_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def parse_hand(hand: str) -> Hand:
    colors_and_numbers = [color_and_number.strip().split(" ") for color_and_number in hand.split(", ")]
    cubes = Counter({color: int(number_word) for number_word, color in colors_and_numbers})
    return cubes


def parse_game(line: str) -> GameInfo:
    game_name, record = line.split(":")
    game_id = int(game_name[len("Game "):])
    hand_strings = record.split(";")
    hands = [parse_hand(hand) for hand in hand_strings]
    return game_id, hands


def is_possible(game: GameInfo) -> bool:
    _, record = game
    return all([hand[color] <= max_allowed for hand in record for color, max_allowed in MAX_ALLOWED_CUBES.items()])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    games = list(map(parse_game, lines))
    allowed_games = list(filter(is_possible, games))
    return sum([game_id for game_id, _ in allowed_games])


def main():
    assert solution("test_input.txt") == 8
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
