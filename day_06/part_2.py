import numpy as np


def parse_run(lines: str) -> tuple[int, int]:
    time = int(lines[0][len("Time:"):].replace(" ", ""))
    distance = int(lines[1][len("Distance:"):].replace(" ", ""))
    return time, distance


def compute_ways_to_beat(time: int, distance: int) -> int:
    if 4 * (distance + 1) > time**2:
        return 0
    # solve the quadratic distance < t * (time - t) (distance + 1 <= t * (time - t))
    t_1 = int(np.ceil(time / 2 - np.sqrt((time / 2)**2 - distance - 1)))
    t_2 = int(np.floor(time / 2 + np.sqrt((time / 2)**2 - distance - 1)))
    # they are definitely both non-negative, also it is still possible to hit 0 solutions if (T/2)**2 == distance and T/2 is not an integer
    assert distance < t_1 * (time - t_1)
    assert distance < t_2 * (time - t_2)
    return t_2 - t_1 + 1


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    time, distance = parse_run(lines)
    return compute_ways_to_beat(time, distance)


def main():
    assert solution("test_input.txt") == 71503
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
