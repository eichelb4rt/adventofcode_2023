import numpy as np
import numpy.typing as npt

UNFOLDING_FACTOR = 5


def parse_line(line: str) -> tuple[str, list[int]]:
    line, sequence = line.split()
    return line, list(map(int, sequence.split(",")))


def unfold_spring_line(spring_line: str) -> str:
    return "?".join([spring_line] * UNFOLDING_FACTOR)


def unfold_sequences(sequence: list[int]) -> list[int]:
    return sequence * UNFOLDING_FACTOR


def is_possible_last_placement(sequence_length: int, spring_line: str, placement: int, cutoff: int) -> bool:
    """Returns if it is possible to place n contiguous '#' at the given position, such that it is the last occurence of '#' before the cutoff."""

    # a placement of (exactly) n contiguous broken springs is possible if:
    # - the placement starts at the start or the left of the placement is a working or unknown spring, and
    # - the placement ends at the end or the right of the placement is a working or unknown spring, and
    # - spring_line[placement : placement + n] is filled with only broken and unknown springs
    if placement > 0 and spring_line[placement - 1] == "#":
        return False
    if placement + sequence_length < len(spring_line) and spring_line[placement + sequence_length] == "#":
        return False
    for spring in spring_line[placement: placement + sequence_length]:
        if spring == ".":
            return False
    # if it should be the last placement (no other contiguous broken springs should exist after this one), then there can't be any broken spring between the end of this placement and the cutoff
    for spring in spring_line[placement + sequence_length: cutoff]:
        if spring == "#":
            return False
    return True


def is_possible_only_placement(sequence_length: int, spring_line: str, placement: int, cut_off: int) -> bool:
    """Returns if it is possible to place n contiguous '#' at the given position, such that it is the only occurence of '#' before the cutoff."""

    if not is_possible_last_placement(sequence_length, spring_line, placement, cut_off):
        return False
    for spring in spring_line[:placement]:
        if spring == "#":
            return False
    return True


def compute_possible_as_last_placements(sequence_length: int, spring_line: str) -> npt.NDArray[np.bool8]:
    """possible_last_placements[position][cut_off] == is_possible_last_placement(n_contiguous_broken, spring_line, placement, cut_off)"""

    n_possible_positions = len(spring_line) - sequence_length + 1
    n_cutoffs = len(spring_line) + 2
    return np.array([[is_possible_last_placement(sequence_length, spring_line, placement, cut_off) for cut_off in range(n_cutoffs)] for placement in range(n_possible_positions)], dtype=bool)


def compute_possible_as_only_placements(sequence_length: int, spring_line: str) -> npt.NDArray[np.bool8]:
    """possible_only_placements[position][cut_off] == is_possible_only_placement(n_contiguous_broken, spring_line, placement, cut_off)"""

    n_possible_positions = len(spring_line) - sequence_length + 1
    n_cutoffs = len(spring_line) + 2
    return np.array([[is_possible_only_placement(sequence_length, spring_line, placement, cutoff) for cutoff in range(n_cutoffs)] for placement in range(n_possible_positions)], dtype=bool)


def compute_next_n_possible_arrangements(sequence_length: int, possible_placements: npt.NDArray[np.bool8], n_arrangements: npt.NDArray[np.int64]) -> list[int]:
    """For the sequence k, the k-th n_arrangements[i] = # of arrangements of the remaining sequences after k (k + 1, ..., n), given sequence k is positioned at i.
    With this, (k-1)-th n_arrangements[i] is the sum of all k-th n_arrangements[j] where i is possible as a last position for the sequence k-1 before j."""

    n_possible_placements = possible_placements.shape[0]
    n_arrangements_next = np.empty(n_possible_placements, dtype=np.int64)
    length_arrangements = n_arrangements.shape[0]
    for placement in range(n_possible_placements):
        # the number of possibilities to place the next one after the current one (there needs to be a free space between the two contiguous sequences)
        first_position_after_sequence = placement + sequence_length + 1
        n_arrangements_next[placement] = possible_placements[placement, first_position_after_sequence:length_arrangements] @ n_arrangements[first_position_after_sequence:]
    return n_arrangements_next


def compute_possible_arrangements(spring_line: str, sequences: list[int]) -> int:
    # pre-process the possible placements for the first sequence, and
    possible_first_placements = compute_possible_as_only_placements(sequences[0], spring_line)
    # if there's only one sequence, we got an easy job
    if len(sequences) == 1:
        return np.count_nonzero(possible_first_placements[:, -1])
    # pre-process the possible placements for all the other occuring lengths of sequences
    occuring_sequence_lengths = set(sequences)
    possible_placements_for_sequence = {sequence_length: compute_possible_as_last_placements(sequence_length, spring_line) for sequence_length in occuring_sequence_lengths}
    # start building the first number of arrangements (if we only had the last n_contiguous)
    sequence_length = sequences[-1]
    n_possible_arrangements = possible_placements_for_sequence[sequence_length][:, -1].astype(np.int64)
    # the next sequence could theoretically start after the line
    for sequence_length in reversed(sequences[1:-1]):
        n_possible_arrangements = compute_next_n_possible_arrangements(sequence_length, possible_placements_for_sequence[sequence_length], n_possible_arrangements)
    # the last one has to be the only sequence
    n_possible_arrangements = compute_next_n_possible_arrangements(sequences[0], possible_first_placements, n_possible_arrangements)
    return sum(n_possible_arrangements)


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    spring_lines, sequences = zip(*map(parse_line, lines))
    spring_lines = list(map(unfold_spring_line, spring_lines))
    sequences = list(map(unfold_sequences, sequences))
    return sum([compute_possible_arrangements(spring_line, sequence) for spring_line, sequence in zip(spring_lines, sequences)])


def main():
    assert solution("test_input.txt") == 525152
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
