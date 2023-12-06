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


def was_mapped_by(destination_value: int, map_entry: MapEntry) -> bool:
    destination_range_start, _, range_length = map_entry
    return destination_range_start <= destination_value < destination_range_start + range_length


def unapply_map_entry(destination_value: int, map_entry: MapEntry) -> int:
    """Assumes that the value is mapped by the entry."""

    destination_range_start, source_range_start, _ = map_entry
    offset = destination_range_start - source_range_start
    return destination_value - offset


def apply_map(destination_value: int, almanac_map: AlmanacMap) -> list[int]:
    _, _, map_entries = almanac_map
    possible_sources = [destination_value]
    for map_entry in map_entries:
        if was_mapped_by(destination_value, map_entry):
            possible_sources.append(unapply_map_entry(destination_value, map_entry))
            print(f"{destination_value} could have been mapped by {map_entry} from {possible_sources[-1]}")
    return possible_sources


def in_value_range(value: int, value_range: ValueRange) -> bool:
    range_start, range_length = value_range
    return range_start <= value < range_start + range_length


def reverse_mapping(input_file: str, target_value: int):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
    source_value_ranges = parse_seeds(lines[0])
    maps = parse_maps(lines[2:])
    current_values = [target_value]
    for almanac_map in reversed(maps):
        print(f"{almanac_map[0]} <- {almanac_map[1]}")
        current_values = [source_value for current_value in current_values for source_value in apply_map(current_value, almanac_map)]
        print(current_values)


def main():
    # reverse_mapping("test_input.txt", 35)
    reverse_mapping("input.txt", 1)


if __name__ == "__main__":
    main()
