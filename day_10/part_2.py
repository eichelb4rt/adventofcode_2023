import numpy as np
import numpy.typing as npt
from enum import Enum, auto
import itertools

np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=np.inf)


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

PIPES = {
    (Direction.North, Direction.South): "|",
    (Direction.East, Direction.West): "-",
    (Direction.North, Direction.East): "L",
    (Direction.North, Direction.West): "J",
    (Direction.South, Direction.West): "7",
    (Direction.South, Direction.East): "F",
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


def get_start_pipe(start_position: npt.NDArray[np.int64], ground: npt.NDArray) -> str:
    connected_directions = []
    for direction in Direction:
        next_position = start_position + WALK[direction]
        if not np.all(next_position >= 0) or not np.all(next_position < ground.shape):
            continue
        pipe = ground[*next_position]
        if pipe not in CONNECTED_DIRECTIONS:
            continue
        if OPPOSITE[direction] in CONNECTED_DIRECTIONS[pipe]:
            connected_directions.append(direction)
    return PIPES[tuple(connected_directions)]


def next_direction(current_direction: Direction, pipe: str) -> Direction:
    connected = CONNECTED_DIRECTIONS[pipe]
    coming_from = OPPOSITE[current_direction]
    if coming_from == connected[0]:
        return connected[1]
    return connected[0]


def compute_loop_tiles(start_position: npt.NDArray[np.int64], ground: npt.NDArray) -> npt.NDArray[np.bool8]:
    """Assumes that start pipe has already been replaced."""
    
    assert ground[*start_position] != "S"
    is_loop_tile = np.full(ground.shape, False)
    direction = CONNECTED_DIRECTIONS[ground[*start_position]][0]
    position = start_position + WALK[direction]
    is_loop_tile[*position] = True
    while not np.all(position == start_position):
        pipe = ground[*position]
        direction = next_direction(direction, pipe)
        position += WALK[direction]
        is_loop_tile[*position] = True
    return is_loop_tile


def zoom_on_pipe(pipe: str) -> npt.NDArray[np.bool8]:
    zoomed_in = np.full((3, 3), False)
    center = np.array([1, 1])
    zoomed_in[*center] = True
    zoomed_in[*(center + WALK[CONNECTED_DIRECTIONS[pipe][0]])] = True
    zoomed_in[*(center + WALK[CONNECTED_DIRECTIONS[pipe][1]])] = True
    return zoomed_in


def zoom_in(ground: npt.NDArray, is_loop_tile: npt.NDArray[np.bool8]) -> npt.NDArray[np.bool8]:
    zoomed_in = np.full((3 * ground.shape[0], 3 * ground.shape[1]), False)
    for y in range(ground.shape[0]):
        for x in range(ground.shape[1]):
            if is_loop_tile[y, x]:
                zoomed_in[3 * y : 3 * (y + 1), 3 * x: 3 * (x + 1)] = zoom_on_pipe(ground[y, x])
    return zoomed_in


def visualize(arr: npt.NDArray[np.bool8]) -> str:
    visualization = np.full(arr.shape, ".")
    visualization[arr] = "X"
    return "\n".join(["".join(line) for line in visualization])


def find_propagations(is_wall: npt.NDArray[np.bool8], flooded: npt.NDArray[np.bool8], last_propagations: list[tuple[int, int]]) -> set[tuple[int, int]]:
    propagations = set()
    for y, x in last_propagations:
        if not flooded[y, x]:
            continue
        for offset_y, offset_x in itertools.product([-1, 1], [-1, 1]):
            if not 0 <= y + offset_y < flooded.shape[0] or not 0 <= x + offset_x < flooded.shape[1]:
                continue
            if not is_wall[y + offset_y, x + offset_x] and not flooded[y + offset_y, x + offset_x]:
                propagations.add((y + offset_y, x + offset_x))
    return propagations


def flood(is_wall: npt.NDArray[np.bool8]) -> npt.NDArray[np.bool8]:
    flooded = np.full(is_wall.shape, False)
    flooded[0, :] = True
    flooded[-1, :] = True
    flooded[:, 0] = True
    flooded[:, -1] = True
    propagations = np.transpose(np.nonzero(flooded))
    while len(propagations) > 0:
        propagation_arr = np.full(flooded.shape, False)
        for y, x in propagations:
            flooded[y, x] = True
            propagation_arr[y, x] = True
        propagations = find_propagations(is_wall, flooded, propagations)
    return flooded


def compute_enclosed_area(ground: npt.NDArray, start_position: npt.NDArray[np.int64]) -> int:
    assert ground[*start_position] != "S"
    is_loop_tile = compute_loop_tiles(start_position, ground)
    zoomed_in = zoom_in(ground, is_loop_tile)
    flooded = flood(zoomed_in)
    is_flooded_tile = flooded[1::3,1::3]
    is_enclosed_tile = ~(is_loop_tile | is_flooded_tile)
    return np.count_nonzero(is_enclosed_tile)


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    ground = np.array([[c for c in line] for line in lines])
    start_position = find_start(ground)
    ground[*start_position] = get_start_pipe(start_position, ground)
    return compute_enclosed_area(ground, start_position)


def main():
    # assert solution("test_input_1_part_2.txt") == 4
    assert solution("test_input_2_part_2.txt") == 4
    assert solution("test_input_3_part_2.txt") == 8
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
