import numpy as np
import numpy.typing as npt
from queue import PriorityQueue
from dataclasses import dataclass, field
from enum import Enum, auto


MAX_LINE_LENGTH = 3
Index = np.uint8
Position = npt.NDArray[Index]
MAX_INT_VALUE = np.iinfo(np.int64).max


class Direction(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()


class Axis(Enum):
    Vertical = auto()
    Horizontal = auto()


OPPOSITE = {
    Direction.North: Direction.South,
    Direction.South: Direction.North,
    Direction.East: Direction.West,
    Direction.West: Direction.East,
}

WALK_STEP = {
    Direction.North: np.array([-1, 0], dtype=Index),
    Direction.South: np.array([1, 0], dtype=Index),
    Direction.East: np.array([0, 1], dtype=Index),
    Direction.West: np.array([0, -1], dtype=Index),
}

AXIS = {
    Direction.North: Axis.Vertical,
    Direction.South: Axis.Vertical,
    Direction.East: Axis.Horizontal,
    Direction.West: Axis.Horizontal,
}


@dataclass(order=True)
class QueueItem:
    heat_lost: int
    position: Position = field(compare=False)
    from_direction: Direction = field(compare=False)


def parse_blocks(lines: list[str]) -> npt.NDArray[np.int64]:
    return np.array([[int(c) for c in line] for line in lines], dtype=np.int64)


def orthogonal_directions(direction: Direction) -> list[Direction]:
    return [orthogonal_direction for orthogonal_direction in Direction if orthogonal_direction not in [direction, OPPOSITE[direction]]]


def add_direction(blocks: npt.NDArray[np.int64], min_heat_lost: dict[Axis, npt.NDArray[np.int64]], work_list: PriorityQueue[QueueItem], current_item: QueueItem, direction: Direction) -> None:
    heat_lost = current_item.heat_lost
    for n_steps in range(1, MAX_LINE_LENGTH + 1):
        # walk in the direction, see if it's in bounds
        new_position = current_item.position + n_steps * WALK_STEP[direction]
        if not np.all(new_position >= 0) or not np.all(new_position < blocks.shape):
            return
        # we're still in bounds. add that new position to the work list
        heat_lost += blocks[*new_position]
        # only add the reached node to the work list (and update) if we have not found a better way on that axis
        if heat_lost < min_heat_lost[AXIS[direction]][*new_position]:
            work_list.put(QueueItem(heat_lost, new_position, direction))
            min_heat_lost[AXIS[direction]][*new_position] = heat_lost


def shortest_path(blocks: npt.NDArray[np.int64]) -> int:
    assert np.all(np.array(blocks.shape) >= MAX_LINE_LENGTH + 1), "This problem is not interesting enough for me."
    # where we start and end
    start_index = np.array([0, 0], dtype=Index)
    destination_index = np.array(blocks.shape, dtype=Index) - 1
    # minimum heat lost when arriving at the position from the indexed axis
    min_heat_lost = {axis: np.full(blocks.shape, MAX_INT_VALUE, dtype=np.int64) for axis in Axis}
    work_list: PriorityQueue[QueueItem] = PriorityQueue()
    # add a queue item for the start index coming from every direction
    for direction in Direction:
        work_list.put(QueueItem(0, start_index, direction))
    # BFS
    while not work_list.empty():
        current_item = work_list.get()
        # if we already can't get better than the best we have currently reached, we're done
        if current_item.heat_lost >= min([min_heat_lost[axis][*destination_index] for axis in Axis]):
            return min([min_heat_lost[axis][*destination_index] for axis in Axis])
        # add the directions that are
        for direction in orthogonal_directions(current_item.from_direction):
            add_direction(blocks, min_heat_lost, work_list, current_item, direction)
    return min([min_heat_lost[axis][*destination_index] for axis in Axis])


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    blocks = parse_blocks(lines)
    return shortest_path(blocks)


def main():
    assert solution("test_input.txt") == 102
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
