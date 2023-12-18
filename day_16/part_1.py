import numpy as np
import numpy.typing as npt
from enum import Enum, auto


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


Position = npt.NDArray[np.int8]
Ray = tuple[Position, Direction]

WALK = {
    Direction.North: np.array([-1, 0], dtype=np.int8),
    Direction.South: np.array([1, 0], dtype=np.int8),
    Direction.East: np.array([0, 1], dtype=np.int8),
    Direction.West: np.array([0, -1], dtype=np.int8),
}


def parse_contraption(lines: list[str]) -> npt.NDArray:
    return np.array([[c for c in line] for line in lines])


def divert_light(tile: str, current_direction: Direction) -> list[Direction]:
    if tile == ".":
        return [current_direction]
    if tile == "/":
        if current_direction == Direction.North:
            return [Direction.East]
        if current_direction == Direction.South:
            return [Direction.West]
        if current_direction == Direction.East:
            return [Direction.North]
        if current_direction == Direction.West:
            return [Direction.South]
        raise ValueError(f"Unknown Direction: {current_direction}")
    if tile == "\\":
        if current_direction == Direction.North:
            return [Direction.West]
        if current_direction == Direction.South:
            return [Direction.East]
        if current_direction == Direction.East:
            return [Direction.South]
        if current_direction == Direction.West:
            return [Direction.North]
        raise ValueError(f"Unknown Direction: {current_direction}")
    if tile == "|":
        if current_direction in [Direction.North, Direction.South]:
            return [current_direction]
        return [Direction.North, Direction.South]
    if tile == "-":
        if current_direction in [Direction.East, Direction.West]:
            return [current_direction]
        return [Direction.East, Direction.West]


def visualize(bool_array: npt.NDArray[np.bool_]) -> npt.NDArray:
    visualization = np.full(bool_array.shape, ".")
    visualization[bool_array] = "#"
    return visualization


def trace_paths(contraption: npt.NDArray) -> int:
    travelling_light = {direction: np.full(contraption.shape, False) for direction in Direction}
    rays: list[Ray] = [(np.array([0, 0], dtype=np.int8), Direction.East)]
    travelling_light[Direction.East][0, 0] = True
    while len(rays) > 0:
        # walk 1 step
        ray_position, ray_direction = rays.pop()
        new_directions = divert_light(contraption[*ray_position], ray_direction)
        # keep computing relevant paths
        for new_direction in new_directions:
            new_position = ray_position + WALK[new_direction]
            # if we reached the edge, we can stop
            if np.any(new_position < 0) or np.any(new_position >= contraption.shape):
                continue
            # if we've already seen this ray, we can stop
            if travelling_light[new_direction][*new_position]:
                continue
            rays.append((new_position, new_direction))
            travelling_light[new_direction][*new_position] = True
    return np.count_nonzero(travelling_light[Direction.North] | travelling_light[Direction.South] | travelling_light[Direction.East] | travelling_light[Direction.West])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    contraption = parse_contraption(lines)
    return trace_paths(contraption)


def main():
    assert solution("test_input.txt") == 46
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
