DIGITS = list(map(str, range(10)))


def digits_in_line(line: str) -> list[int]:
    return [int(c) for c in line if c in DIGITS]


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    digits_per_line = [digits_in_line(line) for line in lines]
    return sum([digits[0] * 10 + digits[-1] for digits in digits_per_line])


def main():
    assert solution("test_input_1.txt") == 142
    answer = solution("input.txt")
    print(f"The calibration number is: {answer}")


if __name__ == "__main__":
    main()
