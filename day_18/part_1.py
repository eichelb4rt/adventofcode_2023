import numpy as np
import numpy.typing as npt
import itertools
from dataclasses import dataclass
from enum import Enum


Index = np.int64
Position = npt.NDArray[Index]


class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


@dataclass
class Instruction:
    direction: Direction
    length: int
    color: str


WALK = {
    Direction.Up: np.array([-1, 0], dtype=Index),
    Direction.Down: np.array([1, 0], dtype=Index),
    Direction.Left: np.array([0, -1], dtype=Index),
    Direction.Right: np.array([0, 1], dtype=Index),
}

AXIS = {
    Direction.Up: 0,
    Direction.Down: 0,
    Direction.Left: 1,
    Direction.Right: 1,
}


def parse_instruction(line: str) -> Instruction:
    direction, length, color = line.split()
    return Instruction(Direction(direction), int(length), color[1:-1])


def expand_ground(ground: npt.NDArray[np.bool_], direction: Direction, expanded_length: int) -> npt.NDArray[np.bool_]:
    if direction == Direction.Up:
        return np.r_[np.full((expanded_length, ground.shape[1]), False), ground]
    if direction == Direction.Down:
        return np.r_[ground, np.full((expanded_length, ground.shape[1]), False)]
    if direction == Direction.Left:
        return np.c_[np.full((ground.shape[0], expanded_length), False), ground]
    if direction == Direction.Right:
        return np.c_[ground, np.full((ground.shape[0], expanded_length), False)]
    raise ValueError("Unknown Direction.")


def dig_trench(instructions: list[Instruction]) -> npt.NDArray[np.bool_]:
    ground = np.full((1, 1), False)
    position = np.array([0, 0], dtype=Index)
    for instruction in instructions:
        new_position = position + instruction.length * WALK[instruction.direction]
        moved_axis = AXIS[instruction.direction]
        if new_position[moved_axis] >= ground.shape[moved_axis]:
            expanded_length = new_position[moved_axis] - ground.shape[moved_axis] + 1
            ground = expand_ground(ground, instruction.direction, expanded_length)
        elif new_position[moved_axis] < 0:
            expanded_length = -new_position[moved_axis]
            ground = expand_ground(ground, instruction.direction, expanded_length)
            # if we expand past 0, the indices have to be adapted
            position[moved_axis] += expanded_length
            new_position[moved_axis] += expanded_length
        y_min = min(position[0], new_position[0])
        y_max = max(position[0], new_position[0])
        x_min = min(position[1], new_position[1])
        x_max = max(position[1], new_position[1])
        ground[y_min: y_max + 1, x_min: x_max + 1] = True
        position = new_position
    return ground


def find_propagations(is_wall: npt.NDArray[np.bool_], flooded: npt.NDArray[np.bool_], last_propagations: list[tuple[int, int]]) -> set[tuple[int, int]]:
    propagations = set()
    for y, x in last_propagations:
        if not flooded[y, x]:
            continue
        for direction in Direction:
            new_position = np.array([y, x], dtype=Index) + WALK[direction]
            if not np.all(new_position >= 0) or not np.all(new_position < flooded.shape):
                continue
            if not is_wall[*new_position] and not flooded[*new_position]:
                propagations.add((new_position[0], new_position[1]))
    return propagations


def flood(is_wall: npt.NDArray[np.bool_]) -> npt.NDArray[np.bool_]:
    flooded = np.full(is_wall.shape, False)
    flooded[0, :] = True
    flooded[-1, :] = True
    flooded[:, 0] = True
    flooded[:, -1] = True
    propagations = np.transpose(np.nonzero(flooded)).astype(Index)
    while len(propagations) > 0:
        propagation_arr = np.full(flooded.shape, False)
        for y, x in propagations:
            flooded[y, x] = True
            propagation_arr[y, x] = True
        propagations = find_propagations(is_wall, flooded, propagations)
    return flooded


def pad_ground(ground: npt.NDArray[np.bool_]) -> npt.NDArray[np.bool_]:
    ground_padded = np.full((ground.shape[0] + 2, ground.shape[1] + 2), False)
    ground_padded[1:-1, 1:-1] = ground
    return ground_padded


def visualize(arr: npt.NDArray[np.bool_]) -> str:
    visualization = np.full(arr.shape, ".")
    visualization[arr] = "#"
    return "\n".join(["".join(line) for line in visualization])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    instructions = list(map(parse_instruction, lines))
    ground = dig_trench(instructions)
    walls = pad_ground(ground)
    water = flood(walls)
    return int(np.prod(walls.shape)) - np.count_nonzero(water)


def main():
    assert solution("test_input.txt") == 62
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
