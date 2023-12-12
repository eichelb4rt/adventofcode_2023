import itertools
from copy import deepcopy


UNFOLDING_CONSTANT = 5


def parse_line(line: str) -> tuple[list[str], list[int]]:
    line, check = line.split()
    return list(line), list(map(int, check.split(",")))


def unfold_spring_line(spring_line: list[str]) -> list[str]:
    line = "".join(spring_line)
    return list("?".join([line] * UNFOLDING_CONSTANT))


def unfold_check(check: list[int]) -> list[int]:
    return check * UNFOLDING_CONSTANT


def find_unknown(line: str) -> list[int]:
    return [i for i, spring in enumerate(line) if spring == "?"]


def compute_check(spring_line: list[str]) -> list[int]:
    check = []
    contiguous = 0
    for spring in spring_line:
        if spring == "#":
            contiguous += 1
        else:
            if contiguous > 0:
                check.append(contiguous)
            contiguous = 0
    if contiguous > 0:
        check.append(contiguous)
    return check


# def _compute_possible_arrangements(spring_line: list[str], check: list[int], unknown_indices: list[int], n_contiguous: int) -> int:
#     # TODO: might have to change this
#     if len(unknown_indices) == 0:
#         return 0

#     if spring_line[0] == "#":
#         if n_contiguous + 1 > check[0]:
#             return 0
#         return _compute_possible_arrangements(spring_line[1:], check, unknown_indices, n_contiguous + 1)
#     if spring_line[0] == ".":
#         if 0 < n_contiguous < check[0]:
#             return 0
#         if n_contiguous == check[0]:
#             return _compute_possible_arrangements(spring_line[1:], check[1:], unknown_indices, n_contiguous)
#         return _compute_possible_arrangements(spring_line[1:], check, unknown_indices, n_contiguous)


def find_islands(spring_line: list[str]) -> list[list[str]]:
    """Separates spring line into islands composed of '?' and '#'."""

    islands = []
    last_island_start = 0
    on_island = False
    for i, spring in enumerate(spring_line):
        # if we were on an island and reached the sea, save the island
        if on_island and spring == ".":
            islands.append(spring_line[last_island_start: i])
            on_island = False
        # if we were in the sea and step on an island, remember where it started
        elif not on_island and spring in ["#", "?"]:
            last_island_start = i
            on_island = True
    # save the last island if we didn't already
    if on_island:
        islands.append(spring_line[last_island_start:])
    return islands


def find_min_broken(island: list[str]) -> int:
    """How many broken springs are definitely on that island?"""

    return len([spring for spring in island if spring == "#"])


def cumulate(integers: list[int]) -> list[int]:
    cumulative_list = [None] * len(integers)
    cumulative_list[0] = integers[0]
    for i in range(1, len(integers)):
        cumulative_list[i] = cumulative_list[i - 1] + integers[i]
    return cumulative_list


SliceIndices = tuple[int, int]
Split = list[SliceIndices]
Check = list[int]


def compute_possible_island_fills(min_broken_springs: int, space: int, sum_of_broken_springs: list[int], sum_offset: int, index_offset: int) -> list[SliceIndices]:
    # a range of contiguous broken springs can fit into an island if:
    # - the number of definitely broken springs on that island is <= the sum of contiguous broken springs
    #   therefore min_broken_springs <= sum_of_broken_springs[j] - sum_offset
    # - and the space on that island >= the space needed for those contiguous broken springs, which is the sum of contiguous broken springs + the number of minimum working springs between them
    #   therefore space >= sum_of_broken_springs[j] - sum_offset + j
    possible_island_fills = [(index_offset, index_offset + j + 1) for j in range(len(sum_of_broken_springs)) if min_broken_springs <= sum_of_broken_springs[j] - sum_offset <= space - j]
    # the empty range is also possible if min_broken_strings == 0
    if min_broken_springs == 0:
        possible_island_fills.append((index_offset, index_offset))
    return possible_island_fills


