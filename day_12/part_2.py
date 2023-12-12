UNFOLDING_CONSTANT = 5


def parse_line(line: str) -> tuple[str, list[int]]:
    line, sequence = line.split()
    return line, list(map(int, sequence.split(",")))


def unfold_spring_line(spring_line: str) -> str:
    return "?".join([spring_line] * UNFOLDING_CONSTANT)


def unfold_sequences(sequence: list[int]) -> list[int]:
    return sequence * UNFOLDING_CONSTANT


def find_unknown(line: str) -> list[int]:
    return [i for i, spring in enumerate(line) if spring == "?"]


def is_possible_last_placement(n_contiguous_broken: int, spring_line: str, placement: int, next_can_start_at: int) -> bool:
    # a placement of (exactly) n contiguous broken springs is possible if:
    # - the placement starts at the start or the left of the placement is a working or unknown spring, and
    # - the placement ends at the end or the right of the placement is a working or unknown spring, and
    # - spring_line[placement : placement + n] is filled with only broken and unknown springs
    if placement > 0 and spring_line[placement - 1] not in [".", "?"]:
        return False
    if placement + n_contiguous_broken < len(spring_line) and spring_line[placement + n_contiguous_broken] not in [".", "?"]:
        return False
    for spring in spring_line[placement: placement + n_contiguous_broken]:
        if spring not in ["#", "?"]:
            return False
    # if it should be the last placement (no other contiguous broken springs should exist after this one), then there can't be any broken spring between the end of this placement and the cutoff
    for spring in spring_line[placement + n_contiguous_broken: next_can_start_at]:
        if spring == "#":
            return False
    return True


def is_possible_only_placement(n_contiguous_broken: int, spring_line: str, placement: int, next_can_start_at: int) -> bool:
    if not is_possible_last_placement(n_contiguous_broken, spring_line, placement, next_can_start_at):
        return False
    for spring in spring_line[:placement]:
        if spring == "#":
            return False
    return True


def compute_possible_last_placements(n_contiguous_broken: int, spring_line: str) -> list[list[bool]]:
    """possible_placements[position][next_can_start_at]"""

    return [[is_possible_last_placement(n_contiguous_broken, spring_line, placement, next_can_start_at) for next_can_start_at in range(len(spring_line) + 2)] for placement in range(len(spring_line) - n_contiguous_broken + 1)]


def compute_possible_only_placements(n_contiguous_broken: int, spring_line: str) -> list[list[bool]]:
    """possible_placements[position][next_can_start_at]"""

    return [[is_possible_only_placement(n_contiguous_broken, spring_line, placement, next_can_start_at) for next_can_start_at in range(len(spring_line) + 2)] for placement in range(len(spring_line) - n_contiguous_broken + 1)]


def compute_next_n_possible_arrangements(n_contiguous: int, possible_placements_current: list[bool], n_possible_arrangements_last: list[int], n_possible_placements: int) -> list[int]:
    n_possible_arrangements = []
    for placement in range(n_possible_placements):
        # the number of possibilities to place the next one after the current one (there needs to be a free space between the two contiguous sequences)
        next_min_placement = placement + n_contiguous + 1
        n_placements_next_after_current = sum([possible_placements_current[placement][next_placement] * n_possible_arrangements_last[next_placement] for next_placement in range(next_min_placement, len(n_possible_arrangements_last))])
        n_possible_arrangements.append(n_placements_next_after_current)
    return n_possible_arrangements


def compute_possible_arrangements(spring_line: str, sequences: list[int]) -> int:
    needed_n_contiguous = set(sequences)
    possible_placements_for_n_contiguous = {n_contiguous: compute_possible_last_placements(n_contiguous, spring_line) for n_contiguous in needed_n_contiguous}
    # if len(sequences) == 0, then sequences[-1] == sequences[0]
    if len(sequences) == 1:
        n_contiguous = sequences[0]
        n_possible_placements = len(spring_line) - n_contiguous + 1
        possible_placements = compute_possible_only_placements(n_contiguous, spring_line)
        n_possible_arrangements = [int(possible_placements[placement][len(spring_line)]) for placement in range(n_possible_placements)]
        return sum(n_possible_arrangements)
    # start building the first number of arrangements (if we only had the last n_contiguous)
    n_contiguous = sequences[-1]
    n_possible_placements = len(spring_line) - n_contiguous + 1
    # the next sequence could theoretically start after the line
    n_possible_arrangements = [int(possible_placements_for_n_contiguous[n_contiguous][placement][len(spring_line)]) for placement in range(n_possible_placements)]
    for n_contiguous in reversed(sequences[1:-1]):
        n_possible_placements = len(spring_line) - n_contiguous + 1
        possible_placements = possible_placements_for_n_contiguous[n_contiguous]
        n_possible_arrangements = compute_next_n_possible_arrangements(n_contiguous, possible_placements, n_possible_arrangements, n_possible_placements)
    # the last one has to be the only sequence
    n_contiguous = sequences[0]
    n_possible_placements = len(spring_line) - n_contiguous + 1
    possible_placements = compute_possible_only_placements(n_contiguous, spring_line)
    n_possible_arrangements = compute_next_n_possible_arrangements(n_contiguous, possible_placements, n_possible_arrangements, n_possible_placements)
    return sum(n_possible_arrangements)


def test_implementation():
    line = "#???????? 1"
    spring_line, sequences = parse_line(line)
    assert compute_possible_arrangements(spring_line, sequences) == 1
    spring_line = unfold_spring_line(spring_line)
    sequences = unfold_sequences(sequences)
    assert compute_possible_arrangements(spring_line, sequences) == 1


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    spring_lines, sequences = zip(*map(parse_line, lines))
    spring_lines = list(map(unfold_spring_line, spring_lines))
    sequences = list(map(unfold_sequences, sequences))
    return sum([compute_possible_arrangements(spring_line, sequence) for spring_line, sequence in zip(spring_lines, sequences)])


def main():
    test_implementation()
    assert solution("test_input.txt") == 525152
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
