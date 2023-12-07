import re
import numpy as np


def parse_runs(lines: str) -> list[tuple[int, int]]:
    times = list(map(int, re.sub(r"\s+", " ", lines[0][len("Time:"):].strip()).split()))
    distances = list(map(int, re.sub(r"\s+", " ", lines[1][len("Distance:"):].strip()).split()))
    return list(zip(times, distances))


def compute_ways_to_beat(time: int, distance: int) -> int:
    if 4 * (distance + 1) > time**2:
        return 0
    # solve the quadratic distance < t * (time - t) (distance + 1 <= t * (time - t))
    t_1 = np.ceil(time / 2 - np.sqrt((time / 2)**2 - distance - 1))
    t_2 = np.floor(time / 2 + np.sqrt((time / 2)**2 - distance - 1))
    # they are definitely both non-negative, also it is still possible to hit 0 solutions if (T/2)**2 == distance and T/2 is not an integer
    assert distance < t_1 * (time - t_1)
    assert distance < t_2 * (time - t_2)
    return t_2 - t_1 + 1


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    runs = parse_runs(lines)
    ways_to_beat_per_run = [compute_ways_to_beat(time, distance) for time, distance in runs]
    return int(np.prod(ways_to_beat_per_run))


def main():
    assert solution("test_input.txt") == 288
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
