import itertools


def parse_line(line: str) -> tuple[list[str], list[int]]:
    line, check = line.split()
    return list(line), list(map(int, check.split(",")))


def find_unknown(line: str) -> list[int]:
    return [i for i, spring in enumerate(line) if spring == "?"]


def compute_check(spring_line: list[str]) -> list[int]:
    check = []
    contiguous = 0
    for spring in spring_line:
        if spring == "#":
            contiguous += 1
        else:
            if contiguous > 0:
                check.append(contiguous)
            contiguous = 0
    if contiguous > 0:
        check.append(contiguous)
    return check


def substitute(springs: list[str], unknown_indices: list[int], assignments: list[str]) -> list[str]:
    for assignment_index, line_index in enumerate(unknown_indices):
        springs[line_index] = assignments[assignment_index]
    return springs


def compute_possible_arrangements(spring_line: list[str], check: list[int]) -> int:
    n_possible_arrangements = 0
    unknown_indices = find_unknown(spring_line)
    for assignments in itertools.product(["#", "."], repeat=len(unknown_indices)):
        substitute(spring_line, unknown_indices, assignments)
        if compute_check(spring_line) == check:
            n_possible_arrangements += 1
    return n_possible_arrangements


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    spring_lines, checks = zip(*map(parse_line, lines))
    return sum([compute_possible_arrangements(spring_line, check) for spring_line, check in zip(spring_lines, checks)])


def main():
    assert solution("test_input.txt") == 21
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
