import numpy as np
import numpy.typing as npt
from enum import Enum, auto


N_CYCLES = 1000000000


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


def parse_rocks(lines: list[str]) -> npt.NDArray:
    return np.array([[c for c in line] for line in lines])


def tilt(rocks: npt.NDArray, direction: Direction) -> None:
    if direction == Direction.North:
        for i in range(rocks.shape[1]):
            tilt_column(rocks[:, i])
    elif direction == Direction.South:
        for i in range(rocks.shape[1]):
            tilt_column(rocks[::-1, i])
    elif direction == Direction.West:
        for i in range(rocks.shape[0]):
            tilt_column(rocks[i, :])
    elif direction == Direction.East:
        for i in range(rocks.shape[0]):
            tilt_column(rocks[i, ::-1])


def tilt_column(column: npt.NDArray) -> None:
    last_cube = -1
    n_round_since_cube = 0
    for i, stone in enumerate(column):
        if stone == "#":
            last_cube = i
            n_round_since_cube = 0
        elif stone == "O":
            column[i] = "."
            column[last_cube + n_round_since_cube + 1] = "O"
            n_round_since_cube += 1


def cycle(rocks: npt.NDArray) -> None:
    for direction in [Direction.North, Direction.West, Direction.South, Direction.East]:
        tilt(rocks, direction)


def compute_load(rocks: npt.NDArray) -> int:
    return sum([np.sum((rocks[i, :] == "O") * (rocks.shape[0] - i)) for i in range(rocks.shape[0])])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    rocks = parse_rocks(lines)
    for _ in range(100000):
        cycle(rocks)
    for _ in range(20):
        cycle(rocks)
        print(rocks)
        print()
    return compute_load(rocks)


def test_implementation():
    with open("test_input.txt", 'r') as f:
        lines = f.read().splitlines()
    rocks = parse_rocks(lines)
    with open("cycle_1.txt", 'r') as f:
        lines = f.read().splitlines()
    rocks_cycle_1 = parse_rocks(lines)
    with open("cycle_2.txt", 'r') as f:
        lines = f.read().splitlines()
    rocks_cycle_2 = parse_rocks(lines)
    with open("cycle_3.txt", 'r') as f:
        lines = f.read().splitlines()
    rocks_cycle_3 = parse_rocks(lines)
    tilt(rocks, Direction.North)
    assert compute_load(rocks) == 136
    cycle(rocks)
    assert np.all(rocks == rocks_cycle_1)
    cycle(rocks)
    assert np.all(rocks == rocks_cycle_2)
    cycle(rocks)
    assert np.all(rocks == rocks_cycle_3)
    print("all tests passed.")


def main():
    test_implementation()
    assert solution("test_input.txt") == 64
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
