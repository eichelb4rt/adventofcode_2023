# x, y
Coordinate = tuple[int, int]
DIGITS = list(map(str, range(10)))
NON_SYMBOLS = DIGITS + ['.']
# number, y, x_start, x_end
NumberInfo = tuple[int, int, int, int]


def extract_coordinates_with_symbols(lines: list[str]) -> set[Coordinate]:
    height = len(lines)
    assert height > 0
    width = len(lines[0])
    return {(x, y) for y in range(height) for x in range(width) if lines[y][x] not in NON_SYMBOLS}


def extract_numbers_in_line(line: str, y: int) -> list[NumberInfo]:
    number = ""
    number_start = 0
    number_end = 0
    numbers: list[NumberInfo] = []
    for x, c in enumerate(line):
        if c in DIGITS:
            # if we find a digit, continue building the current number
            number += c
            number_end = x
        else:
            # if we find non-digit, maybe save the number and prepare for the next one
            if number != "":
                numbers.append((int(number), y, number_start, number_end))
            number = ""
            number_start = x + 1
    # maybe save the number one last time
    if number != "":
        numbers.append((int(number), y, number_start, number_end))
    return numbers


def extract_numbers(lines: list[str]) -> list[NumberInfo]:
    return [number_info for y, line in enumerate(lines) for number_info in extract_numbers_in_line(line, y)]


def build_possible_symbol_coordinates(number: NumberInfo) -> set[Coordinate]:
    _, y_number, x_start, x_end = number
    return {(x, y) for y in range(y_number - 1, y_number + 2) for x in range(x_start - 1, x_end + 2)}


def is_relevant(number: NumberInfo, coordinates_with_symbols: set[Coordinate]) -> bool:
    # if the intersection of the possible symbol coordinates and the coordinates with symbols is empty, the number is not relevant
    return len(build_possible_symbol_coordinates(number).intersection(coordinates_with_symbols)) > 0


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    coordinates_with_symbols = extract_coordinates_with_symbols(lines)
    numbers = extract_numbers(lines)
    relevant_numbers = [number for number, _, _, _ in list(filter(lambda number: is_relevant(number, coordinates_with_symbols), numbers))]
    return sum(relevant_numbers)


def main():
    assert solution("test_input.txt") == 4361
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
