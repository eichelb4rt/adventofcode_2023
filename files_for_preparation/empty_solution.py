def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    return None


def main():
    assert solution("test_input.txt") == EXPECTED_SOLUTION
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
