import numpy as np
import numpy.typing as npt
from enum import Enum, auto


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()

CONNECTED_DIRECTIONS = {
    "|": (Direction.North, Direction.South),
    "-": (Direction.East, Direction.West),
    "L": (Direction.North, Direction.East),
    "J": (Direction.North, Direction.West),
    "7": (Direction.South, Direction.West),
    "F": (Direction.South, Direction.East),
}


# change to [y, x]
WALK = {
    Direction.North: np.array([-1, 0], dtype=np.int64),
    Direction.South: np.array([1, 0], dtype=np.int64),
    Direction.East: np.array([0, 1], dtype=np.int64),
    Direction.West: np.array([0, -1], dtype=np.int64),
}


OPPOSITE = {
    Direction.North: Direction.South,
    Direction.South: Direction.North,
    Direction.East: Direction.West,
    Direction.West: Direction.East,
}


def find_start(lines: list[str]) -> npt.NDArray[np.int64]:
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                return np.array([y, x], dtype=np.int64)


def get_possible_start_direction(start_position: npt.NDArray[np.int64], ground: npt.NDArray) -> Direction:
    for direction in Direction:
        next_position = start_position + WALK[direction]
        pipe = ground[*next_position]
        if pipe not in CONNECTED_DIRECTIONS:
            continue
        if OPPOSITE[direction] in CONNECTED_DIRECTIONS[pipe]:
            return direction


def next_direction(current_direction: Direction, pipe: str) -> Direction:
    connected = CONNECTED_DIRECTIONS[pipe]
    coming_from = OPPOSITE[current_direction]
    if coming_from == connected[0]:
        return connected[1]
    return connected[0]


def compute_length(start_position: npt.NDArray[np.int32], ground: npt.NDArray) -> int:
    direction = get_possible_start_direction(start_position, ground)
    position = start_position + WALK[direction]
    n_steps = 1
    while not np.all(position == start_position):
        pipe = ground[*position]
        direction = next_direction(direction, pipe)
        position += WALK[direction]
        n_steps += 1
    return n_steps


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    ground = np.array([[c for c in line] for line in lines])
    start_position = find_start(ground)
    total_length = compute_length(start_position, ground)
    return total_length // 2


def main():
    assert solution("test_input_1_part_1.txt") == 4
    assert solution("test_input_2_part_1.txt") == 10
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
