DIGITS = list(map(str, range(10)))
WORD_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def replace_words(line: str) -> str:
    for word, digit in WORD_TO_DIGIT.items():
        # word before and after digit, so that this insertion doesn't destroy spelled out digits before and after this one
        line = line.replace(word, word + str(digit) + word)
    return line


def digits_in_line(line: str) -> list[int]:
    return [int(c) for c in line if c in DIGITS]


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    lines = [replace_words(line) for line in lines]
    digits_per_line = [digits_in_line(line) for line in lines]
    return sum([digits[0] * 10 + digits[-1] for digits in digits_per_line])


def main():
    assert solution("test_input_2.txt") == 281
    answer = solution("input.txt")
    print(f"The calibration number is: {answer}")


if __name__ == "__main__":
    main()
