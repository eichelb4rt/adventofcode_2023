import numpy as np
import numpy.typing as npt
from enum import Enum, auto


N_CYCLES = 1000000000
N_CYCLES_BEFORE_LOOP_CHECK = 1000
MAX_LOOP_SIZE = 100


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


def compute_load_per_row(n_rows: int) -> npt.NDArray[np.uint64]:
    return np.array([n_rows - i for i in range(n_rows)], dtype=np.uint64)


def compute_load(rock_hash: npt.NDArray[np.bool_]) -> int:
    load_per_row = compute_load_per_row(rock_hash.shape[0])
    return np.einsum("ij, i -> ", rock_hash, load_per_row)


def hash_rocks(rocks: npt.NDArray) -> npt.NDArray[np.bool_]:
    return rocks == "O"


def find_loop(hashes: list[npt.NDArray[np.bool_]]) -> list[int]:
    for loop_size in range(1, MAX_LOOP_SIZE):
        if np.all(hashes[-1] == hashes[-loop_size - 1]):
            return hashes[-loop_size:]
    return None


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    rocks = parse_rocks(lines)
    hashes = []
    for _ in range(N_CYCLES_BEFORE_LOOP_CHECK):
        cycle(rocks)
        hashes.append(hash_rocks(rocks))
    loop = find_loop(hashes)
    return compute_load(loop[(N_CYCLES - N_CYCLES_BEFORE_LOOP_CHECK - 1) % len(loop)])


def main():
    assert solution("test_input.txt") == 64
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
