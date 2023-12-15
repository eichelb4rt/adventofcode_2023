def parse_instructions(line: str) -> list[str]:
    return line.split(",")


def hash_instruction(instruction: str) -> int:
    hash_result = 0
    for c in instruction:
        hash_result += ord(c)
        hash_result *= 17
        hash_result %= 256
    return hash_result


def solution(input_file: str):
    with open(input_file, 'r') as f:
        line = f.read().strip()
    instructions = parse_instructions(line)
    return sum(map(hash_instruction, instructions))


def main():
    assert solution("test_input.txt") == 1320
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