def _compute_possible_splits(min_broken_per_island: list[int], space_per_island: list[int], sum_of_broken_springs: list[int], sum_offset: int, index_offset: int) -> list[Split]:
    # print("================")
    # print(f"min_broken_per_island: {min_broken_per_island}")
    # print(f"space_per_island: {space_per_island}")
    # print(f"sum_of_broken_springs: {sum_of_broken_springs}")
    # print(f"sum_offset: {sum_offset}")
    # print(f"index_offset: {index_offset}")
    n_islands = len(min_broken_per_island)
    if n_islands == 0:
        # all contiguous broken springs could be distributed, return the empty split
        if len(sum_of_broken_springs) == 0:
            return [[]]
        # not all contiguous broken springs could be distributed, therefore no possible split
        return []
    possible_splits = []
    possible_first_ranges = compute_possible_island_fills(min_broken_per_island[0], space_per_island[0], sum_of_broken_springs, sum_offset, index_offset)
    # print(f"min_broken: {min_broken_per_island[0]}")
    # print(f"space: {space_per_island[0]}")
    # if len(sum_of_broken_springs) > 0:
    #     print(f"min_broken_springs_to_fit: {sum_of_broken_springs[0] - sum_offset}")
    # print(f"possible_first_ranges: {possible_first_ranges}")
    for slice_start, slice_end in possible_first_ranges:
        # if it's the empty slice, we have to pass on the sum offset, otherwise take the sum of the last broken springs
        new_sum_offset = sum_of_broken_springs[slice_end - index_offset - 1] if slice_end > index_offset else sum_offset
        for possible_rest_split in _compute_possible_splits(min_broken_per_island[1:], space_per_island[1:], sum_of_broken_springs[slice_end - index_offset:], new_sum_offset, slice_end):
            possible_splits.append([(slice_start, slice_end)] + possible_rest_split)
    return possible_splits


def compute_possible_splits(min_broken_per_island: list[int], space_per_island: list[int], sum_of_broken_springs: list[int]) -> list[Split]:
    return _compute_possible_splits(min_broken_per_island, space_per_island, sum_of_broken_springs, 0, 0)


def split_to_checks(split: Split, entire_check: list[int]) -> list[Check]:
    return [entire_check[slice_start: slice_end] for slice_start, slice_end in split]


def possible_check_partitions(islands: list[list[str]], check: Check) -> list[list[Check]]:
    min_broken_per_island = list(map(find_min_broken, islands))
    space_per_island = list(map(len, islands))
    sum_of_broken_springs = cumulate(check)
    possible_splits = compute_possible_splits(min_broken_per_island, space_per_island, sum_of_broken_springs)
    return [split_to_checks(split, check) for split in possible_splits]


def compute_possible_arrangements_for_island(island: list[str], check: Check) -> int:

    pass


def compute_possible_arrangements(spring_line: list[str], check: Check) -> int:
    # return _compute_possible_arrangements(spring_line, check, find_unknown(spring_line), 0)
    islands = find_islands(spring_line)
    partitions = possible_check_partitions(islands, check)
    print(len(partitions))
    for partition in partitions:
        for island, island_check in zip(islands, partition):
            pass
    return None


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    spring_lines, checks = zip(*map(parse_line, lines))
    spring_lines = list(map(unfold_spring_line, spring_lines))
    checks = list(map(unfold_check, checks))
    for spring_line, check in zip(deepcopy(spring_lines), checks):
        # print(spring_line, check)
        compute_possible_arrangements(spring_line, check)
    return None
    # return sum([compute_possible_arrangements(spring_line, check) for spring_line, check in zip(spring_lines, checks)])


def test_implementation():
    global UNFOLDING_CONSTANT
    original_unfolding_constant = UNFOLDING_CONSTANT
    UNFOLDING_CONSTANT = 2
    line = ".?.?#. 1,2"
    spring_line, check = parse_line(line)
    spring_line = unfold_spring_line(spring_line)
    check = unfold_check(check)
    assert compute_possible_arrangements(spring_line, check) == 2
    UNFOLDING_CONSTANT = original_unfolding_constant


def main():
    # test_implementation()
    # assert solution("test_input.txt") == 21
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
