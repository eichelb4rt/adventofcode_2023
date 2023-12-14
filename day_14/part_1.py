import numpy as np
import numpy.typing as npt


def parse_rocks(lines: list[str]) -> npt.NDArray:
    return np.array([[c for c in line] for line in lines])


def load_in_column(column: npt.NDArray) -> int:
    n_rows = len(column)
    total_load = 0
    last_cube = 0
    n_round_since_cube = 0
    for i, stone in enumerate(column, 1):
        if stone == "#":
            last_cube = i
            n_round_since_cube = 0
        elif stone == "O":
            total_load += n_rows - (last_cube + n_round_since_cube)
            n_round_since_cube += 1
    return total_load


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    rocks = parse_rocks(lines)
    return sum([load_in_column(rocks[:, i]) for i in range(rocks.shape[1])])


def main():
    assert solution("test_input.txt") == 136
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
