import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from enum import Enum


Index = np.int64
Position = npt.NDArray[Index]


class Direction(Enum):
    Up = "3"
    Down = "1"
    Left = "2"
    Right = "0"


@dataclass
class Instruction:
    direction: Direction
    length: int


@dataclass(order=True)
class Interval:
    start: int
    end: int

    def __post_init__(self):
        self.length = self.end - self.start + 1


WALK = {
    Direction.Up: np.array([-1, 0], dtype=Index),
    Direction.Down: np.array([1, 0], dtype=Index),
    Direction.Left: np.array([0, -1], dtype=Index),
    Direction.Right: np.array([0, 1], dtype=Index),
}


def parse_instruction(line: str) -> Instruction:
    _, _, color = line.split()
    length = int(color[2:-2], base=16)
    direction = Direction(color[-2])
    return Instruction(direction, length)


def create_intervals(instructions: list[Instruction]) -> list[tuple[int, list[Interval]]]:
    position = np.array([0, 0], dtype=Index)
    intervals = []
    for instruction in instructions:
        if instruction.direction == Direction.Up:
            intervals.append((position[1], Interval(position[0] - instruction.length, position[0])))
        elif instruction.direction == Direction.Down:
            intervals.append((position[1], Interval(position[0], position[0] + instruction.length)))
        position += instruction.length * WALK[instruction.direction]
    intervals.sort()
    intervals_with_same_x = []
    current_x, _ = intervals[0]
    current_interval_collection = []
    for x, interval in intervals:
        if x == current_x:
            current_interval_collection.append(interval)
        else:
            intervals_with_same_x.append((current_x, current_interval_collection))
            current_interval_collection = [interval]
            current_x = x
    intervals_with_same_x.append((current_x, current_interval_collection))
    return intervals_with_same_x


def can_connect(interval_1: Interval, interval_2: Interval) -> bool:
    return interval_1.end == interval_2.start or interval_2.end == interval_1.start


def connect(interval_1: Interval, interval_2: Interval) -> Interval:
    if interval_1.end == interval_2.start:
        return Interval(interval_1.start, interval_2.end)
    return Interval(interval_2.start, interval_1.end)


def reduce_active(active_intervals: list[Interval]) -> list[Interval]:
    if len(active_intervals) == 0:
        return []
    sorted_intervals = sorted(active_intervals)
    reduced_intervals = []
    current_interval = sorted_intervals[0]
    for interval in sorted_intervals[1:]:
        if can_connect(current_interval, interval):
            current_interval = connect(current_interval, interval)
        else:
            reduced_intervals.append(current_interval)
            current_interval = interval
    reduced_intervals.append(current_interval)
    return reduced_intervals


def includes(big_interval: Interval, small_interval: Interval) -> bool:
    return big_interval.start <= small_interval.start and small_interval.end <= big_interval.end


def overlap(interval_1: Interval, interval_2: Interval) -> bool:
    return (interval_1.start <= interval_2.start <= interval_1.end) or (interval_1.start <= interval_2.end <= interval_1.end)


def cut_interval(big_interval: Interval, small_interval: Interval) -> list[Interval]:
    if big_interval == small_interval:
        return []
    if big_interval.start == small_interval.start:
        return [Interval(small_interval.end, big_interval.end)]
    if big_interval.end == small_interval.end:
        return [Interval(big_interval.start, small_interval.start)]
    return [Interval(big_interval.start, small_interval.start), Interval(small_interval.end, big_interval.end)]


def cut_all(active_intervals: list[Interval], cutting_intervals: list[Interval]) -> list[Interval]:
    for interval in cutting_intervals:
        added_intervals = []
        removed_intervals = []
        for active_interval in active_intervals:
            if includes(active_interval, interval):
                removed_intervals.append(active_interval)
                added_intervals += cut_interval(active_interval, interval)
        active_intervals = [interval for interval in active_intervals if interval not in removed_intervals] + added_intervals
    return sorted(active_intervals)


def compute_area(intervals_on_same_x: list[tuple[int, list[Interval]]]) -> int:
    last_x, first_intervals = intervals_on_same_x[0]
    active_intervals: list[Interval] = first_intervals
    area = sum([interval.length for interval in active_intervals])
    for x, intervals in intervals_on_same_x[1:]:
        cutting_intervals = [interval for interval in intervals if any([includes(active_interval, interval) for active_interval in active_intervals])]
        non_cutting_intervals = [interval for interval in intervals if interval not in cutting_intervals]
        # add all lines i such that last_x < i < x
        area += (x - last_x - 1) * sum([interval.length for interval in active_intervals])
        # add all intervals that don't cut other intervals
        active_intervals += non_cutting_intervals
        active_intervals = reduce_active(active_intervals)
        area += sum([interval.length for interval in active_intervals])
        # prepare the next iteration
        active_intervals = cut_all(active_intervals, cutting_intervals)
        last_x = x
    assert len(active_intervals) == 0, active_intervals
    return area


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    instructions = list(map(parse_instruction, lines))
    intervals_on_same_x = create_intervals(instructions)
    return compute_area(intervals_on_same_x)


def main():
    assert solution("test_input.txt") == 952408144115
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
