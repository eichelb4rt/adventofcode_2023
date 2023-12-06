# destination range start, source range start, range length
MapEntry = tuple[int, int, int]
# source category, destination category, entries
AlmanacMap = tuple[str, str, list[MapEntry]]
# range start, range length
ValueRange = tuple[int, int]


def parse_seeds(line: str) -> list[ValueRange]:
    numbers = list(map(int, line[len("seeds: "):].split()))
    starts = numbers[0::2]
    lengths = numbers[1::2]
    return list(zip(starts, lengths))


def parse_map_entry(line: str) -> MapEntry:
    return tuple(map(int, line.split()))


def parse_map(lines: list[str]) -> AlmanacMap:
    # example: "seed-to-soil map:"
    source_category, destination_category = lines[0].split()[0].split("-to-")
    return source_category, destination_category, list(map(parse_map_entry, lines[1:]))


def partition_map_lines(lines: list[str]) -> list[list[str]]:
    map_lines: list[list[str]] = []
    map_start = 0
    for i, line in enumerate(lines):
        # source-to-destination starts a map
        if "-to-" in line:
            map_start = i
        # empty line ends the map
        elif len(line.strip()) == 0:
            map_lines.append(lines[map_start:i])
    # append last map
    map_lines.append(lines[map_start:])
    return map_lines


def parse_maps(lines: list[str]) -> list[AlmanacMap]:
    partitioned_lines = partition_map_lines(lines)
    return list(map(parse_map, partitioned_lines))


def find_mapped_range(source_range: ValueRange, map_entry: MapEntry) -> ValueRange:
    source_values_start, n_source_values = source_range
    _, map_entry_start, map_entry_length = map_entry
    source_values_end = source_values_start + n_source_values - 1
    map_entry_end = map_entry_start + map_entry_length - 1
    # mapped start could be bigger than mapped end, but then n_mapped is 0
    mapped_start = max(source_values_start, map_entry_start)
    mapped_end = min(source_values_end, map_entry_end)
    n_mapped = max(0, mapped_end - mapped_start + 1)
    return mapped_start, n_mapped


def apply_map_entry(source_range: ValueRange, map_entry: MapEntry) -> tuple[list[ValueRange], list[ValueRange]]:
    source_values_start, n_source_values = source_range
    # find the value range where the values will actually change
    mapped_start, n_mapped = find_mapped_range(source_range, map_entry)
    # if we map 0 values in here, all values stay the same
    if n_mapped == 0:
        return [], [source_range]
    # the value range could be split up into multiple ranges my the map entry
    unmapped_ranges: list[ValueRange] = []
    mapped_ranges: list[ValueRange] = []
    # entries before the mapped values stay the same (these are mapped_start - source_values_start many values)
    n_before_mapped = mapped_start - source_values_start
    if n_before_mapped > 0:
        unmapped_ranges.append((source_values_start, n_before_mapped))
    # mapped entries are mapped with an added offset. the number of mapped values does not change with that
    destination_range_start, source_range_start, _ = map_entry
    offset = destination_range_start - source_range_start
    mapped_ranges.append((mapped_start + offset, n_mapped))
    # HUNTED_STARTS = [0, 1287961387, 1251886222, 2602570677, 2520588939, 3209251068]
    # if mapped_start + offset in HUNTED_STARTS:
    #     print(f"found map to {mapped_start + offset}: mapped from {mapped_start} with source range {source_range}")
    # entries after the mapped values stay the same
    source_values_end = source_range_start + n_source_values - 1
    mapped_end = mapped_start + n_mapped - 1
    n_after_mapped = source_values_end - mapped_end
    if n_after_mapped > 0:
        unmapped_ranges.append((mapped_end + 1, n_after_mapped))
    # if mapped_end + 1 in HUNTED_STARTS:
    #     print(f"found cutoff for {mapped_end + 1}: cut off from range {source_range} with map entry {map_entry}")
    return mapped_ranges, unmapped_ranges


def apply_map(source_value_ranges: list[ValueRange], almanac_map: AlmanacMap) -> list[ValueRange]:
    _, _, map_entries = almanac_map
    mapped_ranges: list[ValueRange] = []
    for map_entry in map_entries:
        value_ranges_per_source = [apply_map_entry(source_value_range, map_entry) for source_value_range in source_value_ranges]
        # flatten new mapped ranges and append them to the already mapped ranges
        mapped_ranges += [mapped_range for mapped_ranges, _ in value_ranges_per_source for mapped_range in mapped_ranges]
        # flatten new unmapped ranges and continue mapping them
        source_value_ranges = [unmapped_range for _, unmapped_ranges in value_ranges_per_source for unmapped_range in unmapped_ranges]
    return mapped_ranges + source_value_ranges


def overlap(map_entry_1: MapEntry, map_entry_2: MapEntry) -> bool:
    _, source_range_start_1, range_length_1 = map_entry_1
    _, source_range_start_2, range_length_2 = map_entry_2
    source_range_end_1 = source_range_start_1 + range_length_1 - 1
    source_range_end_2 = source_range_start_2 + range_length_2 - 1
    return source_range_start_2 <= source_range_start_1 <= source_range_end_2 or source_range_start_2 <= source_range_end_1 <= source_range_end_2


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    source_value_ranges = parse_seeds(lines[0])
    maps = parse_maps(lines[2:])
    # assert that the map entries in each map respectively don't overlap
    for almanac_map in maps:
        for map_entry_1 in almanac_map[2]:
            for map_entry_2 in almanac_map[2]:
                if map_entry_1 != map_entry_2:
                    assert not overlap(map_entry_1, map_entry_2)
    # propagate
    for almanac_map in maps:
        print(f"{almanac_map[0]} -> {almanac_map[1]}")
        source_value_ranges = apply_map(source_value_ranges, almanac_map)
    return min([range_start for range_start, _ in source_value_ranges])


def main():
    assert solution("test_input.txt") == 46
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
