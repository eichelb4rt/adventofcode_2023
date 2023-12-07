from dataclasses import dataclass


@dataclass
class MapEntry:
    destination_start: int
    source_start: int
    length: int

    def __post_init__(self):
        self.source_end = self.source_start + self.length - 1
        self.destination_end = self.destination_start + self.length - 1
        self.offset = self.destination_start - self.source_start


@dataclass
class AlmanacMap:
    source_category: str
    destination_category: str
    entries: list[MapEntry]


@dataclass
class ValueRange:
    start: int
    length: int

    def __post_init__(self):
        self.end = self.start + self.length - 1


def parse_seeds(line: str) -> list[ValueRange]:
    numbers = list(map(int, line[len("seeds: "):].split()))
    starts = numbers[0::2]
    lengths = numbers[1::2]
    return [ValueRange(start, length) for start, length in zip(starts, lengths)]

# TODO: try doing it without the tuple


def parse_map_entry(line: str) -> MapEntry:
    return MapEntry(*tuple(map(int, line.split())))


def parse_map(lines: list[str]) -> AlmanacMap:
    # example: "seed-to-soil map:"
    source_category, destination_category = lines[0].split()[0].split("-to-")
    return AlmanacMap(source_category, destination_category, list(map(parse_map_entry, lines[1:])))


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
    # mapped start could be bigger than mapped end, but then n_mapped is 0
    mapped_start = max(source_range.start, map_entry.source_start)
    mapped_end = min(source_range.end, map_entry.source_end)
    n_mapped = max(0, mapped_end - mapped_start + 1)
    return ValueRange(mapped_start, n_mapped)


def apply_map_entry(source_range: ValueRange, map_entry: MapEntry) -> tuple[list[ValueRange], list[ValueRange]]:
    # find the value range where the values will actually change
    mapped_range = find_mapped_range(source_range, map_entry)
    # if we map 0 values in here, all values stay the same
    if mapped_range.length == 0:
        return [], [source_range]
    # the value range could be split up into multiple ranges my the map entry
    unmapped_ranges: list[ValueRange] = []
    mapped_ranges: list[ValueRange] = []
    # entries before the mapped values stay the same (these are mapped_start - source_values_start many values)
    n_before_mapped = mapped_range.start - source_range.start
    if n_before_mapped > 0:
        unmapped_ranges.append(ValueRange(source_range.start, n_before_mapped))
    # the map is an additive offset
    mapped_ranges.append(ValueRange(mapped_range.start + map_entry.offset, mapped_range.length))
    # HUNTED_STARTS = [0, 1287961387, 1251886222, 2602570677, 2520588939, 3209251068]
    # entries after the mapped values stay the same
    n_after_mapped = source_range.end - mapped_range.end
    if n_after_mapped > 0:
        unmapped_ranges.append(ValueRange(mapped_range.end + 1, n_after_mapped))
    return mapped_ranges, unmapped_ranges


def apply_map(source_value_ranges: list[ValueRange], almanac_map: AlmanacMap) -> list[ValueRange]:
    mapped_ranges: list[ValueRange] = []
    for map_entry in almanac_map.entries:
        ranges_per_source = [apply_map_entry(source_value_range, map_entry) for source_value_range in source_value_ranges]
        # flatten new mapped ranges and append them to the already mapped ranges
        mapped_ranges += [mapped_range for mapped_ranges, _ in ranges_per_source for mapped_range in mapped_ranges]
        # flatten new unmapped ranges and continue mapping them
        source_value_ranges = [unmapped_range for _, unmapped_ranges in ranges_per_source for unmapped_range in unmapped_ranges]
    return mapped_ranges + source_value_ranges


def overlap(map_entry_1: MapEntry, map_entry_2: MapEntry) -> bool:
    return map_entry_2.source_start <= map_entry_1.source_start <= map_entry_2.source_end or map_entry_2.source_start <= map_entry_1.source_end <= map_entry_2.source_end


def solution(input_file: str):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    source_value_ranges = parse_seeds(lines[0])
    maps = parse_maps(lines[2:])
    # assert that the map entries in each map respectively don't overlap
    for almanac_map in maps:
        for map_entry_1 in almanac_map.entries:
            for map_entry_2 in almanac_map.entries:
                if map_entry_1 != map_entry_2:
                    assert not overlap(map_entry_1, map_entry_2)
    # propagate
    for almanac_map in maps:
        source_value_ranges = apply_map(source_value_ranges, almanac_map)
    return min([value_range.start for value_range in source_value_ranges])


def main():
    assert solution("test_input.txt") == 46
    answer = solution("input.txt")
    print(f"<flavor text>: {answer}")


if __name__ == "__main__":
    main()
